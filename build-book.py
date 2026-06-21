#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""בונה מסמך Word אחד מכל הסצנות, מסודר כספר לקריאה והערות."""
import re
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path("/home/user/King_David")
SCENES = ROOT / "scenes"

BOOK = [
    ("חלק א'", "מַעֲרָכָה א — מִן הָרוֹעֶה לַמֶּלֶךְ", None),
    (None, None, "prologue.md"),
    (None, None, "scene-01-05-full.md"),
    ("הרחבות", "הרחבות המדבר (תמונה 4) — לפי סדר מקראי", None),
    (None, None, "scene-jonathan-farewell.md"),
    (None, None, "scene-gath-madness.md"),
    (None, None, "scene-nob-massacre.md"),
    (None, None, "scene-04-the-cave.md"),
    (None, None, "scene-04b-wilderness-additions.md"),
    (None, None, "scene-nabal-abigail.md"),
    (None, None, "scene-cave-hill.md"),
    (None, None, "scene-05b-witch-endor.md"),
    (None, None, "scene-ziklag.md"),
    (None, None, "scene-philistines-reject.md"),
    (None, None, "scene-gilboa.md"),
    ("חלק ב'", "מַעֲרָכָה ב — הַמֶּלֶךְ", None),
    (None, None, "scene-06-lament.md"),
    (None, None, "scene-07-brothers-war.md"),
    (None, None, "scene-08-dance.md"),
    (None, None, "scene-09-not-you.md"),
    (None, None, "scene-chr25-singers.md"),
    (None, None, "scene-10-mephibosheth.md"),
    (None, None, "scene-10b-ammon-war.md"),
    (None, None, "scene-bathsheba-uriah.md"),
    (None, None, "bathhouse.md"),
    (None, None, "scene-13b-amnon-tamar.md"),
    (None, None, "scene-13e-absalom-return.md"),
    (None, None, "scene-13c-revolt.md"),
    (None, None, "scene-13d-absalom.md"),
    (None, None, "scene-13f-david-return.md"),
    (None, None, "scene-13g-rizpah.md"),
    (None, None, "scene-water-libation.md"),
    (None, None, "scene-14-hallelujah.md"),
    (None, None, "scene-22-23-david-song.md"),
    (None, None, "scene-15-testament.md"),
    ("נספח", "נספח — תת-עלילות", None),
    (None, None, "scene-tzruya-david.md"),
]

FONT = "Arial"

doc = Document()

# שוליים צרים יותר
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.1)
    section.right_margin = Inches(1.1)

# סגנון בסיס — Arial, RTL
style = doc.styles["Normal"]
style.font.name = FONT
style.font.size = Pt(11)
style._element.rPr.rFonts.set(qn("w:cs"), FONT)
style.paragraph_format.space_before = Pt(0)
style.paragraph_format.space_after = Pt(3)

def set_rtl(p):
    pPr = p._p.get_or_add_pPr()
    # bidi — כיוון RTL לפסקה
    bidi = OxmlElement("w:bidi")
    pPr.append(bidi)
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

def add_par(text, size=11, bold=False, italic=False, color=None,
            align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=3, line_spacing=1.15):
    p = doc.add_paragraph()
    set_rtl(p)
    p.alignment = align
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = Pt(size * line_spacing * 1.3)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.name = FONT
    run.font._element.rPr.rFonts.set(qn("w:cs"), FONT)
    if color:
        run.font.color.rgb = color
    return p

# --- עמוד שער ---
for _ in range(3):
    doc.add_paragraph()
add_par("מִזְמוֹר לְדָוִד", size=36, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
add_par("הַצַּדִּיק שֶׁכּוֹתֵב שִׁירִים", size=18, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=16)
add_par("מחזמר במה על חיי דוד המלך", size=13, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
add_par("טיוטה לקריאה והערות", size=11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, color=RGBColor(0x80,0x80,0x80))
doc.add_page_break()

# --- הערת קריאה ---
add_par("לקורא", size=16, bold=True, space_after=6)
add_par("מסמך זה מאחד את כל הסצנות של המחזמר בסדר קריאה רציף, כספר.", space_after=3)
add_par("שלוש השפות: דיאלוג = פרוזה מליצית מקראית · מונולוג פנימי = שיר חופשי על דרך תהילים · שיר מוזיקלי = חרוז ומטר קבועים.", space_after=3)
add_par("סימון [להכריע: רסיטטיב/פזמון] — מקום שטרם הוכרע אם להלחינו כרסיטטיב או לעבדו לפזמון.", space_after=3)
add_par("הערות *(כך)* הן הוראות במאי. ציטוטים מקראיים מסומנים *(ספר פרק, פסוק)*.", space_after=3)
doc.add_page_break()

# --- עיבוד markdown לפסקאות Word ---
def render_md(text):
    lines = text.split("\n")
    in_code = False
    prev_empty = False
    for raw in lines:
        line = raw.rstrip()
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        # שורה ריקה — מדלגים על רצפים של שורות ריקות
        if not line.strip():
            if not prev_empty:
                prev_empty = True
            continue
        prev_empty = False
        if re.match(r"^\s*\|[-\s:|]+\|\s*$", line):
            continue
        # כותרות
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            txt = clean_inline(m.group(2))
            size = {1:18,2:15,3:13,4:12,5:11,6:11}.get(level,11)
            sa = 5 if level <= 2 else 3
            add_par(txt, size=size, bold=True, space_after=sa)
            continue
        # ציטוט/בלוק
        if line.strip().startswith(">"):
            txt = clean_inline(line.strip()[1:].strip())
            add_par(txt, italic=True, color=RGBColor(0x55,0x55,0x55), space_after=2)
            continue
        # שורת טבלה
        if line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            txt = "  —  ".join(c for c in cells if c)
            add_par(clean_inline(txt), size=10, space_after=2)
            continue
        # רשימה
        if re.match(r"^\s*[-*]\s+", line):
            txt = clean_inline(re.sub(r"^\s*[-*]\s+","",line))
            add_par("•  " + txt, space_after=2)
            continue
        # מפריד
        if re.match(r"^\s*---+\s*$", line):
            add_par("⸻", align=WD_ALIGN_PARAGRAPH.CENTER, color=RGBColor(0xAA,0xAA,0xAA), space_after=3)
            continue
        # רגיל
        add_par(clean_inline(line), space_after=3)

def clean_inline(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", s)
    s = re.sub(r"`(.+?)`", r"\1", s)
    return s

# --- בניית הספר ---
for part, title, fname in BOOK:
    if fname is None:
        doc.add_page_break()
        add_par(part, size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER,
                color=RGBColor(0x55,0x55,0x55), space_after=4)
        add_par(title, size=20, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
        continue
    fpath = SCENES / fname
    if not fpath.exists():
        continue
    doc.add_page_break()
    render_md(fpath.read_text(encoding="utf-8"))

out = ROOT / "מזמור-לדוד-ספר-לקריאה.docx"
doc.save(out)
print(f"נשמר: {out}")
print(f"מספר פסקאות: {len(doc.paragraphs)}")
