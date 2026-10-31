#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reading Tracker - a personal book-progress tracker running on EC2 with S3 storage.
Data model: each book entry is stored as an S3 object under the 'books/' prefix.
Server-side work: computing library stats (counts, total pages, avg rating, progress).
"""
import io, re, json, os
from datetime import datetime, timezone
from urllib.parse import quote
import boto3
from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)

BUCKET = os.environ.get("READING_BUCKET", "")
PREFIX = "books/"

# --- S3 helpers --------------------------------------------------------------
def s3():
    return boto3.client("s3")

def load_books():
    """Read every book object from S3 and return them newest-first."""
    books = []
    paginator = s3().get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET, Prefix=PREFIX):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            try:
                data = s3().get_object(Bucket=BUCKET, Key=key)
                raw = data["Body"].read().decode("utf-8")
                entry = json.loads(raw)
                entry["key"] = key
                books.append(entry)
            except Exception:
                continue  # skip any object that is not a valid book record
    books.sort(key=lambda b: b.get("created_at", ""), reverse=True)
    return books

def save_book(entry):
    """Write one book entry to S3 under books/<timestamp>_<slug>.json"""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    slug = re.sub(r"[^a-z0-9]+", "-", entry["title"].lower()).strip("-")[:40]
    key = f"{PREFIX}{ts}_{slug or 'book'}.json"
    s3().put_object(Bucket=BUCKET, Key=key, Body=json.dumps(entry, ensure_ascii=False).encode("utf-8"))
    return key

# --- server-side stats -------------------------------------------------------
def compute_stats(books):
    total = len(books)
    reading = sum(1 for b in books if b.get("status") == "reading")
    finished = sum(1 for b in books if b.get("status") == "finished")
    want = sum(1 for b in books if b.get("status") == "want")
    total_pages = sum(int(b.get("pages_read") or 0) for b in books)
    rated = [int(b["rating"]) for b in books if b.get("rating")]
    avg_rating = round(sum(rated) / len(rated), 1) if rated else None
    return {
        "total": total, "reading": reading, "finished": finished, "want": want,
        "total_pages": total_pages, "avg_rating": avg_rating,
    }

STATUS_LABEL = {"want": "Want to read", "reading": "Reading", "finished": "Finished"}

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Reading Tracker</title>
<style>
body{max-width:820px;margin:36px auto;padding:0 20px;font-family:Arial,sans-serif;color:#17202a;background:#f4f7f9;line-height:1.5}
h1{color:#176b5b;margin-bottom:4px}.sub{color:#667;font-size:14px;margin-top:0}
.cards{display:flex;flex-wrap:wrap;gap:12px;margin:18px 0}
.card{flex:1 1 120px;background:#fff;border:1px solid #dce3e6;border-radius:8px;padding:14px}
.card .num{font-size:26px;font-weight:700;color:#176b5b}
.card .lbl{font-size:12px;color:#667}
form{background:#fff;border:1px solid #dce3e6;border-radius:8px;padding:18px;margin-bottom:22px}
label{display:block;margin-top:12px;font-weight:600;font-size:14px}
input,select,textarea{width:100%;box-sizing:border-box;padding:9px;margin-top:5px;border:1px solid #c8d1d8;border-radius:5px;font-size:14px}
.row{display:flex;gap:12px}.row>div{flex:1}
button{margin-top:16px;padding:10px 20px;color:#fff;background:#176b5b;border:0;border-radius:5px;font-size:15px;cursor:pointer}
article{background:#fff;border:1px solid #dce3e6;border-radius:8px;padding:16px;margin-bottom:14px}
article h2{margin:0 0 4px;color:#17202a}
.badge{display:inline-block;font-size:12px;padding:2px 9px;border-radius:10px;color:#fff;background:#5d8a7c}
.badge.fin{background:#2f8f5b}.badge.read{background:#b8860b}.badge.want{background:#7f8c8d}
.meta{color:#667;font-size:13px;margin-top:6px}
.stars{color:#e0a800;letter-spacing:2px}
.bar{height:8px;background:#e8edf0;border-radius:4px;overflow:hidden;margin-top:8px}
.bar>div{height:100%;background:#176b5b}
.note{background:#f0f5f3;border-left:3px solid #176b5b;padding:8px 12px;margin-top:10px;font-size:14px}
</style>
</head>
<body>
<h1>Reading Tracker</h1>
<p class="sub">Log what you are reading, how far along you are, and what you thought. Runs on EC2, stored in S3.</p>

<div class="cards">
  <div class="card"><div class="num">{{ s.total }}</div><div class="lbl">Books logged</div></div>
  <div class="card"><div class="num">{{ s.reading }}</div><div class="lbl">Reading now</div></div>
  <div class="card"><div class="num">{{ s.finished }}</div><div class="lbl">Finished</div></div>
  <div class="card"><div class="num">{{ s.total_pages }}</div><div class="lbl">Pages read</div></div>
  <div class="card"><div class="num">{% if s.avg_rating is not none %}{{ s.avg_rating }}/5{% else %}&ndash;{% endif %}</div><div class="lbl">Avg rating</div></div>
</div>

<form method="post">
  <label for="title">Book title</label>
  <input id="title" name="title" maxlength="120" required>
  <div class="row">
    <div>
      <label for="status">Status</label>
      <select id="status" name="status">
        <option value="want">Want to read</option>
        <option value="reading" selected>Reading</option>
        <option value="finished">Finished</option>
      </select>
    </div>
    <div>
      <label for="rating">Rating</label>
      <select id="rating" name="rating">
        <option value="">&ndash;</option>
        {% for i in range(1,6) %}<option value="{{ i }}">{{ i }} star</option>{% endfor %}
      </select>
    </div>
  </div>
  <div class="row">
    <div><label for="pages_read">Pages read</label><input id="pages_read" name="pages_read" type="number" min="0" value="0"></div>
    <div><label for="total_pages">Total pages</label><input id="total_pages" name="total_pages" type="number" min="0"></div>
  </div>
  <label for="note">Reading note</label>
  <textarea id="note" name="note" rows="3" maxlength="600"></textarea>
  <button type="submit">Add to tracker</button>
</form>

{% for b in books %}
<article>
  <h2>{{ b.title }}</h2>
  <span class="badge {{ b.status }}">{{ STATUS_LABEL.get(b.status, b.status) }}</span>
  {% if b.rating %}<span class="stars">{{ '★' * b.rating|int }}</span>{% endif %}
  <div class="meta">
    {{ b.pages_read }}{% if b.total_pages %}/{{ b.total_pages }}{% endif %} pages
    {% if b.pct is not none %} &middot; {{ b.pct }}% complete{% endif %}
    &middot; {{ b.created_at }}
  </div>
  {% if b.pct is not none %}<div class="bar"><div style="width:{{ b.pct }}%"></div></div>{% endif %}
  {% if b.note %}<div class="note">{{ b.note }}</div>{% endif %}
</article>
{% else %}
<p>No books yet. Add your first book above.</p>
{% endfor %}
</body>
</html>"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        note = request.form.get("note", "").strip()
        if title:
            try:
                pages_read = int(request.form.get("pages_read") or 0)
            except ValueError:
                pages_read = 0
            try:
                total_pages = int(request.form.get("total_pages") or 0)
            except ValueError:
                total_pages = 0
            rating = request.form.get("rating") or None
            status = request.form.get("status") if request.form.get("status") in STATUS_LABEL else "reading"
            if total_pages and total_pages > 0:
                pct = min(100, round(pages_read / total_pages * 100))
            else:
                pct = None
            entry = {
                "title": title, "status": status, "rating": rating,
                "pages_read": pages_read, "total_pages": total_pages, "pct": pct,
                "note": note,
                "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            }
            save_book(entry)
        return redirect(url_for("home"))
    books = load_books()
    stats = compute_stats(books)
    return render_template_string(PAGE, books=books, s=stats, STATUS_LABEL=STATUS_LABEL)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
