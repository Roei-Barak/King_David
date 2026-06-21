#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""בונה קובץ HTML יחיד עם כל המחזמר — לקריאה, הערות ואינטראקציה."""
import re, json
from pathlib import Path

ROOT = Path("/home/user/King_David")
SCENES = ROOT / "scenes"

BOOK = [
    ("חלק א'", "מַעֲרָכָה א — מִן הָרוֹעֶה לַמֶּלֶךְ", None, None),
    (None, None, "prologue.md", "פרולוג"),
    (None, None, "scene-01-05-full.md", "תמונות א–ה: מהרועה למלך"),
    ("הרחבות", "הרחבות המדבר — לפי סדר מקראי", None, None),
    (None, None, "scene-jonathan-farewell.md", "פרידת יונתן"),
    (None, None, "scene-gath-madness.md", "שיגעון גת"),
    (None, None, "scene-nob-massacre.md", "טבח נוב"),
    (None, None, "scene-04-the-cave.md", "המערה"),
    (None, None, "scene-04b-wilderness-additions.md", "הרחבות המדבר"),
    (None, None, "scene-nabal-abigail.md", "נבל ואביגיל"),
    (None, None, "scene-cave-hill.md", "המערה והגבעה"),
    (None, None, "scene-05b-witch-endor.md", "אוב עין-דור"),
    (None, None, "scene-ziklag.md", "צקלג"),
    (None, None, "scene-philistines-reject.md", "פלשתים דוחים"),
    (None, None, "scene-gilboa.md", "גלבוע"),
    ("חלק ב'", "מַעֲרָכָה ב — הַמֶּלֶךְ", None, None),
    (None, None, "scene-06-lament.md", "הקינה"),
    (None, None, "scene-07-brothers-war.md", "מלחמת האחים"),
    (None, None, "scene-08-dance.md", "הריקוד"),
    (None, None, "scene-09-not-you.md", "לא אתה"),
    (None, None, "scene-chr25-singers.md", "288 המשוררים"),
    (None, None, "scene-10-mephibosheth.md", "מפיבושת"),
    (None, None, "scene-10b-ammon-war.md", "מלחמת עמון"),
    (None, None, "scene-bathsheba-uriah.md", "בת-שבע ואוריה"),
    (None, None, "bathhouse.md", "בית המרחץ"),
    (None, None, "scene-13b-amnon-tamar.md", "אמנון ותמר"),
    (None, None, "scene-13e-absalom-return.md", "שיבת אבשלום"),
    (None, None, "scene-13c-revolt.md", "המרד"),
    (None, None, "scene-13d-absalom.md", "מות אבשלום"),
    (None, None, "scene-13f-david-return.md", "שיבת דוד"),
    (None, None, "scene-13g-rizpah.md", "רצפה"),
    (None, None, "scene-water-libation.md", "ניסוך המים"),
    (None, None, "scene-14-hallelujah.md", "הללויה"),
    (None, None, "scene-22-23-david-song.md", "שיר דוד"),
    (None, None, "scene-15-testament.md", "הצוואה"),
    ("נספח", "נספח — תת-עלילות", None, None),
    (None, None, "scene-tzruya-david.md", "צרויה ודוד"),
]

CHARACTERS = {
    "דוד": {"color": "#2563eb", "scenes": []},
    "שאול": {"color": "#dc2626", "scenes": []},
    "יונתן": {"color": "#16a34a", "scenes": []},
    "מיכל": {"color": "#9333ea", "scenes": []},
    "יואב": {"color": "#92400e", "scenes": []},
    "אביגיל": {"color": "#ea580c", "scenes": []},
    "בת-שבע": {"color": "#0891b2", "scenes": []},
    "נתן": {"color": "#4338ca", "scenes": []},
    "אבשלום": {"color": "#be123c", "scenes": []},
    "אמנון": {"color": "#854d0e", "scenes": []},
    "תמר": {"color": "#86198f", "scenes": []},
    "מפיבושת": {"color": "#065f46", "scenes": []},
    "שמואל": {"color": "#1e3a5f", "scenes": []},
    "אוריה": {"color": "#374151", "scenes": []},
    "רצפה": {"color": "#be185d", "scenes": []},
}

