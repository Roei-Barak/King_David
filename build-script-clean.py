#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
מחלץ מלל נקי מהמחזה — דיאלוג + שירים בלבד, ללא הוראות במאי.
"""
import re
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path("/home/user/King_David")
SCENES_DIR = ROOT / "scenes"
FONT = "Arial"

SCENE_ORDER = [
    "scene-01-05-full.md",
    "scene-jonathan-farewell.md",
    "scene-gath-madness.md",
    "scene-nob-massacre.md",
    "scene-04-the-cave.md",
    "scene-04b-wilderness-additions.md",
    "scene-cave-hill.md",
    "scene-nabal-abigail.md",
    "scene-05b-witch-endor.md",
    "scene-ziklag.md",
    "scene-philistines-reject.md",
    "scene-gilboa.md",
    "scene-06-lament.md",
    "scene-07-brothers-war.md",
    "scene-ishbosheth.md",
    "scene-jerusalem.md",
    "scene-08-dance.md",
    "scene-09-not-you.md",
    "scene-chr25-singers.md",
    "scene-10-mephibosheth.md",
    "scene-10b-ammon-war.md",
    "scene-bathsheba-uriah.md",
    "scene-bathhouse.md",
    "scene-13b-amnon-tamar.md",
    "scene-13e-absalom-return.md",
    "scene-13c-revolt.md",
    "scene-13d-absalom.md",
    "scene-13f-david-return.md",
    "scene-13g-rizpah.md",
    "scene-water-libation.md",
    "scene-14-hallelujah.md",
    "scene-22-23-david-song.md",
    "scene-15-testament.md",
    "scene-tzruya-david.md",
]

# ---- helpers ----

def is_stage_direction(line):
    """שורה שהיא רק הוראת במאי — לא מלל"""
    s = line.strip()
    # שורה שכולה *(...)*
    if re.match(r'^\*\([^)]*\)\*\.?\s*$', s):
        return True
    # הערות > שהן לא שירה (מזוהות בהמשך בנפרד)
    return False

def clean_inline(text):
    """מסיר *(...)* inline, **bold**, [לאמת...], [מ-...] אבל שומר טקסט"""
    # הסר הוראות במאי inline: *(...)*
    text = re.sub(r'\s*\*\([^)]*\)\*', '', text)
    # הסר [לאמת...] ו[מ-...]
    text = re.sub(r'\[[^\]]*\]', '', text)
    # הסר bold markers
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    # הסר single * italic
    text = re.sub(r'(?<!\*)\*(?!\*)([^*]+)(?<!\*)\*(?!\*)', r'\1', text)
    # הסר backtick
    text = re.sub(r'`([^`]+)`', r'\1', text)
    return text.strip()

def extract_speaker_line(line):
    """
    מחלץ שם דובר ותוכן מ: **שם** [*(תנועה)*]: "טקסט"
    מחזיר (speaker, content) או None
    """
    # **SPEAKER** *(opt)*: content
    m = re.match(r'^\*\*([^*]+)\*\*\s*(?:\*\([^)]*\)\*)?\s*[:：]\s*(.*)', line)
    if m:
        speaker = m.group(1).strip()
        content = m.group(2).strip()
        # נקה מ content הוראות במאי inline
        content = clean_inline(content)
        return speaker, content
    return None

def is_song_line(line):
    """שורת שיר — מתחילה ב-> ואינה הוראת במאי"""
    s = line.strip()
    if s.startswith('>'):
        inner = s[1:].strip()
        # הוראת במאי בתוך ציטוט
        if re.match(r'^\*\([^)]*\)\*\s*$', inner):
            return False
        return True
    return False

def is_heading(line):
    return re.match(r'^#{1,6}\s+', line)

def skip_heading(line):
    """כותרות מטא שאינן שמות סצנות"""
    s = line.strip()
    # טבלאות סיכום, מקורות, מבנה, הוראות
    for pat in ['סיכום', 'מקורות', 'מבנה', 'הוראות', 'שכבה', 'תפקיד', 'טבלה',
                'דרמטי', 'מחזמר', 'ז\'אנר', 'ז"אנר', 'מוזיקה', 'תאורה',
                'composer', 'brief', 'director', 'notes']:
        if pat.lower() in s.lower():
            return True
    return False

def should_skip_block(line):
    """האם זו שורה שצריך לדלג עליה לגמרי"""
    s = line.strip()
    if not s:
        return False
    # טבלאות markdown
    if s.startswith('|'):
        return True
    # bullet lists שהן הוראות
    if re.match(r'^[-*+]\s+', s) and not re.match(r'^\*\*[^*]+\*\*', s):
        return True
    # שורות קוד
    if s.startswith('```'):
        return True
    # שורה שהיא הוראת במאי טהורה
    if re.match(r'^\*\([^)]*\)\*\.?\s*$', s):
        return True
    # הוראות במאי בנטייה
    if re.match(r'^\*[^*].*\*\s*$', s) and not re.match(r'^\*\*', s):
        return True
    return False

# ---- document setup ----

doc = Document()
for s in doc.sections:
    s.top_margin = Inches(1.0); s.bottom_margin = Inches(1.0)
    s.left_margin = Inches(1.2); s.right_margin = Inches(1.2)

style = doc.styles["Normal"]
style.font.name = FONT
style.font.size = Pt(11)
style._element.rPr.rFonts.set(qn("w:cs"), FONT)
style.paragraph_format.space_after = Pt(0)

def set_rtl(p):
    pPr = p._p.get_or_add_pPr()
    pPr.append(OxmlElement("w:bidi"))
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

def add_par(text, size=11, bold=False, italic=False, color=None,
            center=False, sb=0, sa=3, indent=0.0):
    if not text or not text.strip():
        return
    p = doc.add_paragraph(); set_rtl(p)
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(sb)
    p.paragraph_format.space_after = Pt(sa)
    p.paragraph_format.line_spacing = Pt(size * 1.5)
    if indent:
        p.paragraph_format.left_indent = Inches(indent)
    run = p.add_run(text)
    run.font.size = Pt(size); run.bold = bold; run.italic = italic
    run.font.name = FONT
    run.font._element.rPr.rFonts.set(qn("w:cs"), FONT)
    if color:
        run.font.color.rgb = color
    return p

def add_dialogue(speaker, content):
    """שורת דיאלוג: **שם** — תוכן"""
    if not content:
        return
    p = doc.add_paragraph(); set_rtl(p)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = Pt(11 * 1.5)
    # שם הדובר
    r1 = p.add_run(speaker + ": ")
    r1.bold = True; r1.font.size = Pt(11)
    r1.font.name = FONT; r1.font._element.rPr.rFonts.set(qn("w:cs"), FONT)
    r1.font.color.rgb = RGBColor(0x22, 0x22, 0x66)
    # תוכן
    r2 = p.add_run(content)
    r2.font.size = Pt(11)
    r2.font.name = FONT; r2.font._element.rPr.rFonts.set(qn("w:cs"), FONT)

def add_song_line(text):
    add_par(text, size=11, italic=True, center=True, sa=1,
            color=RGBColor(0x2a, 0x2a, 0x55))

# ---- title page ----

for _ in range(4): doc.add_paragraph()
add_par("מִזְמוֹר לְדָוִד", size=36, bold=True, center=True, sa=10)
add_par("מחזמר — מלל נקי", size=16, italic=True, center=True, sa=6)
add_par("דיאלוג ושירים בלבד", size=12, center=True,
        color=RGBColor(0x66, 0x66, 0x66))
doc.add_page_break()

# ---- parse and render ----

def render_scene(path):
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")

    in_code_block = False
    in_table_block = False
    skip_meta = False   # דילוג על כותרת-מטא וה"גוף" שלה
    song_buf = []

    def flush_song():
        nonlocal song_buf
        if song_buf:
            doc.add_paragraph()
            for sl in song_buf:
                add_song_line(sl)
            doc.add_paragraph()
        song_buf = []

    for raw in lines:
        line = raw.rstrip()

        # בלוק קוד
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # שורה ריקה
        if not line.strip():
            flush_song()
            continue

        # כותרות
        hm = is_heading(line)
        if hm:
            flush_song()
            level = len(re.match(r'^(#+)', line).group(1))
            htitle = re.sub(r'^#+\s*', '', line).strip()
            htitle = clean_inline(htitle)

            if skip_heading(line):
                skip_meta = True
                continue

            skip_meta = False

            if level == 1:
                doc.add_page_break()
                add_par(htitle, size=18, bold=True, center=True, sb=12, sa=10)
            elif level == 2:
                add_par(htitle, size=13, bold=True, sb=8, sa=4,
                        color=RGBColor(0x33, 0x33, 0x66))
            else:
                add_par(htitle, size=11, bold=True, sb=5, sa=2,
                        color=RGBColor(0x55, 0x55, 0x55))
            continue

        if skip_meta:
            continue

        # טבלאות
        if line.strip().startswith('|'):
            continue

        # הוראות במאי / bullet meta
        if should_skip_block(line):
            continue

        # מפריד
        if re.match(r'^\s*(---+|\*\s*\*\s*\*|⸻)\s*$', line):
            flush_song()
            add_par("— — —", center=True, size=10,
                    color=RGBColor(0xbb, 0xbb, 0xbb), sb=4, sa=4)
            continue

        # שורת שיר (ציטוט >)
        if is_song_line(line):
            inner = line.strip()[1:].strip()
            inner = clean_inline(inner)
            if inner:
                song_buf.append(inner)
            continue

        # דיאלוג
        result = extract_speaker_line(line)
        if result:
            flush_song()
            speaker, content = result
            if content:
                add_dialogue(speaker, content)
            # המשך שורות תוכן (שורות נוספות ב"") — יטופלו בלולאה
            continue

        # שורה נוספת אחרי דיאלוג (המשך ציטוט ב"")
        # שורות שמתחילות ב-" ואינן הוראה
        if line.strip().startswith('"') or line.strip().startswith('״'):
            flush_song()
            content = clean_inline(line.strip())
            if content:
                add_par(content, indent=0.3, sb=0, sa=1)
            continue

        # כל שאר — מדלגים (הוראות, מטא, פסקאות רקע)
        continue

    flush_song()

# ---- עבד סצנות ----

processed = set()
for fname in SCENE_ORDER:
    fpath = SCENES_DIR / fname
    if not fpath.exists():
        print(f"  חסר: {fname}")
        continue
    print(f"  + {fname}")
    render_scene(fpath)
    processed.add(fname)

# סצנות שלא ברשימה
extras = sorted(SCENES_DIR.glob("scene-*.md"))
for f in extras:
    if f.name not in processed and f.name not in ("scene-midrashim.md", "new-scenes.md"):
        print(f"  + (extra) {f.name}")
        render_scene(f)

out = ROOT / "מזמור-לדוד-מלל-נקי.docx"
doc.save(out)
print(f"\nנשמר: {out}")
print(f"פסקאות: {len(doc.paragraphs)}")
