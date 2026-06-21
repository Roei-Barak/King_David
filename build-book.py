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

# סדר הספר — לפי outline/master-version-ab.md, עם הרחבות בסדר מקראי
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
    (None, None, "scene-bathhouse.md"),
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

doc = Document()

# סגנון בסיס — גופן עברי, RTL
style = doc.styles["Normal"]
style.font.name = "David"
style.font.size = Pt(12)
style._element.rPr.rFonts.set(qn("w:cs"), "David")

def set_rtl(p):
    pPr = p._p.get_or_add_pPr()
    bidi = OxmlElement("w:bidi")
    pPr.append(bidi)
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

def add_par(text, size=12, bold=False, italic=False, color=None, align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=6):
    p = doc.add_paragraph()
    set_rtl(p)
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.name = "David"
    run.font._element.rPr.rFonts.set(qn("w:cs"), "David")
    if color:
        run.font.color.rgb = color
    return p

# --- עמוד שער ---
for _ in range(6):
    doc.add_paragraph()
add_par("מִזְמוֹר לְדָוִד", size=40, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
add_par("הַצַּדִּיק שֶׁכּוֹתֵב שִׁירִים", size=20, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)
add_par("מחזמר במה על חיי דוד המלך", size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
add_par("טיוטה לקריאה והערות", size=12, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, color=RGBColor(0x80,0x80,0x80))
doc.add_page_break()

# --- הערת קריאה ---
add_par("לקורא", size=18, bold=True, space_after=10)
add_par("מסמך זה מאחד את כל הסצנות של המחזמר בסדר קריאה רציף, כספר. הסדר נקבע לפי המתווה המאוחד (outline/master-version-ab.md).", space_after=6)
add_par("שלוש השפות במחזה: דיאלוג = פרוזה מליצית מקראית · מונולוג פנימי = שיר חופשי על דרך תהילים · שיר מוזיקלי = חרוז ומטר קבועים.", space_after=6)
add_par("סימון [להכריע: רסיטטיב/פזמון] מציין מקום שבו טקסט מולחן הוא פסוק תהילים גולמי — וטרם הוכרע אם להלחינו כרסיטטיב או לעבדו לפזמון.", space_after=6)
add_par("הערות בסוגריים נטויים *(כך)* הן הוראות במאי. ציטוטים מקראיים מסומנים *(ספר פרק, פסוק)*.", space_after=6)
doc.add_page_break()

# --- עיבוד markdown לפסקאות Word ---
def render_md(text):
    lines = text.split("\n")
    in_code = False
    for raw in lines:
        line = raw.rstrip()
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not line.strip():
            continue
        # טבלאות markdown — מדלגים על שורת המפריד, מנקים את צינורות
        if re.match(r"^\s*\|[-\s:|]+\|\s*$", line):
            continue
        # כותרות
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            txt = clean_inline(m.group(2))
            size = {1:22,2:18,3:15,4:13,5:12,6:12}.get(level,12)
            add_par(txt, size=size, bold=True, space_after=8 if level<=2 else 4)
            continue
        # ציטוט/בלוק
        if line.strip().startswith(">"):
            txt = clean_inline(line.strip()[1:].strip())
            add_par(txt, italic=True, color=RGBColor(0x55,0x55,0x55), space_after=4)
            continue
        # שורת טבלה — הופכים לטקסט מופרד
        if line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            txt = "  —  ".join(c for c in cells if c)
            add_par(clean_inline(txt), size=11, space_after=2)
            continue
        # רשימה
        if re.match(r"^\s*[-*]\s+", line):
            txt = clean_inline(re.sub(r"^\s*[-*]\s+","",line))
            p = add_par("•  " + txt, space_after=2)
            continue
        # מפריד
        if re.match(r"^\s*---+\s*$", line):
            add_par("⸻", align=WD_ALIGN_PARAGRAPH.CENTER, color=RGBColor(0xAA,0xAA,0xAA), space_after=4)
            continue
        # רגיל
        add_par(clean_inline(line), space_after=4)

def clean_inline(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)   # bold
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", s)  # italic
    s = re.sub(r"`(.+?)`", r"\1", s)
    return s

# --- בניית הספר ---
for part, title, fname in BOOK:
    if fname is None:
        doc.add_page_break()
        add_par(part, size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, color=RGBColor(0x33,0x33,0x33), space_after=6)
        add_par(title, size=24, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
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
