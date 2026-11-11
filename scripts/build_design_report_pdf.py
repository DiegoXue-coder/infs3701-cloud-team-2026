"""Render the English design report for technical review."""

from html import escape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/design-report-working.md"
OUTPUT = ROOT / "output/pdf/reading-tracker-design-review.pdf"
INK = colors.HexColor("#172F43")
MUTED = colors.HexColor("#486171")
ACCENT = colors.HexColor("#006D77")


def markup(text):
    text = escape(text)
    text = re.sub(r"`([^`]+)`", r'<font face="Courier">\1</font>', text)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)


def page_frame(canvas, doc):
    width, height = A4
    canvas.setFillColor(ACCENT)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(doc.leftMargin, height - 30, "INFS3701  /  READING TRACKER")
    canvas.drawRightString(width - doc.rightMargin, height - 30, "REVIEW DRAFT")
    canvas.setStrokeColor(colors.HexColor("#D5E2E8"))
    canvas.line(doc.leftMargin, 42, width - doc.rightMargin, 42)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 9)
    canvas.drawString(doc.leftMargin, 27, "Term 3, 2026  |  Design report")
    canvas.drawRightString(width - doc.rightMargin, 27, str(doc.page))


def main():
    source = SOURCE.read_text(encoding="utf-8")
    title, remainder = source.split("\n", 1)
    body_start = remainder.index("## 1. ")
    body, references = remainder[body_start:].split("## References and internal evidence", 1)
    body_style = ParagraphStyle(
        "Body", fontName="Helvetica", fontSize=10.75, leading=14.1,
        textColor=INK, alignment=TA_LEFT, spaceAfter=8,
        allowWidows=0, allowOrphans=0,
    )
    heading = ParagraphStyle(
        "Heading", parent=body_style, fontName="Helvetica-Bold", fontSize=14,
        leading=18, textColor=ACCENT, spaceBefore=10, spaceAfter=6, keepWithNext=True,
    )
    title_style = ParagraphStyle(
        "Title", parent=heading, fontSize=27, leading=31,
        textColor=INK, spaceBefore=0, spaceAfter=11,
    )
    note = ParagraphStyle("Note", parent=body_style, fontSize=9.5, leading=13, textColor=MUTED)
    story = [
        Paragraph(markup(title.removeprefix("# ")), title_style),
        Paragraph("Design report review draft  |  12 November 2026, Sydney", note),
        Spacer(1, 5),
    ]
    for block in body.strip().split("\n\n"):
        if block.startswith("## "):
            story.append(Paragraph(markup(block[3:]), heading))
        else:
            story.append(Paragraph(markup(" ".join(block.splitlines())), body_style))
    story.extend([PageBreak(), Paragraph("References and internal evidence", heading)])
    for block in references.strip().split("\n\n"):
        text = markup(block)
        match = re.search(r" https://\S+$", block)
        if match:
            url = escape(match.group().strip(), quote=True)
            text = markup(block[:match.start()]) + f' <link href="{url}" color="#006D77">AWS documentation</link>'
        story.append(Paragraph(text, body_style))
    story.append(Paragraph(markup(remainder[:body_start].strip()), note))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, leftMargin=49, rightMargin=49, topMargin=56,
        bottomMargin=54, title=title.removeprefix("# "), author="INFS3701 Reading Tracker team",
    )
    doc.build(story, onFirstPage=page_frame, onLaterPages=page_frame)


if __name__ == "__main__":
    main()
