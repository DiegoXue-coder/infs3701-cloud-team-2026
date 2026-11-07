"""Reading Tracker with local development and shared DynamoDB storage."""
import os
from datetime import datetime, timezone
from threading import Lock
from uuid import uuid4

from flask import Flask, abort, jsonify, redirect, render_template_string, request, url_for


class LocalStore:
    def __init__(self):
        self.books = []
        self.lock = Lock()

    def load_books(self):
        with self.lock:
            return list(self.books)

    def save_book(self, entry):
        with self.lock:
            self.books.append(entry)
        return entry["record_id"]


class StorageError(Exception):
    """The configured storage could not complete an operation."""


class DynamoStore:
    def __init__(self, region, table_name):
        self.region = region
        self.table_name = table_name

    def table(self):
        # Keep the AWS SDK and credential discovery out of local mode and /health.
        import boto3
        from botocore.config import Config

        session = boto3.session.Session()
        return session.resource(
            "dynamodb",
            region_name=self.region,
            config=Config(connect_timeout=2, read_timeout=3,
                          retries={"mode": "standard", "total_max_attempts": 2}),
        ).Table(self.table_name)

    def load_books(self):
        from botocore.exceptions import BotoCoreError, ClientError

        books = []
        try:
            table = self.table()
            page = table.scan(ConsistentRead=True)
            while True:
                books.extend(page["Items"])
                cursor = page.get("LastEvaluatedKey")
                if not cursor:
                    return books
                page = table.scan(ConsistentRead=True, ExclusiveStartKey=cursor)
        except (BotoCoreError, ClientError) as error:
            raise StorageError("Could not load reading records") from error

    def save_book(self, entry):
        from botocore.exceptions import BotoCoreError, ClientError

        try:
            self.table().put_item(
                Item=entry, ConditionExpression="attribute_not_exists(record_id)"
            )
        except (BotoCoreError, ClientError) as error:
            raise StorageError("Could not save reading record") from error
        return entry["record_id"]


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
<p class="sub">Log what you are reading, how far along you are, and what you thought. {{ storage_label }}</p>

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
  <textarea id="note" name="note" rows="3" maxlength="2000"></textarea>
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


def parse_entry(form):
    title = form.get("title", "").strip()
    note = form.get("note", "").strip()
    status = form.get("status", "reading")
    if not 1 <= len(title) <= 120 or len(note) > 2000 or status not in STATUS_LABEL:
        raise ValueError("Check the title, note length and reading status.")

    try:
        pages_read = int(form.get("pages_read") or 0)
        total_pages = int(form.get("total_pages") or 0)
        rating = int(form["rating"]) if form.get("rating") else None
    except ValueError as error:
        raise ValueError("Pages and ratings must be whole numbers.") from error

    # DynamoDB numbers allow up to 38 digits. Keep both modes on the same contract.
    if not (0 <= pages_read < 10**38 and 0 <= total_pages < 10**38):
        raise ValueError("Page counts must be non-negative and at most 38 digits.")
    if total_pages and pages_read > total_pages:
        raise ValueError("Pages read cannot exceed total pages.")
    if rating is not None and not 1 <= rating <= 5:
        raise ValueError("Rating must be between 1 and 5.")

    return {
        "record_id": str(uuid4()),
        "title": title,
        "status": status,
        "pages_read": pages_read,
        "total_pages": total_pages,
        "rating": rating,
        "note": note,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="microseconds"),
    }


def create_app():
    mode = os.environ.get("READING_DATA_MODE")
    if mode == "local":
        store = LocalStore()
        storage_label = "Local development mode. Records reset when the process stops."
    elif mode == "dynamodb":
        region = os.environ.get("AWS_DEFAULT_REGION")
        table_name = os.environ.get("READING_TABLE")
        if not region or not table_name:
            raise RuntimeError("DynamoDB mode requires AWS_DEFAULT_REGION and READING_TABLE.")
        store = DynamoStore(region, table_name)
        storage_label = "Records are stored in the shared reading library."
    else:
        raise RuntimeError("Set READING_DATA_MODE to local or dynamodb.")

    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 64 * 1024
    instance = os.environ.get("APP_INSTANCE") or ("local-dev" if mode == "local" else "unconfigured")

    @app.after_request
    def identify(response):
        response.headers["X-App-Instance"] = instance
        return response

    @app.get("/health")
    def health():
        return jsonify(status="ok", instance=instance, stage="reading-tracker")

    @app.route("/", methods=["GET", "POST"])
    def home():
        try:
            if request.method == "POST":
                try:
                    entry = parse_entry(request.form)
                except ValueError as error:
                    abort(400, description=str(error))
                store.save_book(entry)
                return redirect(url_for("home"))

            books = sorted(store.load_books(),
                           key=lambda book: (book["created_at"], book["record_id"]),
                           reverse=True)
        except StorageError:
            app.logger.exception("Reading Tracker storage operation failed")
            abort(503, description="Reading records are temporarily unavailable.")

        # DynamoDB returns Decimal for numbers. Convert before calculating progress.
        display_books = []
        for book in books:
            total = int(book["total_pages"])
            pages = int(book["pages_read"])
            progress = round(pages / total * 100) if total else None
            display_books.append(dict(book, pct=progress))
        return render_template_string(
            PAGE, books=display_books, s=compute_stats(books),
            STATUS_LABEL=STATUS_LABEL, storage_label=storage_label,
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("APP_PORT", "8000")))