def md_to_html(text):
    lines = text.split("\n")
    out = []
    in_code = False
    for raw in lines:
        line = raw.rstrip()
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not line.strip():
            out.append('<div class="spacer"></div>')
            continue
        if re.match(r"^\s*\|[-\s:|]+\|\s*$", line):
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            txt = inline_md(m.group(2))
            tag = f"h{min(level+1,6)}"
            out.append(f'<{tag} class="md-h{level}">{txt}</{tag}>')
            continue
        if line.strip().startswith(">"):
            txt = inline_md(line.strip()[1:].strip())
            out.append(f'<blockquote class="md-blockquote">{txt}</blockquote>')
            continue
        if re.match(r"^\s*\|", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            row = " &nbsp;—&nbsp; ".join(f"<span>{inline_md(c)}</span>" for c in cells if c)
            out.append(f'<p class="md-table-row">{row}</p>')
            continue
        if re.match(r"^\s*[-*]\s+", line):
            txt = inline_md(re.sub(r"^\s*[-*]\s+","",line))
            out.append(f'<li class="md-li">{txt}</li>')
            continue
        if re.match(r"^\s*---+\s*$", line):
            out.append('<hr class="md-hr">')
            continue
        out.append(f'<p class="md-p">{inline_md(line)}</p>')
    return "\n".join(out)

def inline_md(s):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s

# Build scene data
scenes_data = []
scene_index = 0
current_part = None

for part, title, fname, label in BOOK:
    if fname is None:
        current_part = part or title
        continue
    fpath = SCENES / fname
    if not fpath.exists():
        continue
    content = fpath.read_text(encoding="utf-8")
    html = md_to_html(content)
    chars_in_scene = [c for c in CHARACTERS if c in content]
    sid = f"scene-{scene_index}"
    scenes_data.append({
        "id": sid,
        "fname": fname,
        "label": label,
        "part": current_part,
        "html": html,
        "chars": chars_in_scene,
        "raw": content[:500],
    })
    for c in chars_in_scene:
        CHARACTERS[c]["scenes"].append(sid)
    scene_index += 1

scenes_json = json.dumps([{
    "id": s["id"], "label": s["label"], "part": s["part"],
    "chars": s["chars"], "preview": s["raw"][:200].replace('"', '\\"').replace('\n', ' ')
} for s in scenes_data], ensure_ascii=False)

chars_json = json.dumps(CHARACTERS, ensure_ascii=False)

html_parts = []
for s in scenes_data:
    chars_attr = " ".join(s["chars"])
    html_parts.append(f'''
<article id="{s["id"]}" class="scene-article" data-chars="{chars_attr}" data-part="{s["part"] or ''}" data-label="{s["label"]}">
  <div class="scene-header">
    <h2 class="scene-title">{s["label"]}</h2>
    <div class="scene-meta">
      <span class="scene-part-badge">{s["part"] or ''}</span>
      <div class="char-chips">{' '.join(f'<span class="char-chip" style="background:{CHARACTERS[c]["color"]}22;color:{CHARACTERS[c]["color"]};border-color:{CHARACTERS[c]["color"]}40">{c}</span>' for c in s["chars"])}</div>
    </div>
    <div class="scene-actions">
      <button class="btn-icon" onclick="printScene('{s["id"]}')" title="הדפס סצנה">🖨</button>
      <button class="btn-icon" onclick="toggleAnnotation('{s["id"]}')" title="הוסף הערה">✏️</button>
    </div>
  </div>
  <div class="scene-content" dir="rtl">{s["html"]}</div>
  <div class="annotation-box" id="ann-{s["id"]}" style="display:none">
    <div class="annotation-label">הערות והצעות לסצנה זו:</div>
    <textarea class="annotation-textarea" id="textarea-{s["id"]}"
      oninput="saveAnnotation('{s["id"]}')"
      placeholder="כתבו כאן את הערותיכם, הצעות לשינוי, שאלות למחבר..."></textarea>
    <div class="annotation-saved" id="saved-{s["id"]}"></div>
  </div>
</article>''')

all_scenes_html = "\n".join(html_parts)

HTML = f'''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>מזמור לדוד — המחזמר המלא</title>
<style>
:root {{
  --bg: #fafaf8;
  --bg2: #f0ede6;
  --bg3: #e8e4dc;
  --fg: #1a1612;
  --fg2: #4a4540;
  --fg3: #7a7570;
  --accent: #8b2500;
  --accent2: #c44a00;
  --border: #d4cfc8;
  --sidebar-w: 280px;
  --font-body: "David", "Times New Roman", serif;
  --font-ui: "Segoe UI", "Arial Hebrew", Arial, sans-serif;
}}
[data-theme="dark"] {{
  --bg: #18160f;
  --bg2: #22201a;
  --bg3: #2c2922;
  --fg: #f0ede6;
  --fg2: #c0bdb6;
  --fg3: #8a8780;
  --accent: #e08060;
  --accent2: #f0a080;
  --border: #3a3730;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: var(--font-body);
  background: var(--bg);
  color: var(--fg);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}}

/* ── TOP BAR ── */
#topbar {{
  position: sticky; top: 0; z-index: 100;
  background: var(--accent);
  color: #fff;
  display: flex; align-items: center; gap: 12px;
  padding: 8px 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,.3);
}}
#topbar h1 {{ font-size: 1.1rem; font-weight: bold; flex: 1; }}
.topbar-btn {{
  background: rgba(255,255,255,.15);
  border: 1px solid rgba(255,255,255,.3);
  color: #fff;
  padding: 5px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-family: var(--font-ui);
  font-size: .85rem;
  white-space: nowrap;
}}
.topbar-btn:hover {{ background: rgba(255,255,255,.25); }}
#search-input {{
  background: rgba(255,255,255,.15);
  border: 1px solid rgba(255,255,255,.3);
  color: #fff;
  padding: 5px 10px;
  border-radius: 6px;
  font-family: var(--font-body);
  font-size: .9rem;
  width: 180px;
}}
#search-input::placeholder {{ color: rgba(255,255,255,.6); }}
#search-input:focus {{ outline: none; background: rgba(255,255,255,.25); }}

/* ── LAYOUT ── */
#layout {{ display: flex; flex: 1; overflow: hidden; height: calc(100vh - 45px); }}

/* ── SIDEBAR ── */
#sidebar {{
  width: var(--sidebar-w);
  background: var(--bg2);
  border-left: 1px solid var(--border);
  overflow-y: auto;
  flex-shrink: 0;
  padding: 8px 0;
}}
.sidebar-section {{
  padding: 6px 12px 2px;
  font-size: .7rem;
  font-family: var(--font-ui);
  color: var(--fg3);
  text-transform: uppercase;
  letter-spacing: .05em;
  margin-top: 8px;
}}
.sidebar-item {{
  display: block;
  padding: 5px 16px;
  font-size: .88rem;
  color: var(--fg2);
  cursor: pointer;
  border-right: 3px solid transparent;
  transition: all .15s;
  font-family: var(--font-body);
}}
.sidebar-item:hover {{ background: var(--bg3); color: var(--fg); }}
.sidebar-item.active {{
  background: var(--bg3);
  color: var(--accent);
  border-right-color: var(--accent);
  font-weight: bold;
}}
.sidebar-divider {{
  height: 1px; background: var(--border);
  margin: 8px 12px;
}}
.sidebar-special {{
  display: block;
  padding: 6px 16px;
  font-size: .85rem;
  color: var(--accent);
  cursor: pointer;
  font-family: var(--font-ui);
}}
.sidebar-special:hover {{ background: var(--bg3); }}

/* ── MAIN ── */
#main {{
  flex: 1;
  overflow-y: auto;
  padding: 0;
}}

/* ── VIEWS ── */
.view {{ display: none; }}
.view.active {{ display: block; }}

/* ── SCENES VIEW ── */
#view-scenes {{ padding: 24px 32px; max-width: 860px; margin: 0 auto; }}

.scene-article {{
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  margin-bottom: 32px;
  overflow: hidden;
  scroll-margin-top: 20px;
}}
.scene-article.hidden {{ display: none; }}
.scene-header {{
  background: var(--bg2);
  border-bottom: 1px solid var(--border);
  padding: 14px 20px 10px;
  display: flex; flex-direction: column; gap: 6px;
}}
.scene-title {{
  font-size: 1.25rem;
  font-weight: bold;
  color: var(--accent);
}}
.scene-meta {{
  display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
}}
.scene-part-badge {{
  background: var(--accent);
  color: #fff;
  font-size: .7rem;
  padding: 2px 8px;
  border-radius: 10px;
  font-family: var(--font-ui);
}}
.char-chips {{ display: flex; gap: 4px; flex-wrap: wrap; }}
.char-chip {{
  font-size: .72rem;
  padding: 1px 7px;
  border-radius: 10px;
  border: 1px solid;
  font-family: var(--font-ui);
  cursor: pointer;
}}
.char-chip:hover {{ opacity: .8; }}
.scene-actions {{
  display: flex; gap: 6px; margin-top: 2px;
}}
.btn-icon {{
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 4px 10px;
  cursor: pointer;
  font-size: .9rem;
  color: var(--fg2);
}}
.btn-icon:hover {{ background: var(--border); }}

.scene-content {{
  padding: 24px 28px;
  line-height: 1.85;
  font-size: 1rem;
}}
.md-h1,.md-h2,.md-h3,.md-h4,.md-h5,.md-h6 {{
  color: var(--accent); margin: 1.2em 0 .5em;
  font-family: var(--font-body);
}}
.md-h1 {{ font-size: 1.5rem; }}
.md-h2 {{ font-size: 1.3rem; }}
.md-h3 {{ font-size: 1.15rem; }}
.md-h4 {{ font-size: 1rem; }}
.md-p {{ margin: .4em 0; }}
.md-blockquote {{
  border-right: 3px solid var(--accent);
  padding: .3em 1em;
  margin: .6em 0;
  color: var(--fg2);
  font-style: italic;
  background: var(--bg2);
  border-radius: 0 6px 6px 0;
}}
.md-li {{ margin: .2em 0 .2em 1.5em; list-style: none; }}
.md-li::before {{ content: "•"; margin-left: .5em; color: var(--accent); }}
.md-hr {{ border: none; border-top: 1px solid var(--border); margin: 1.2em 0; }}
.md-table-row {{ color: var(--fg2); font-size: .9rem; margin: .2em 0; }}
.spacer {{ height: .4em; }}
code {{ background: var(--bg3); padding: 0 4px; border-radius: 3px; font-size: .85em; }}

/* highlight search */
mark {{ background: #ffd70088; color: var(--fg); border-radius: 2px; }}

/* ── ANNOTATION ── */
.annotation-box {{
  border-top: 1px solid var(--border);
  padding: 16px 20px;
  background: var(--bg2);
}}
.annotation-label {{
  font-size: .82rem;
  color: var(--fg3);
  margin-bottom: 8px;
  font-family: var(--font-ui);
}}
.annotation-textarea {{
  width: 100%;
  min-height: 100px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px;
  font-family: var(--font-body);
  font-size: .95rem;
  color: var(--fg);
  resize: vertical;
  direction: rtl;
}}
.annotation-textarea:focus {{ outline: 2px solid var(--accent); }}
.annotation-saved {{
  font-size: .75rem;
  color: var(--fg3);
  margin-top: 4px;
  font-family: var(--font-ui);
}}

/* ── FAMILY TREE VIEW ── */
#view-tree {{
  padding: 20px;
  overflow: auto;
  min-height: 100%;
}}
#view-tree h2 {{
  font-size: 1.4rem;
  color: var(--accent);
  margin-bottom: 16px;
  text-align: center;
}}
#tree-svg-container {{
  overflow: auto;
  background: var(--bg2);
  border-radius: 12px;
  border: 1px solid var(--border);
  padding: 20px;
}}
.person-node {{
  cursor: pointer;
}}
.person-node rect {{
  rx: 8; ry: 8;
  transition: filter .15s;
}}
.person-node:hover rect {{ filter: brightness(1.15); }}
.person-name {{ font-family: "David", serif; font-size: 14px; }}
.person-role {{ font-family: Arial, sans-serif; font-size: 10px; opacity: .7; }}
.tree-edge {{ stroke-dasharray: none; }}
#tree-tooltip {{
  position: fixed;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 14px;
  font-family: var(--font-body);
  font-size: .9rem;
  color: var(--fg);
  pointer-events: none;
  z-index: 200;
  max-width: 240px;
  display: none;
  direction: rtl;
}}

/* ── STRUCTURE VIEW ── */
#view-structure {{
  padding: 28px 32px;
  max-width: 960px;
  margin: 0 auto;
}}
#view-structure h2 {{
  font-size: 1.5rem;
  color: var(--accent);
  margin-bottom: 20px;
}}
.structure-intro {{
  color: var(--fg2);
  line-height: 1.7;
  margin-bottom: 24px;
  font-size: .95rem;
}}
.arc-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
  margin-bottom: 28px;
}}
.arc-card {{
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px;
}}
.arc-card h3 {{
  font-size: 1rem;
  color: var(--accent);
  margin-bottom: 8px;
}}
.arc-card .arc-work {{
  font-weight: bold;
  font-size: .9rem;
  margin-bottom: 4px;
}}
.arc-card p {{
  font-size: .85rem;
  color: var(--fg2);
  line-height: 1.5;
}}
.arc-comparison {{
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
}}
.arc-comparison h3 {{
  color: var(--accent);
  margin-bottom: 12px;
}}
.compare-table {{
  width: 100%;
  border-collapse: collapse;
  font-size: .88rem;
}}
.compare-table th {{
  background: var(--bg3);
  padding: 8px 12px;
  text-align: right;
  border: 1px solid var(--border);
  color: var(--fg2);
  font-family: var(--font-ui);
  font-size: .8rem;
}}
.compare-table td {{
  padding: 8px 12px;
  border: 1px solid var(--border);
  vertical-align: top;
  line-height: 1.45;
}}
.compare-table tr:nth-child(even) td {{ background: var(--bg2); }}
.highlight-row td {{ background: #8b250015 !important; color: var(--accent); font-weight: bold; }}

.freytag {{
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
}}
.freytag h3 {{ color: var(--accent); margin-bottom: 16px; }}
.pyramid-svg {{ width: 100%; max-width: 700px; display: block; margin: 0 auto; }}

/* ── PRINT ── */
@media print {{
  #topbar, #sidebar, .scene-actions, .annotation-box, .scene-meta {{ display: none !important; }}
  #layout {{ height: auto; overflow: visible; }}
  #main {{ overflow: visible; }}
  .scene-article {{ page-break-after: always; border: none; }}
  .scene-article.hidden {{ display: none; }}
  .scene-content {{ padding: 0; }}
}}

/* ── CHAR FILTER BAR ── */
#char-filter {{
  position: sticky;
  top: 0;
  background: var(--bg2);
  border-bottom: 1px solid var(--border);
  padding: 8px 16px;
  display: none;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
  z-index: 50;
}}
#char-filter.visible {{ display: flex; }}
#char-filter-label {{
  font-size: .8rem;
  color: var(--fg3);
  font-family: var(--font-ui);
  margin-left: 8px;
}}
.filter-chip {{
  font-size: .78rem;
  padding: 3px 10px;
  border-radius: 12px;
  border: 1px solid;
  cursor: pointer;
  font-family: var(--font-ui);
  transition: all .15s;
  opacity: .5;
}}
.filter-chip.on {{ opacity: 1; font-weight: bold; }}
.filter-clear {{
  font-size: .78rem;
  padding: 3px 10px;
  border-radius: 12px;
  border: 1px solid var(--border);
  cursor: pointer;
  font-family: var(--font-ui);
  color: var(--fg3);
  background: var(--bg3);
}}

/* ── SCROLLBAR ── */
#sidebar::-webkit-scrollbar, #main::-webkit-scrollbar {{ width: 6px; }}
#sidebar::-webkit-scrollbar-track, #main::-webkit-scrollbar-track {{ background: transparent; }}
#sidebar::-webkit-scrollbar-thumb, #main::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}
</style>
</head>
<body>

<!-- TOP BAR -->
<div id="topbar">
  <button class="topbar-btn" onclick="toggleSidebar()">☰</button>
  <h1>מזמור לדוד — המחזמר המלא</h1>
  <input type="text" id="search-input" placeholder="חיפוש בטקסט..." oninput="doSearch(this.value)">
  <button class="topbar-btn" onclick="showView('scenes')">📜 סצנות</button>
  <button class="topbar-btn" onclick="showView('tree')">🌳 אילן יוחסין</button>
  <button class="topbar-btn" onclick="showView('structure')">🎭 מבנה דרמטי</button>
  <button class="topbar-btn" onclick="toggleCharFilter()">🎭 דמויות</button>
  <button class="topbar-btn" onclick="toggleTheme()">🌙</button>
  <button class="topbar-btn" onclick="exportAnnotations()">💾 ייצוא הערות</button>
</div>

<!-- LAYOUT -->
<div id="layout">

<!-- SIDEBAR -->
<nav id="sidebar">
  <div class="sidebar-special" onclick="showView('tree')">🌳 אילן יוחסין</div>
  <div class="sidebar-special" onclick="showView('structure')">🎭 מבנה דרמטי</div>
  <div class="sidebar-divider"></div>
  <div id="sidebar-nav"></div>
</nav>

<!-- MAIN -->
<main id="main">

  <!-- CHARACTER FILTER BAR -->
  <div id="char-filter">
    <span id="char-filter-label">סנן לפי דמות:</span>
  </div>

  <!-- SCENES VIEW -->
  <div id="view-scenes" class="view active">
    {all_scenes_html}
  </div>

  <!-- FAMILY TREE VIEW -->
  <div id="view-tree" class="view">
    <h2>אילן יוחסין — דמויות המחזמר</h2>
    <div id="tree-svg-container">
      <svg id="tree-svg" xmlns="http://www.w3.org/2000/svg"
           viewBox="0 0 1200 900" style="width:100%;min-width:900px;height:auto;">
        <!-- EDGES -->
        <!-- Jesse → David -->
        <line x1="600" y1="80" x2="600" y2="160" stroke="#666" stroke-width="2" class="tree-edge"/>
        <!-- Saul → Jonathan -->
        <line x1="200" y1="80" x2="150" y2="160" stroke="#666" stroke-width="2"/>
        <!-- Saul → Michal -->
        <line x1="200" y1="80" x2="280" y2="160" stroke="#666" stroke-width="2"/>
        <!-- David → children lines -->
        <line x1="600" y1="210" x2="600" y2="280" stroke="#666" stroke-width="1.5"/>
        <line x1="300" y1="280" x2="900" y2="280" stroke="#666" stroke-width="1.5"/>
        <line x1="300" y1="280" x2="300" y2="360" stroke="#666" stroke-width="1.5"/>
        <line x1="450" y1="280" x2="450" y2="360" stroke="#666" stroke-width="1.5"/>
        <line x1="600" y1="280" x2="600" y2="360" stroke="#666" stroke-width="1.5"/>
        <line x1="750" y1="280" x2="750" y2="360" stroke="#666" stroke-width="1.5"/>
        <line x1="900" y1="280" x2="900" y2="360" stroke="#666" stroke-width="1.5"/>
        <!-- Jonathan → Mephibosheth -->
        <line x1="150" y1="210" x2="150" y2="480" stroke="#666" stroke-width="1.5"/>
        <!-- David ↔ Michal (marriage) -->
        <line x1="280" y1="185" x2="520" y2="185" stroke="#9333ea" stroke-width="1.5" stroke-dasharray="5,4"/>
        <!-- David ↔ Bathsheba -->
        <line x1="600" y1="210" x2="750" y2="210" stroke="#0891b2" stroke-width="1.5" stroke-dasharray="5,4"/>
        <!-- Zeruiah → Joab,Abishai,Asahel -->
        <line x1="900" y1="80" x2="900" y2="160" stroke="#666" stroke-width="2"/>
        <line x1="800" y1="160" x2="1000" y2="160" stroke="#666" stroke-width="1.5"/>
        <line x1="800" y1="160" x2="800" y2="240" stroke="#666" stroke-width="1.5"/>
        <line x1="900" y1="160" x2="900" y2="240" stroke="#666" stroke-width="1.5"/>
        <line x1="1000" y1="160" x2="1000" y2="240" stroke="#666" stroke-width="1.5"/>

        <!-- LEGEND -->
        <line x1="30" y1="855" x2="80" y2="855" stroke="#666" stroke-width="2"/>
        <text x="90" y="859" font-family="Arial" font-size="11" fill="#666">קשר משפחתי</text>
        <line x1="200" y1="855" x2="250" y2="855" stroke="#9333ea" stroke-width="2" stroke-dasharray="5,4"/>
        <text x="260" y="859" font-family="Arial" font-size="11" fill="#9333ea">נישואים</text>

        <!-- NODES -->
        <!-- Jesse -->
        <g class="person-node" onclick="personClick('ישי','אביו של דוד','ישי בן אובד מבית לחם, צאצא רות ובועז')">
          <rect x="540" y="30" width="120" height="45" fill="#d4a800" rx="8"/>
          <text x="600" y="52" text-anchor="middle" class="person-name" fill="#fff">ישי</text>
          <text x="600" y="67" text-anchor="middle" class="person-role" fill="#fff">אבי דוד</text>
        </g>
        <!-- Saul -->
        <g class="person-node" onclick="personClick('שאול','המלך הראשון','שאול בן קיש ממטה בנימין — המלך הראשון שנדחה')">
          <rect x="140" y="30" width="120" height="45" fill="#dc2626" rx="8"/>
          <text x="200" y="52" text-anchor="middle" class="person-name" fill="#fff">שאול</text>
          <text x="200" y="67" text-anchor="middle" class="person-role" fill="#fff">מלך ישראל</text>
        </g>
        <!-- David -->
        <g class="person-node" onclick="personClick('דוד','מלך ישראל','דוד בן ישי — הרועה שנמשח, גיבור, חוטא, מתחרט, משורר')">
          <rect x="520" y="160" width="160" height="50" fill="#2563eb" rx="8"/>
          <text x="600" y="183" text-anchor="middle" class="person-name" fill="#fff" font-size="16">דוד המלך</text>
          <text x="600" y="200" text-anchor="middle" class="person-role" fill="#fff">מלך יהודה וישראל</text>
        </g>
        <!-- Jonathan -->
        <g class="person-node" onclick="personClick('יונתן','בן שאול','יונתן בן שאול — אוהב דוד, בחר בברית על חשבון יורשתו')">
          <rect x="90" y="160" width="120" height="45" fill="#16a34a" rx="8"/>
          <text x="150" y="182" text-anchor="middle" class="person-name" fill="#fff">יונתן</text>
          <text x="150" y="197" text-anchor="middle" class="person-role" fill="#fff">בן שאול</text>
        </g>
        <!-- Michal -->
        <g class="person-node" onclick="personClick('מיכל','בת שאול, אשת דוד','מיכל אהבה את דוד, הצילה אותו, הוחזרה בכוח ומתה עקרה')">
          <rect x="220" y="160" width="120" height="45" fill="#9333ea" rx="8"/>
          <text x="280" y="182" text-anchor="middle" class="person-name" fill="#fff">מיכל</text>
          <text x="280" y="197" text-anchor="middle" class="person-role" fill="#fff">בת שאול, אשת דוד</text>
        </g>
        <!-- Bathsheba -->
        <g class="person-node" onclick="personClick('בת-שבע','אשת אוריה ואח״כ דוד','בת-שבע — אשת אוריה החתי, נלקחה על ידי דוד, ילדה את שלמה')">
          <rect x="700" y="160" width="130" height="45" fill="#0891b2" rx="8"/>
          <text x="765" y="182" text-anchor="middle" class="person-name" fill="#fff">בת-שבע</text>
          <text x="765" y="197" text-anchor="middle" class="person-role" fill="#fff">אם שלמה</text>
        </g>
        <!-- Children of David -->
        <!-- Amnon -->
        <g class="person-node" onclick="personClick('אמנון','בכור דוד מאחינועם','אמנון — אנס את תמר אחותו, נהרג ע״י אבשלום')">
          <rect x="250" y="360" width="110" height="45" fill="#854d0e" rx="8"/>
          <text x="305" y="382" text-anchor="middle" class="person-name" fill="#fff">אמנון</text>
          <text x="305" y="397" text-anchor="middle" class="person-role" fill="#fff">בכור דוד</text>
        </g>
        <!-- Tamar -->
        <g class="person-node" onclick="personClick('תמר','בת דוד ומעכה','תמר — בת דוד, נאנסה ע״י אמנון, חיה שוממה בבית אבשלום')">
          <rect x="395" y="360" width="110" height="45" fill="#86198f" rx="8"/>
          <text x="450" y="382" text-anchor="middle" class="person-name" fill="#fff">תמר</text>
          <text x="450" y="397" text-anchor="middle" class="person-role" fill="#fff">בת דוד</text>
        </g>
        <!-- Absalom -->
        <g class="person-node" onclick="personClick('אבשלום','בן דוד ומעכה','אבשלום — יפה תואר, נקם בגלל תמר, מרד, נהרג ע״י יואב')">
          <rect x="540" y="360" width="120" height="45" fill="#be123c" rx="8"/>
          <text x="600" y="382" text-anchor="middle" class="person-name" fill="#fff">אבשלום</text>
          <text x="600" y="397" text-anchor="middle" class="person-role" fill="#fff">בן דוד</text>
        </g>
        <!-- Solomon -->
        <g class="person-node" onclick="personClick('שלמה','בן דוד ובת-שבע','שלמה — יורש המלכות, בנה את בית המקדש שדוד חלם עליו')">
          <rect x="695" y="360" width="120" height="45" fill="#047857" rx="8"/>
          <text x="755" y="382" text-anchor="middle" class="person-name" fill="#fff">שלמה</text>
          <text x="755" y="397" text-anchor="middle" class="person-role" fill="#fff">יורש המלכות</text>
        </g>
        <!-- Adonijah -->
        <g class="person-node" onclick="personClick('אדוניה','בן דוד מחגית','אדוניה — התמרד ורצה למלוך, הודח לטובת שלמה')">
          <rect x="850" y="360" width="110" height="45" fill="#374151" rx="8"/>
          <text x="905" y="382" text-anchor="middle" class="person-name" fill="#fff">אדוניה</text>
          <text x="905" y="397" text-anchor="middle" class="person-role" fill="#fff">בן דוד מחגית</text>
        </g>
        <!-- Mephibosheth -->
        <g class="person-node" onclick="personClick('מפיבושת','בן יונתן','מפיבושת — נכה, בן יונתן, הוזמן לשולחן דוד לכל ימיו')">
          <rect x="90" y="480" width="120" height="45" fill="#065f46" rx="8"/>
          <text x="150" y="502" text-anchor="middle" class="person-name" fill="#fff">מפיבושת</text>
          <text x="150" y="517" text-anchor="middle" class="person-role" fill="#fff">בן יונתן</text>
        </g>
        <!-- Zeruiah (David's sister) -->
        <g class="person-node" onclick="personClick('צרויה','אחות דוד','צרויה — אחות דוד, אם יואב אבישי ועשהאל')">
          <rect x="840" y="30" width="120" height="45" fill="#6b7280" rx="8"/>
          <text x="900" y="52" text-anchor="middle" class="person-name" fill="#fff">צרויה</text>
          <text x="900" y="67" text-anchor="middle" class="person-role" fill="#fff">אחות דוד</text>
        </g>
        <!-- Joab -->
        <g class="person-node" onclick="personClick('יואב','שר צבא דוד','יואב בן צרויה — שר הצבא החזק, הסיר את \"הדם החף\" מדוד')">
          <rect x="740" y="240" width="120" height="45" fill="#92400e" rx="8"/>
          <text x="800" y="262" text-anchor="middle" class="person-name" fill="#fff">יואב</text>
          <text x="800" y="277" text-anchor="middle" class="person-role" fill="#fff">שר צבא</text>
        </g>
        <!-- Abishai -->
        <g class="person-node" onclick="personClick('אבישי','אח יואב','אבישי בן צרויה — נאמן לדוד, רצה לשחוט את שמעי')">
          <rect x="870" y="240" width="110" height="45" fill="#78716c" rx="8"/>
          <text x="925" y="262" text-anchor="middle" class="person-name" fill="#fff">אבישי</text>
          <text x="925" y="277" text-anchor="middle" class="person-role" fill="#fff">בן צרויה</text>
        </g>
        <!-- Asahel -->
        <g class="person-node" onclick="personClick('עשהאל','אח יואב','עשהאל — קל ברגליים, נהרג ע״י אבנר; מותו גרם ליואב לנקום')">
          <rect x="990" y="240" width="110" height="45" fill="#a8a29e" rx="8"/>
          <text x="1045" y="262" text-anchor="middle" class="person-name" fill="#fff">עשהאל</text>
          <text x="1045" y="277" text-anchor="middle" class="person-role" fill="#fff">בן צרויה</text>
        </g>
        <!-- Nathan -->
        <g class="person-node" onclick="personClick('נתן','הנביא','נתן הנביא — שגר לדוד את משל האיש העני, מלך שלמה')">
          <rect x="60" y="600" width="120" height="45" fill="#4338ca" rx="8"/>
          <text x="120" y="622" text-anchor="middle" class="person-name" fill="#fff">נתן</text>
          <text x="120" y="637" text-anchor="middle" class="person-role" fill="#fff">הנביא</text>
        </g>
        <!-- Samuel -->
        <g class="person-node" onclick="personClick('שמואל','שופט ונביא','שמואל — משח את שאול ואח״כ את דוד; מוזג האל לעולם')">
          <rect x="200" y="600" width="120" height="45" fill="#1e3a5f" rx="8"/>
          <text x="260" y="622" text-anchor="middle" class="person-name" fill="#fff">שמואל</text>
          <text x="260" y="637" text-anchor="middle" class="person-role" fill="#fff">הנביא</text>
        </g>
        <!-- Abigail -->
        <g class="person-node" onclick="personClick('אביגיל','אשת נבל ואחר כן דוד','אביגיל — חכמה ויפה, עצרה את דוד מלשפוך דם נבל')">
          <rect x="350" y="600" width="120" height="45" fill="#ea580c" rx="8"/>
          <text x="410" y="622" text-anchor="middle" class="person-name" fill="#fff">אביגיל</text>
          <text x="410" y="637" text-anchor="middle" class="person-role" fill="#fff">אשת דוד</text>
        </g>
        <!-- Uriah -->
        <g class="person-node" onclick="personClick('אוריה','החתי, בעל בת-שבע','אוריה החתי — לוחם נאמן, נשלח למות על ידי דוד שרצה את אשתו')">
          <rect x="500" y="600" width="120" height="45" fill="#374151" rx="8"/>
          <text x="560" y="622" text-anchor="middle" class="person-name" fill="#fff">אוריה</text>
          <text x="560" y="637" text-anchor="middle" class="person-role" fill="#fff">החתי</text>
        </g>
        <!-- Rizpah -->
        <g class="person-node" onclick="personClick('רצפה','פילגש שאול','רצפה בת איה — שמרה על גופות בניה חמישה חודשים')">
          <rect x="650" y="600" width="120" height="45" fill="#be185d" rx="8"/>
          <text x="710" y="622" text-anchor="middle" class="person-name" fill="#fff">רצפה</text>
          <text x="710" y="637" text-anchor="middle" class="person-role" fill="#fff">פילגש שאול</text>
        </g>
        <!-- Shimei -->
        <g class="person-node" onclick="personClick('שמעי','בן גרא הבנימיני','שמעי — קילל את דוד בברחו, בקש סליחה, נהרג ע״פ צוואת דוד')">
          <rect x="800" y="600" width="120" height="45" fill="#78350f" rx="8"/>
          <text x="860" y="622" text-anchor="middle" class="person-name" fill="#fff">שמעי</text>
          <text x="860" y="637" text-anchor="middle" class="person-role" fill="#fff">בן גרא</text>
        </g>
        <!-- Ahithophel -->
        <g class="person-node" onclick="personClick('אחיתופל','יועץ שפנה לאבשלום','אחיתופל — יועץ דוד שבגד ועבר לאבשלום; התאבד כשלא שמעו לעצתו')">
          <rect x="950" y="600" width="120" height="45" fill="#1f2937" rx="8"/>
          <text x="1010" y="622" text-anchor="middle" class="person-name" fill="#fff">אחיתופל</text>
          <text x="1010" y="637" text-anchor="middle" class="person-role" fill="#fff">היועץ הבוגד</text>
        </g>

        <!-- Annotations lines for secondary -->
        <text x="120" y="590" text-anchor="middle" font-family="Arial" font-size="9" fill="#666">נביאים ויועצים</text>
        <text x="600" y="590" text-anchor="middle" font-family="Arial" font-size="9" fill="#666">דמויות צדדיות</text>
      </svg>
    </div>
    <p style="text-align:center;color:var(--fg3);font-size:.8rem;margin-top:12px;font-family:var(--font-ui)">
      לחץ על דמות לפרטים ולסצנות שבהן היא מופיעה
    </p>
  </div>

  <!-- DRAMATIC STRUCTURE VIEW -->
  <div id="view-structure" class="view">
    <h2>מבנה דרמטי — מזמור לדוד בהקשר</h2>
    <p class="structure-intro">
      כל מחזמר גדול מסתמך על מבנה דרמטי שנוסה ונבחן לאורך מאות שנים.
      הטבלה שלפניכם ממקמת את <strong>מזמור לדוד</strong> על פי עקרונות פרייטאג (1863)
      וממשילה אותו ליצירות במה בנות ביצוע — שייקספיר, <em>מלך האריות</em>, <em>ביקור הפקידה</em>,
      <em>Les Misérables</em> — כדי לזהות מה ייחודי ומה אוניברסלי.
    </p>

    <div class="freytag">
      <h3>פירמידת פרייטאג — מבנה חמשת-שלבים</h3>
      <svg class="pyramid-svg" viewBox="0 0 700 260" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="pygrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#2563eb;stop-opacity:.7"/>
            <stop offset="40%" style="stop-color:#8b2500;stop-opacity:.9"/>
            <stop offset="100%" style="stop-color:#374151;stop-opacity:.7"/>
          </linearGradient>
        </defs>
        <!-- Pyramid shape -->
        <polygon points="20,220 350,40 680,220" fill="url(#pygrad)" opacity=".15" stroke="#8b2500" stroke-width="2"/>
        <!-- Vertical dividers -->
        <line x1="185" y1="130" x2="185" y2="220" stroke="#666" stroke-width="1" stroke-dasharray="4,3"/>
        <line x1="350" y1="40" x2="350" y2="220" stroke="#666" stroke-width="1" stroke-dasharray="4,3"/>
        <line x1="515" y1="130" x2="515" y2="220" stroke="#666" stroke-width="1" stroke-dasharray="4,3"/>
        <!-- Labels top -->
        <text x="95" y="25" text-anchor="middle" font-family="Arial" font-size="11" fill="#2563eb">① חשיפה</text>
        <text x="268" y="25" text-anchor="middle" font-family="Arial" font-size="11" fill="#8b2500">② עלייה</text>
        <text x="350" y="18" text-anchor="middle" font-family="Arial" font-size="13" fill="#8b2500" font-weight="bold">③ שיא</text>
        <text x="435" y="25" text-anchor="middle" font-family="Arial" font-size="11" fill="#374151">④ ירידה</text>
        <text x="605" y="25" text-anchor="middle" font-family="Arial" font-size="11" fill="#374151">⑤ סיום</text>
        <!-- Play moments -->
        <circle cx="95" cy="185" r="5" fill="#2563eb"/>
        <text x="95" y="205" text-anchor="middle" font-family="David,serif" font-size="10" fill="#333">משיחת דוד</text>
        <circle cx="185" cy="155" r="5" fill="#16a34a"/>
        <text x="185" y="245" text-anchor="middle" font-family="David,serif" font-size="10" fill="#333">ברית יונתן</text>
        <circle cx="268" cy="90" r="5" fill="#2563eb"/>
        <text x="268" y="250" text-anchor="middle" font-family="David,serif" font-size="10" fill="#333">המלכת דוד</text>
        <circle cx="350" cy="40" r="7" fill="#8b2500"/>
        <text x="350" y="255" text-anchor="middle" font-family="David,serif" font-size="10" fill="#8b2500" font-weight="bold">בת-שבע/אוריה</text>
        <circle cx="430" cy="90" r="5" fill="#be123c"/>
        <text x="430" y="245" text-anchor="middle" font-family="David,serif" font-size="10" fill="#333">מרד אבשלום</text>
        <circle cx="515" cy="145" r="5" fill="#374151"/>
        <text x="515" y="250" text-anchor="middle" font-family="David,serif" font-size="10" fill="#333">מות אבשלום</text>
        <circle cx="605" cy="185" r="5" fill="#047857"/>
        <text x="605" y="205" text-anchor="middle" font-family="David,serif" font-size="10" fill="#333">צוואה/שלמה</text>
      </svg>
    </div>

    <div class="arc-comparison">
      <h3>השוואה למחזמרים ויצירות במה קלאסיות</h3>
      <table class="compare-table">
        <thead>
          <tr>
            <th>שלב דרמטי</th>
            <th>מזמור לדוד</th>
            <th>המלך ליר (שייקספיר)</th>
            <th>מלך האריות</th>
            <th>Les Misérables</th>
            <th>ביקור הפקידה (דיירנמאט)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>① חשיפה / Exposition</td>
            <td>דוד הרועה; משיחת שמואל; גלית</td>
            <td>ליר מחלק ממלכתו; הרעה והטובה</td>
            <td>סימבה כגור; מפלת מופסה</td>
            <td>ז'אן-ואלז'אן יוצא מהכלא</td>
            <td>העיר ממתינה לפקידה; עוני</td>
          </tr>
          <tr>
            <td>② עלייה / Rising Action</td>
            <td>ברית יונתן; בריחת שאול; המלכה בחברון</td>
            <td>גורנריל ורגן מפשיטים את ליר; בורח לסערה</td>
            <td>סימבה בגלות; חברות עם טימון ופומבה</td>
            <td>ז'אן בונה עצמו; חיפוש קוזט</td>
            <td>הפקידה מגיעה; מציעה כסף תמורת נקם</td>
          </tr>
          <tr class="highlight-row">
            <td>③ שיא / Climax</td>
            <td><strong>בת-שבע ואוריה — "עֲשֵׂה זֹאת"</strong></td>
            <td>ליר בסערה; "גזרה-ה-עיניים"</td>
            <td>סימבה מול סקאר</td>
            <td>מחסום הבריקאדה; מות גברוש</td>
            <td>הפקידה קונה ​את כל העיר</td>
          </tr>
          <tr>
            <td>④ ירידה / Falling Action</td>
            <td>קללת נתן; אמנון-תמר; מרד אבשלום; "בני אבשלום!"</td>
            <td>מות קורדליה; ליר אוחז בגופה</td>
            <td>קרב פוהארי; סקאר נחשף כרוצח</td>
            <td>ז'אן בורח; ז'אבר מתאבד; לחם חסד</td>
            <td>אלפרד איל נשפט ונהרג</td>
          </tr>
          <tr>
            <td>⑤ סיום / Denouement</td>
            <td>צוואת דוד; המלכת שלמה; "שיר לדוד"</td>
            <td>ליר מת על גופת קורדליה; ממלכה חרבה</td>
            <td>סימבה מולך; "Circle of Life"</td>
            <td>מות ז'אן; אהבה-זיכרון; "Do you hear the people sing"</td>
            <td>העיר מקבלת את הכסף ואת מותה</td>
          </tr>
          <tr>
            <td>💡 הנושא המרכזי</td>
            <td>אמונה דרך ייסורים; עצירת יד = כינור</td>
            <td>גאווה → עיוורון → כאב → חסד מאוחר מדי</td>
            <td>זהות; גאולה; מעגל החיים</td>
            <td>חסד מול צדק; ניגאל מנשלט על ידי חוק</td>
            <td>נקמה היא עסקה; הצדק עולה ביוקר</td>
          </tr>
          <tr>
            <td>🎵 הרגע המוזיקלי הגדול</td>
            <td>"הללויה"; "בני אבשלום"; תהילים מן הלב</td>
            <td>"Blow winds and crack your cheeks" (פרוזה)</td>
            <td>"Can you feel the love tonight"</td>
            <td>"I Dreamed a Dream"; "One Day More"</td>
            <td>(מחזה פרוזה, אין מוזיקה)</td>
          </tr>
          <tr>
            <td>🔑 ייחוד מזמור לדוד</td>
            <td colspan="5" style="color:var(--accent);font-weight:bold">
              חוט הזהב שאין לו אח: הדמות הראשית <em>כותבת</em> את השירים שלה — תהילים צומח בזמן אמת מתוך הסבל.
              הקהל יודע את הסוף (ספר תהילים) אבל לא יודע איך הגיעו לשם.
              בשום מחזמר אחר המוזיקה <em>היא</em> המקור ולא רק ביטוי.
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="arc-grid">
      <div class="arc-card">
        <h3>קשת דוד — גיבור שנופל ומתרומם</h3>
        <div class="arc-work">ז'אן ואלז'אן / המלך ליר / סימבה</div>
        <p>גיבור עם מתנה טבעית (אומץ/שיר/מלוכה) → חטא או ניסיון → גלות פנימית → חזרה מכוח ביטוי עמוק. ייחוד: דוד חוזר <em>דרך</em> תהילים, לא למרותם.</p>
      </div>
      <div class="arc-card">
        <h3>קשת יואב — ה"ידיים הלכלכות"</h3>
        <div class="arc-work">יאגו / מקבת / ז'אבר</div>
        <p>הדמות הצדדית שעושה את המלאכה המלוכלכת — הורגת את אבנר, מחסלת את אבשלום. יואב מאמין שהוא שומר על דוד. זהו ויכוח על מוסר ושלטון.</p>
      </div>
      <div class="arc-card">
        <h3>קשת אבשלום — הבן שלא מוכר</h3>
        <div class="arc-work">האמלט / שיילוק / אספק</div>
        <p>בן שנדחה, יופי ללא פנים, כעס שמבקש הכרה. ייחוד: דוד אוהב אותו עד הסוף — "בני בני אבשלום" — גם אחרי המרד. זה לא מנגנון של שנאה אלא של קרע.</p>
      </div>
    </div>

    <div class="arc-comparison">
      <h3>מבנה המחזמר — 15 תמונות לפי מעגל הרגשי</h3>
      <table class="compare-table">
        <thead>
          <tr><th>#</th><th>תמונה</th><th>רגש מרכזי</th><th>מזמור</th><th>מקביל בעולם</th></tr>
        </thead>
        <tbody>
          <tr><td>א</td><td>המשיחה + גלית</td><td>תמימות ואמונה</td><td>כג</td><td>Simba born / Jean Valjean released</td></tr>
          <tr><td>ב</td><td>יונתן + ברית</td><td>אהבה לא-רומנטית</td><td>נז</td><td>Hamlet & Horatio / Frodo & Sam</td></tr>
          <tr><td>ג</td><td>בריחה מפני שאול</td><td>בדידות ואמונה</td><td>לד</td><td>Les Mis Act I / Hamlet exile</td></tr>
          <tr><td>ד</td><td>מות שאול + קינה</td><td>אבל על אויב</td><td>יח</td><td>Lear over Cordelia / "No good deed"</td></tr>
          <tr><td>ה</td><td>מלחמת האחים</td><td>מחיר הכוח</td><td>—</td><td>Richard III rising / Henry IV civil war</td></tr>
          <tr><td>ו</td><td>הריקוד ומיכל</td><td>אקסטזה מול בושה</td><td>כד</td><td>Eliza Doolittle dancing / Defying Gravity</td></tr>
          <tr class="highlight-row"><td>ז</td><td>"לא אתה תבנה"</td><td>קבלת מגבלה = חירות</td><td>קלה</td><td>אין מקביל ישיר — ייחוד מזמור לדוד</td></tr>
          <tr><td>ח</td><td>בת-שבע ואוריה</td><td>תאווה ופשע</td><td>נא</td><td>Macbeth / Othello jealousy / Scar's plot</td></tr>
          <tr><td>ט</td><td>אמנון + תמר</td><td>פשע ודממה</td><td>—</td><td>Titus Andronicus / Rigoletto</td></tr>
          <tr><td>י</td><td>מרד אבשלום</td><td>קרע אב-בן</td><td>ג</td><td>King Lear / The Lion King (Scar)</td></tr>
          <tr><td>יא</td><td>מות אבשלום</td><td>אבל הגדול ביותר</td><td>—</td><td>Lear/Cordelia; Hamlet/Ophelia</td></tr>
          <tr><td>יב</td><td>שיבה לירושלים</td><td>תיקון חלקי</td><td>קכו</td><td>Jean Valjean returns / The Return of the King</td></tr>
          <tr><td>יג</td><td>הללויה + שיר</td><td>כפרה דרך שיר</td><td>יח</td><td>Finale — "Do you hear?" / "Circle of Life"</td></tr>
          <tr><td>יד</td><td>הצוואה</td><td>ירושה מורכבת</td><td>עב</td><td>Henry IV Part 2 / Lion King epilogue</td></tr>
        </tbody>
      </table>
    </div>
  </div>

</main>
</div>

<!-- TOOLTIP -->
<div id="tree-tooltip"></div>

<script>
// ── DATA ──
const SCENES = {scenes_json};
const CHARS = {chars_json};

// ── INIT ──
let activeChar = null;
let activeScene = null;
let sidebarOpen = true;

function init() {{
  buildSidebar();
  loadAllAnnotations();
  loadTheme();
}}

function buildSidebar() {{
  const nav = document.getElementById('sidebar-nav');
  let currentPart = null;
  SCENES.forEach(s => {{
    if (s.part !== currentPart) {{
      currentPart = s.part;
      if (currentPart) {{
        const div = document.createElement('div');
        div.className = 'sidebar-section';
        div.textContent = currentPart;
        nav.appendChild(div);
        const hr = document.createElement('div');
        hr.className = 'sidebar-divider';
        nav.appendChild(hr);
      }}
    }}
    const a = document.createElement('a');
    a.className = 'sidebar-item';
    a.textContent = s.label;
    a.href = '#';
    a.onclick = (e) => {{ e.preventDefault(); jumpToScene(s.id); }};
    a.id = 'nav-' + s.id;
    nav.appendChild(a);
  }});
  buildCharFilter();
}}

function buildCharFilter() {{
  const bar = document.getElementById('char-filter');
  Object.entries(CHARS).forEach(([name, data]) => {{
    const chip = document.createElement('button');
    chip.className = 'filter-chip on';
    chip.textContent = name;
    chip.style.background = data.color + '22';
    chip.style.color = data.color;
    chip.style.borderColor = data.color + '60';
    chip.onclick = () => filterByChar(name, chip);
    bar.appendChild(chip);
  }});
  const clear = document.createElement('button');
  clear.className = 'filter-clear';
  clear.textContent = 'הצג הכל';
  clear.onclick = clearFilter;
  bar.appendChild(clear);
}}

// ── NAVIGATION ──
function showView(name) {{
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.getElementById('view-' + name).classList.add('active');
}}

function jumpToScene(id) {{
  showView('scenes');
  document.querySelectorAll('.sidebar-item').forEach(a => a.classList.remove('active'));
  const nav = document.getElementById('nav-' + id);
  if (nav) nav.classList.add('active');
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({{behavior:'smooth', block:'start'}});
}}

// ── SIDEBAR ──
function toggleSidebar() {{
  sidebarOpen = !sidebarOpen;
  document.getElementById('sidebar').style.display = sidebarOpen ? '' : 'none';
}}

// ── SEARCH ──
let searchTimeout;
function doSearch(q) {{
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => applySearch(q.trim()), 300);
}}

function applySearch(q) {{
  const articles = document.querySelectorAll('.scene-article');
  // Remove old highlights
  articles.forEach(a => {{
    const content = a.querySelector('.scene-content');
    content.innerHTML = content.innerHTML.replace(/<mark>(.*?)<\/mark>/gi, '$1');
  }});
  if (!q) {{
    articles.forEach(a => a.classList.remove('hidden'));
    return;
  }}
  const re = new RegExp(q.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&'), 'gi');
  articles.forEach(a => {{
    const text = a.querySelector('.scene-content').textContent;
    if (re.test(text)) {{
      a.classList.remove('hidden');
      const content = a.querySelector('.scene-content');
      content.innerHTML = content.innerHTML.replace(re, m => `<mark>${{m}}</mark>`);
    }} else {{
      a.classList.add('hidden');
    }}
  }});
}}

// ── CHARACTER FILTER ──
function toggleCharFilter() {{
  const bar = document.getElementById('char-filter');
  bar.classList.toggle('visible');
}}

function filterByChar(name, chip) {{
  const isOn = chip.classList.contains('on');
  if (isOn) {{
    // Turn this one off, filter to only this char
    document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('on'));
    chip.classList.add('on');
    activeChar = name;
  }} else {{
    chip.classList.add('on');
    activeChar = null;
  }}
  applyCharFilter();
}}

function clearFilter() {{
  document.querySelectorAll('.filter-chip').forEach(c => c.classList.add('on'));
  activeChar = null;
  applyCharFilter();
}}

function applyCharFilter() {{
  document.querySelectorAll('.scene-article').forEach(a => {{
    if (!activeChar) {{ a.classList.remove('hidden'); return; }}
    const chars = a.dataset.chars || '';
    if (chars.includes(activeChar)) a.classList.remove('hidden');
    else a.classList.add('hidden');
  }});
}}

// ── ANNOTATIONS ──
function toggleAnnotation(id) {{
  const box = document.getElementById('ann-' + id);
  const ta = document.getElementById('textarea-' + id);
  box.style.display = box.style.display === 'none' ? 'block' : 'none';
  if (box.style.display === 'block') ta.focus();
}}

function saveAnnotation(id) {{
  const ta = document.getElementById('textarea-' + id);
  const key = 'ann_' + id;
  localStorage.setItem(key, ta.value);
  const saved = document.getElementById('saved-' + id);
  saved.textContent = '✓ נשמר';
  setTimeout(() => {{ saved.textContent = ''; }}, 1500);
}}

function loadAllAnnotations() {{
  SCENES.forEach(s => {{
    const val = localStorage.getItem('ann_' + s.id);
    if (val) {{
      const ta = document.getElementById('textarea-' + s.id);
      if (ta) ta.value = val;
    }}
  }});
}}

function exportAnnotations() {{
  const lines = [];
  lines.push('הערות למחזמר מזמור לדוד');
  lines.push('תאריך: ' + new Date().toLocaleDateString('he-IL'));
  lines.push('');
  SCENES.forEach(s => {{
    const val = localStorage.getItem('ann_' + s.id);
    if (val && val.trim()) {{
      lines.push('=== ' + s.label + ' ===');
      lines.push(val);
      lines.push('');
    }}
  }});
  if (lines.length <= 3) {{
    alert('אין עדיין הערות שמורות.');
    return;
  }}
  const blob = new Blob([lines.join('\\n')], {{type: 'text/plain;charset=utf-8'}});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'הערות-מזמור-לדוד.txt';
  a.click();
}}

// ── PRINT ──
function printScene(id) {{
  // Hide all other scenes, print, restore
  document.querySelectorAll('.scene-article').forEach(a => {{
    if (a.id !== id) a.classList.add('hidden');
  }});
  window.print();
  document.querySelectorAll('.scene-article').forEach(a => a.classList.remove('hidden'));
  applyCharFilter();
}}

// ── THEME ──
function toggleTheme() {{
  const dark = document.documentElement.getAttribute('data-theme') === 'dark';
  document.documentElement.setAttribute('data-theme', dark ? '' : 'dark');
  localStorage.setItem('theme', dark ? 'light' : 'dark');
}}
function loadTheme() {{
  const t = localStorage.getItem('theme');
  if (t === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
}}

// ── FAMILY TREE TOOLTIP ──
function personClick(name, role, desc) {{
  const tt = document.getElementById('tree-tooltip');
  const sceneList = CHARS[name] ? CHARS[name].scenes : [];
  const sceneLinks = sceneList.map(id => {{
    const s = SCENES.find(x => x.id === id);
    return s ? `<a href="#" onclick="jumpToScene('${{id}}');return false" style="color:var(--accent)">${{s.label}}</a>` : '';
  }}).filter(Boolean).join(', ');
  tt.innerHTML = `
    <strong>${{name}}</strong><br>
    <span style="color:#666;font-size:.8rem">${{role}}</span><br>
    <p style="margin:.5em 0;font-size:.85rem">${{desc}}</p>
    ${{sceneLinks ? '<div style="font-size:.8rem;margin-top:4px"><strong>סצנות:</strong> ' + sceneLinks + '</div>' : ''}}
    <div style="font-size:.75rem;color:#999;margin-top:6px">לחץ שוב לסגירה</div>
  `;
  if (tt.style.display === 'block' && tt.dataset.person === name) {{
    tt.style.display = 'none';
  }} else {{
    tt.style.display = 'block';
    tt.dataset.person = name;
    tt.style.top = '200px';
    tt.style.right = '300px';
  }}
}}

document.addEventListener('click', e => {{
  const tt = document.getElementById('tree-tooltip');
  if (!e.target.closest('#tree-svg') && !e.target.closest('#tree-tooltip')) {{
    tt.style.display = 'none';
  }}
}});

// ── SCROLL SPY ──
const observer = new IntersectionObserver((entries) => {{
  entries.forEach(entry => {{
    if (entry.isIntersecting) {{
      const id = entry.target.id;
      document.querySelectorAll('.sidebar-item').forEach(a => a.classList.remove('active'));
      const nav = document.getElementById('nav-' + id);
      if (nav) {{
        nav.classList.add('active');
        nav.scrollIntoView({{block:'nearest'}});
      }}
    }}
  }});
}}, {{threshold: 0.1, rootMargin: '-10% 0px -80% 0px'}});

document.querySelectorAll('.scene-article').forEach(el => observer.observe(el));

init();
</script>
</body>
</html>'''

out = ROOT / "מזמור-לדוד-web.html"
out.write_text(HTML, encoding="utf-8")
size = out.stat().st_size
print(f"נשמר: {out}")
print(f"גודל: {size:,} bytes ({size//1024} KB)")
