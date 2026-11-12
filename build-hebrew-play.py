#!/usr/bin/env python3
"""Build the Hebrew play (hebrew/act-1.md + hebrew/act-2.md) into one Word file.

Output: word-output/מזמור-לדוד-המחזה-העברי.docx
"""
import re
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).parent
SOURCES = [ROOT / "hebrew" / "act-1.md", ROOT / "hebrew" / "act-2.md"]
OUT = ROOT / "word-output" / "מזמור-לדוד-המחזה-העברי.docx"
FONT = "David"
GREY = RGBColor(0x55, 0x55, 0x55)

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(2.5)
sec.top_margin = sec.bottom_margin = Cm(2.5)
# right-to-left section
bidi = OxmlElement("w:bidi")
sec._sectPr.append(bidi)

INLINE = re.compile(r"(\*\*.+?\*\*|\*.+?\*)")


def set_rtl(p):
    pPr = p._p.get_or_add_pPr()
    b = OxmlElement("w:bidi")
    b.set(qn("w:val"), "1")
    pPr.append(b)


def style_run(run, size, bold=False, italic=False, color=None):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    fonts = rPr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        rPr.insert(0, fonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs"):
        fonts.set(qn(attr), FONT)
    for tag, val in (("w:bCs", bold), ("w:iCs", italic)):
        el = OxmlElement(tag)
        el.set(qn("w:val"), "1" if val else "0")
        rPr.append(el)
    sz = OxmlElement("w:szCs")
    sz.set(qn("w:val"), str(int(size * 2)))
    rPr.append(sz)
    rPr.append(OxmlElement("w:rtl"))


def new_par(align="right", before=0, after=6, indent=0, keep_next=False, style=None):
    p = doc.add_paragraph(style=style) if style else doc.add_paragraph()
    set_rtl(p)
    # In an RTL paragraph Word mirrors alignment: LEFT means the "start" (right) side.
    p.alignment = {"right": WD_ALIGN_PARAGRAPH.LEFT,
                   "center": WD_ALIGN_PARAGRAPH.CENTER}[align]
    pf = p.paragraph_format
    pf.space_before, pf.space_after = Pt(before), Pt(after)
    pf.line_spacing = 1.25
    if indent:
        pf.left_indent = Cm(indent)   # mirrored: this is the right-hand indent
    pf.keep_with_next = keep_next
    return p


def add_inline(p, text, size, bold=False, italic=False, color=None):
    """Add text with *italic* / **bold** markdown spans."""
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            style_run(p.add_run(part[2:-2]), size, True, italic, color)
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            style_run(p.add_run(part[1:-1]), size, bold, True, color)
        else:
            style_run(p.add_run(part), size, bold, italic, color)


def add_lines(p, lines, size, **kw):
    for i, line in enumerate(lines):
        if i:
            p.add_run().add_break(WD_BREAK.LINE)
        add_inline(p, line, size, **kw)


def page_break():
    p = doc.add_paragraph()
    p.add_run().add_break(WD_BREAK.PAGE)


def heading(text, level, size, before=18, after=10):
    p = new_par("center", before, after, keep_next=True, style=f"Heading {level}")
    style_run(p.add_run(text), size, bold=True, color=RGBColor(0, 0, 0))
    return p


def direction(text):
    text = text.strip()
    if text.startswith("*") and text.endswith("*"):
        text = text[1:-1]
    p = new_par("right", 2, 6, indent=1.0)
    add_inline(p, text, 11, italic=True, color=GREY)


def cue(lines):
    lines = list(lines)
    lines[0] = re.sub(r"^\*\*\[", "", lines[0])
    lines[-1] = re.sub(r"\*{0,2}\]\*{0,2}$", "", lines[-1])
    cleaned = []
    for i, ln in enumerate(lines):
        ln = ln.strip()
        if i == 0:
            # the first line is bold up to its closing ** (or entirely)
            ln = ln.rstrip("*")
            cleaned.append(("head", ln))
        else:
            cleaned.append(("line", ln.rstrip("*") if ln.endswith("**") and ln.count("**") % 2 else ln))
    p = new_par("right", 6, 10, indent=1.0)
    pPr = p._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    for side in ("left", "right"):
        if side == "right":
            el = OxmlElement("w:right")
            el.set(qn("w:val"), "single"); el.set(qn("w:sz"), "12")
            el.set(qn("w:space"), "8"); el.set(qn("w:color"), "888888")
            bdr.append(el)
    pPr.append(bdr)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), "F2F2F2")
    pPr.append(shd)
    for i, (kind, ln) in enumerate(cleaned):
        if i:
            p.add_run().add_break(WD_BREAK.LINE)
        if kind == "head":
            add_inline(p, ln.replace("**", ""), 10.5, bold=True)
        else:
            add_inline(p, ln, 10.5)


