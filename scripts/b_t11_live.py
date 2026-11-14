"""Verify the published demo over HTTP using only synthetic records."""
import argparse
from datetime import datetime, timezone
from html import unescape
import json
import re
from urllib.parse import urlencode
from urllib.request import Request, build_opener
from uuid import uuid4

from c_request_log import NoRedirect


LABELS = {"az-a", "az-b"}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--reference-title", help="Exact title of the operator’s 12/120-page, four-star record")
    parser.add_argument("--write-one-fictional", action="store_true")
    args = parser.parse_args()
    if not args.reference_title and not args.write_one_fictional:
        parser.error("provide --reference-title or --write-one-fictional")
    base = args.url.rstrip("/")
    opener = build_opener(NoRedirect())

    def request(path, form=None):
        data = urlencode(form).encode("ascii") if form is not None else None
        req = Request(base + path, data=data, headers={"Connection": "close"})
        try:
            response = opener.open(req, timeout=5)
        except OSError as error:
            if not hasattr(error, "code"):
                raise
            response = error
        with response:
            label = response.headers.get("X-App-Instance")
            print(json.dumps({"utc": datetime.now(timezone.utc).isoformat(), "method": req.get_method(),
                              "path": path, "status": response.code, "instance": label}), flush=True)
            require(label in LABELS, f"Unexpected instance label: {label!r}")
            return response.code, label, response.headers.get("Location"), response.read().decode("utf-8")

    def records_on_both(title, pages, rating):
        seen = set()
        for _ in range(6):
            status, label, _, body = request("/")
            require(status == 200 and "Records are stored in the shared reading library." in body,
                    "Business home or shared-store label did not match")
            articles = re.findall(r"<article\b[^>]*>(.*?)</article>", body, flags=re.S)
            matching = [article for article in articles if f"<h2>{title}</h2>" in unescape(article)]
            require(len(matching) == 1, f"Expected one exact match for {title!r} on {label}")
            row = unescape(matching[0])
            require('class="badge reading">Reading</span>' in row and f"{pages} pages" in row and f">{'★' * rating}<" in row,
                    f"Unexpected status, pages, or rating on {label}")
            seen.add(label)
            print(json.dumps({"verified_title": title, "instance": label, "matches": 1,
                              "status": "reading", "pages": pages, "rating": rating}), flush=True)
            if seen == LABELS:
                return
        raise RuntimeError(f"Business readback reached only {sorted(seen)}")

    seen_health = set()
    for _ in range(6):
        status, label, _, body = request("/health")
        require(status == 200 and json.loads(body) == {"stage": "reading-tracker", "instance": label, "status": "ok"},
                "Business health payload or label mismatch")
        seen_health.add(label)
        if seen_health == LABELS:
            break
    require(seen_health == LABELS, f"Health reached only {sorted(seen_health)}")
    if args.reference_title:
        records_on_both(args.reference_title, "12/120", 4)
    else:
        # Verify that both business pages can read the configured store before writing.
        seen_home = set()
        for _ in range(8):
            status, label, _, body = request("/")
            require(status == 200 and "Records are stored in the shared reading library." in body,
                    "Business home or shared-store label did not match")
            seen_home.add(label)
            if seen_home == LABELS:
                break
        require(seen_home == LABELS, f"Business home reached only {sorted(seen_home)}")

    if args.write_one_fictional:
        title = f"Fictional Alex T11 {uuid4().hex[:12]}"
        print(json.dumps({"synthetic_write_title": title, "max_post_attempts": 1}), flush=True)
        status, label, location, _ = request("/", {"title": title, "status": "reading",
                                                "pages_read": 9, "total_pages": 45, "rating": 5})
        require(status == 302 and location == "/", f"Single POST result: {status}, {location!r}")
        print(json.dumps({"synthetic_write_accepted": title, "writer": label}), flush=True)
        records_on_both(title, "9/45", 5)



if __name__ == "__main__":
    main()