def note(lines):
    text = " ".join(l.lstrip("> ").strip() for l in lines)
    p = new_par("right", 4, 8)
    add_inline(p, text.replace("`", ""), 9.5, italic=True, color=GREY)


def render_block(lines, state):
    first = lines[0]
    if first.startswith("**[") or first.startswith("*["):
        cue(lines); return
    if first.startswith(">"):
        note(lines); return
    if re.fullmatch(r"\*\*(סוף.*|הפסקה)\*\*", first.strip()) or first.strip() == "*הפסקה*":
        p = new_par("center", 24, 12)
        style_run(p.add_run(first.strip().strip("*")), 14, bold=True)
        return
    buf = []

    def flush():
        if buf:
            p = new_par("right", 0, 8, indent=0.5)
            add_lines(p, buf, 12)
            buf.clear()

    for ln in lines:
        s = ln.strip()
        m = re.fullmatch(r"\*\*([^*\[\]]+)\*\*", s)
        if m:                                   # speaker name
            flush()
            p = new_par("right", 8, 1, keep_next=True)
            style_run(p.add_run(m.group(1)), 12, bold=True)
        elif s.startswith("*") and s.endswith("*") and not s.startswith("**"):
            flush(); direction(s)               # stage direction
        else:
            buf.append(s)
    flush()


def title_page(blocks):
    p = new_par("center", 140, 18)
    style_run(p.add_run("מזמור לדוד"), 40, bold=True)
    for b in blocks:
        if b[0].startswith(">"):
            p = new_par("center", 60, 0)
            txt = " ".join(l.lstrip("> ").strip() for l in b)
            txt = re.sub(r"\s*מראי המקום וההערות — ב-`[^`]*`\.", "", txt)
            add_inline(p, txt.replace("`", ""), 9.5, italic=True, color=GREY)
        else:
            for ln in b:
                p = new_par("center", 4, 4)
                add_inline(p, re.sub(r"\s*\(`[^`]*`\)", "", ln).replace("`", ""), 14)


def build():
    first_file = True
    for src in SOURCES:
        text = src.read_text(encoding="utf-8")
        blocks = [b.split("\n") for b in re.split(r"\n\s*\n", text.strip())]
        i = 0
        if first_file:
            # everything before the first '---' is front matter
            front = []
            while blocks[i][0].strip() != "---":
                front.append(blocks[i]); i += 1
            title_page([b for b in front if not b[0].startswith("# ")])
        state = {}
        while i < len(blocks):
            b = blocks[i]; i += 1
            head = b[0].strip()
            if head == "---":
                continue
            if head.startswith("# "):
                title = head[2:].strip()
                if title == "מזמור לדוד":
                    continue
                page_break()
                heading(title, 1, 26, before=120, after=8)
                continue
            if head.startswith("## "):
                title = head[3:].strip()
                if title.startswith("תמונה"):
                    heading(title, 2, 16, before=26, after=10)
                else:
                    p = new_par("center", 0, 30)
                    style_run(p.add_run(title), 16, italic=True)
                    for extra in b[1:]:
                        pass
                continue
            render_block(b, state)
        first_file = False

    # page numbers
    footer = doc.sections[0].footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer.add_run()
    for kind, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), kind)
        else:
            el = OxmlElement("w:instrText"); el.set(qn("xml:space"), "preserve"); el.text = txt
        run._r.append(el)

    OUT.parent.mkdir(exist_ok=True)
    doc.save(OUT)
    print("saved", OUT)


if __name__ == "__main__":
    build()
