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
    "דוד": {"color": "#2563eb", "story": "רועה צאן שנמשח למלך על ידי שמואל הנביא, לוחם וסופר מזמורי תהילים. עלה לגדולה בעקבות ניצחונו על גוליית, ונס מפני שאול שנים רבות. מלך על כל ישראל ויהודה, ידוע כ\"חביב ה'\" אך נפל בחטא בת-שבע ואוריה.", "scenes": []},
    "שאול": {"color": "#dc2626", "story": "המלך הראשון על ישראל, נבחר בגלל מראהו המלכותי. נדחה מהמלוכה בגלל חטאיו, ורדף אחרי דוד מתוך קנאה ופחד. נפל בגלבוע יחד עם שלושת בניו.", "scenes": []},
    "יונתן": {"color": "#16a34a", "story": "בן שאול ואוהב נפש של דוד, אחד הלוחמים האמיצים ביותר. כרת ברית אהבה עם דוד שגברה על נאמנותו לאביו. נפל יחד עם אביו בגלבוע.", "scenes": []},
    "מיכל": {"color": "#9333ea", "story": "בת שאול ואשתו הראשונה של דוד, שאהבה אותו. הצילה אותו מידי שאול אך נפרדה ממנו ונישאה לאחר. ביקרה את דוד בריקודו לפני הארון ומתה ללא ילדים.", "scenes": []},
    "יואב": {"color": "#92400e", "story": "אחיין דוד ומפקד צבאו הנאמן אך הקשה. הרג את אבנר ועשהאל ואבשלום בניגוד לציווי דוד. גיבור מלחמה חסר רחמים שסייע לדוד בעלייתו ובמרד אבשלום.", "scenes": []},
    "אביגיל": {"color": "#ea580c", "story": "אשה חכמה ויפה, אשתו של נבל הנבל. מנעה מדוד לשפוך דם בכעסו ולאחר מות נבל נשאה דוד לאשה. סמלה של חוכמה ומניעת מלחמת אחים.", "scenes": []},
    "בת-שבע": {"color": "#0891b2", "story": "אשתו של אוריה החתי שדוד ראה רוחצת וחטא בגללה. לאחר מות אוריה נישאה לדוד, ובנה שלמה ירש את המלוכה. נביאת חסד ואם חכמה.", "scenes": []},
    "נתן": {"color": "#4338ca", "story": "הנביא הגדול בחצר דוד, שהוכיח אותו על חטא בת-שבע במשל כבשת הרש. הבטיח לדוד בית נאמן לעולם (נבואת נתן). עמד לצד שלמה בהמלכתו.", "scenes": []},
    "אבשלום": {"color": "#be123c", "story": "בן דוד היפה ביותר, שמרד באביו לאחר שדוד לא ענישו על אונס תמר. מרד כמעט הצליח אך נתלה בשיערו באלה ונהרג בידי יואב. דוד קונן עליו: \"בני אבשלום.\"", "scenes": []},
    "אמנון": {"color": "#854d0e", "story": "בכור דוד שאנס את אחותו תמר מאוהבה. דוד לא ענשו ואבשלום נקם את דמה ורצח אותו. מותו הוא שורש המשבר המשפחתי ומרד אבשלום.", "scenes": []},
    "תמר": {"color": "#86198f", "story": "בת דוד ואחות אבשלום, קורבן האונס של אמנון. ישבה שוממה בבית אחיה לאחר שדוד שתק. קולה הוא קול הדממה — \"אל תשלחני!\"", "scenes": []},
    "מפיבושת": {"color": "#065f46", "story": "בן יונתן שנפגע ברגליו בילדותו בבריחה מגלבוע. דוד הושיבו לשולחנו לכבוד ברית יונתן. עמד בניסיון כשעבדו ציבא הכפיש אותו, ועמד אמין לדוד.", "scenes": []},
    "שמואל": {"color": "#1e3a5f", "story": "הנביא האחרון מימי השופטים, שמשח את שאול ואחר כך את דוד. דחה את שאול מהמלוכה בשם ה'. מותו ציין קץ עידן השופטים.", "scenes": []},
    "אוריה": {"color": "#374151", "story": "הלוחם החתי, בעלה של בת-שבע, לוחם אמיץ ונאמן לדוד. סרב לשוב לביתו בזמן שאחיו במלחמה. דוד שלחו לחזית להיהרג — חטא דוד הגדול.", "scenes": []},
    "רצפה": {"color": "#be185d", "story": "פילגש שאול, שבניה הוצאו להורג ביד הגבעונים בתביעת נקם. שמרה על גופות בניה חודשים, יומם ולילה, עד שדוד שמע ולקחם לקבורה. סמל אהבת אם.", "scenes": []},
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
  --font-body: Arial, "Arial Hebrew", "Segoe UI", sans-serif;
  --font-ui: Arial, "Arial Hebrew", "Segoe UI", sans-serif;
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
#view-scenes {{ padding: 14px 20px; max-width: 820px; margin: 0 auto; }}

.scene-article {{
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  margin-bottom: 14px;
  overflow: hidden;
  scroll-margin-top: 10px;
}}
.scene-article.hidden {{ display: none; }}
.scene-header {{
  background: var(--bg2);
  border-bottom: 1px solid var(--border);
  padding: 8px 14px 7px;
  display: flex; flex-direction: column; gap: 3px;
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
  padding: 16px 24px;
  line-height: 1.65;
  font-size: .97rem;
  text-align: right;
}}
.md-h1,.md-h2,.md-h3,.md-h4,.md-h5,.md-h6 {{
  color: var(--accent); margin: .9em 0 .35em;
  font-family: var(--font-body);
  text-align: right;
}}
.md-h1 {{ font-size: 1.35rem; }}
.md-h2 {{ font-size: 1.18rem; }}
.md-h3 {{ font-size: 1.05rem; }}
.md-h4 {{ font-size: .97rem; }}
.md-p {{ margin: .25em 0; text-align: right; }}
.md-blockquote {{
  border-right: 3px solid var(--accent);
  padding: .25em .8em;
  margin: .4em 0;
  color: var(--fg2);
  font-style: italic;
  background: var(--bg2);
  border-radius: 0 6px 6px 0;
  text-align: right;
}}
.md-li {{ margin: .15em 0 .15em 1em; list-style: none; text-align: right; }}
.md-li::before {{ content: "•"; margin-left: .4em; color: var(--accent); }}
.md-hr {{ border: none; border-top: 1px solid var(--border); margin: .7em 0; }}
.md-table-row {{ color: var(--fg2); font-size: .88rem; margin: .15em 0; text-align: right; }}
.spacer {{ height: .15em; }}
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
  padding: 16px;
  overflow: auto;
  min-height: 100%;
  background: var(--bg);
}}
#view-tree h2 {{
  font-size: 1.3rem;
  color: var(--accent);
  margin-bottom: 10px;
  text-align: center;
}}
#tree-legend {{
  display: flex; gap: 20px; justify-content: center;
  margin-bottom: 12px; flex-wrap: wrap;
  font-family: var(--font-ui); font-size: .8rem; color: var(--fg2);
}}
.legend-item {{ display: flex; align-items: center; gap: 6px; }}
.legend-solid {{ display: inline-block; width: 30px; height: 2px; background: #888; }}
.legend-dashed {{ display: inline-block; width: 30px; height: 2px; border-top: 2px dashed #9333ea; }}
.legend-dotted {{ display: inline-block; width: 30px; height: 2px; border-top: 2px dotted #888; }}
#tree-scroll {{
  overflow-x: auto;
  overflow-y: auto;
  background: var(--bg2);
  border-radius: 10px;
  border: 1px solid var(--border);
  padding: 12px;
}}
.person-node {{ cursor: pointer; }}
.person-node rect {{ transition: filter .15s; }}
.person-node:hover rect {{ filter: brightness(1.2); }}
#tree-tooltip {{
  position: fixed;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 12px 16px;
  font-family: var(--font-ui);
  font-size: .88rem;
  color: var(--fg);
  z-index: 300;
  max-width: 300px;
  min-width: 200px;
  display: none;
  direction: rtl;
  box-shadow: 0 4px 20px rgba(0,0,0,.2);
  line-height: 1.5;
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

/* ── RELATIONS VIEW ── */
#view-relations {{
  padding: 16px;
  min-height: 100%;
  background: var(--bg);
}}
#view-relations h2 {{
  font-size: 1.3rem;
  color: var(--accent);
  margin-bottom: 10px;
  text-align: center;
}}
#rel-legend {{
  display: flex; gap: 10px; justify-content: center;
  margin-bottom: 12px; flex-wrap: wrap;
  font-family: var(--font-ui); font-size: .75rem; color: var(--fg2);
}}
.rel-legend-item {{
  display: flex; align-items: center; gap: 4px;
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 10px; padding: 2px 8px;
}}
.rel-legend-dot {{
  width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0;
}}
#rel-scroll {{
  overflow: auto;
  background: var(--bg2);
  border-radius: 10px;
  border: 1px solid var(--border);
  padding: 12px;
}}
.rel-node {{ cursor: pointer; }}
.rel-node circle {{ transition: r .15s, filter .15s; }}
.rel-node:hover circle {{ filter: brightness(1.2); }}
#rel-tooltip {{
  position: fixed;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px 14px;
  font-family: var(--font-ui);
  font-size: .85rem;
  color: var(--fg);
  z-index: 300;
  max-width: 280px;
  min-width: 180px;
  display: none;
  direction: rtl;
  box-shadow: 0 4px 20px rgba(0,0,0,.2);
  line-height: 1.5;
}}
.rel-filter-bar {{
  display: flex; gap: 6px; justify-content: center;
  margin-bottom: 10px; flex-wrap: wrap;
  font-family: var(--font-ui); font-size: .78rem;
}}
.rel-filter-btn {{
  padding: 3px 10px; border-radius: 12px; border: 1px solid;
  cursor: pointer; font-family: var(--font-ui); font-size: .76rem;
  transition: opacity .15s;
}}
.rel-filter-btn.off {{ opacity: .3; }}

/* ── SCROLLBAR ── */
#sidebar::-webkit-scrollbar, #main::-webkit-scrollbar {{ width: 6px; }}
#sidebar::-webkit-scrollbar-track, #main::-webkit-scrollbar-track {{ background: transparent; }}
#sidebar::-webkit-scrollbar-thumb, #main::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}

/* ── CHARACTERS VIEW ── */
.char-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; padding: 16px; }}
.char-card {{ background: var(--bg2); border-radius: 12px; padding: 20px; border-left: 4px solid var(--accent); cursor: pointer; transition: transform .15s; }}
.char-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,.15); }}
.char-card h3 {{ margin: 0 0 8px; font-size: 1.3rem; }}
.char-card p {{ margin: 0 0 10px; font-size: .88rem; color: var(--fg2); line-height: 1.6; }}
.char-scenes-label {{ font-size: .75rem; color: var(--fg3); }}
.char-scenes-label span {{ display: inline-block; background: var(--bg3,#e5e7eb); border-radius: 4px; padding: 1px 6px; margin: 2px; font-size: .7rem; }}
</style>
</head>
<body>

<!-- TOP BAR -->
<div id="topbar">
  <button class="topbar-btn" onclick="toggleSidebar()">☰</button>
  <h1>מזמור לדוד — המחזמר המלא</h1>
  <input type="text" id="search-input" placeholder="חיפוש בטקסט..." oninput="doSearch(this.value)">
  <button class="topbar-btn" onclick="showViewWrapped('scenes')">📜 סצנות</button>
  <button class="topbar-btn" onclick="showViewWrapped('tree')">🌳 אילן יוחסין</button>
  <button class="topbar-btn" onclick="showViewWrapped('structure')">🎭 מבנה דרמטי</button>
  <button class="topbar-btn" onclick="showViewWrapped('relations')">🕸 גרף קשרים</button>
  <button class="topbar-btn" onclick="showViewWrapped('chars')">👤 כרטיסי דמויות</button>
  <button class="topbar-btn" onclick="toggleCharFilter()">🎭 דמויות</button>
  <button class="topbar-btn" onclick="toggleTheme()">🌙</button>
  <button class="topbar-btn" onclick="exportAnnotations()">💾 ייצוא הערות</button>
</div>

<!-- LAYOUT -->
<div id="layout">

<!-- SIDEBAR -->
<nav id="sidebar">
  <div class="sidebar-special" onclick="showViewWrapped('tree')">🌳 אילן יוחסין</div>
  <div class="sidebar-special" onclick="showViewWrapped('structure')">🎭 מבנה דרמטי</div>
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
    <div id="tree-legend">
      <span class="legend-item"><span class="legend-solid"></span> הורה / ילד</span>
      <span class="legend-item"><span class="legend-dashed"></span> נישואים לדוד</span>
      <span class="legend-item"><span class="legend-dotted"></span> נישואים קודמים</span>
    </div>
    <div id="tree-scroll">
      <svg id="tree-svg" xmlns="http://www.w3.org/2000/svg"
           style="display:block;min-width:2060px;height:660px;">
        <!-- drawn by drawTree() in JS -->
      </svg>
    </div>
    <p style="text-align:center;color:var(--fg3);font-size:.78rem;margin-top:8px;font-family:var(--font-ui)">
      לחץ על כל דמות לסיפור קצר ולסצנות שבהן היא מופיעה
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
        <text x="95" y="205" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" fill="#333">משיחת דוד</text>
        <circle cx="185" cy="155" r="5" fill="#16a34a"/>
        <text x="185" y="245" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" fill="#333">ברית יונתן</text>
        <circle cx="268" cy="90" r="5" fill="#2563eb"/>
        <text x="268" y="250" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" fill="#333">המלכת דוד</text>
        <circle cx="350" cy="40" r="7" fill="#8b2500"/>
        <text x="350" y="255" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" fill="#8b2500" font-weight="bold">בת-שבע/אוריה</text>
        <circle cx="430" cy="90" r="5" fill="#be123c"/>
        <text x="430" y="245" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" fill="#333">מרד אבשלום</text>
        <circle cx="515" cy="145" r="5" fill="#374151"/>
        <text x="515" y="250" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" fill="#333">מות אבשלום</text>
        <circle cx="605" cy="185" r="5" fill="#047857"/>
        <text x="605" y="205" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" fill="#333">צוואה/שלמה</text>
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

  <!-- CHARACTERS VIEW -->
  <div id="view-chars" class="view">
    <h2 style="padding: 16px 16px 0; color: var(--accent);">דמויות המחזמר</h2>
    <div class="char-grid" id="char-cards-grid"></div>
  </div>

  <!-- RELATIONS VIEW -->
  <div id="view-relations" class="view">
    <h2>גרף קשרים — רגשות בין דמויות</h2>
    <div class="rel-filter-bar" id="rel-filter-bar"></div>
    <div id="rel-legend"></div>
    <div id="rel-scroll">
      <svg id="rel-svg" xmlns="http://www.w3.org/2000/svg"
           style="display:block;min-width:1100px;height:720px;"></svg>
    </div>
    <p style="text-align:center;color:var(--fg3);font-size:.76rem;margin-top:8px;font-family:var(--font-ui)">
      לחץ על דמות לפרטים · לחץ על סוג קשר לסינון
    </p>
  </div>

</main>
</div>

<!-- TOOLTIP -->
<div id="tree-tooltip"></div>
<div id="rel-tooltip"></div>

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
  buildCharCards();
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

function buildCharCards() {{
  const grid = document.getElementById('char-cards-grid');
  Object.entries(CHARS).forEach(([name, data]) => {{
    const card = document.createElement('div');
    card.className = 'char-card';
    card.style.borderLeftColor = data.color;
    const scenes = data.scenes || [];
    const scenePills = scenes.length
      ? scenes.map(s => `<span>${{s}}</span>`).join("")
      : "<span>—</span>";
    card.innerHTML = `<h3 style="color:${{data.color}}">${{name}}</h3><p>${{data.story || ""}}</p><div class="char-scenes-label">סצנות: ${{scenePills}}</div>`;
    card.onclick = () => {{
      showView('scenes');
      document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('on'));
      const chip = Array.from(document.querySelectorAll('.filter-chip')).find(c => c.textContent === name);
      if (chip) chip.classList.add('on');
      activeChar = name;
      applyCharFilter();
    }};
    grid.appendChild(card);
  }});
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

// ── FAMILY TREE ──
const TNODES = [
  // Row 0 — ancestors y=55
  {{id:'saul',    name:'שאול',      role:'מלך ישראל הראשון', cx:160,  cy:55,  c:'#dc2626', desc:'שאול בן קיש ממטה בנימין. נמשח ע"י שמואל, נדחה בגלל אי-ציות. רדף את דוד שנים רבות ונפל בגלבוע יחד עם יונתן בניו.'}},
  {{id:'jesse',   name:'ישי',       role:'אבי דוד',           cx:830,  cy:55,  c:'#b45309', desc:'ישי בן עובד מבית לחם, מזרע רות ובועז. אבי שמונה בנים — דוד הצעיר נמשח למלך כאשר שמואל דחה את כולם לפניו.'}},
  // Row 1 — main generation y=195
  {{id:'jonathan',  name:'יונתן',    role:'בן שאול',                  cx:55,   cy:195, c:'#16a34a', desc:'יונתן בן שאול — יורש העצר שויתר על כתרו. כרת ברית אהבה עם דוד, ואמר לו: "ואתה תמלוך". נפל בגלבוע עם אביו. דוד קינן: "נפלאתה אהבתך לי מאהבת נשים".'}},
  {{id:'michal',    name:'מיכל',     role:'בת שאול / אשת דוד',        cx:215,  cy:195, c:'#9333ea', desc:'מיכל בת שאול אהבה את דוד והצילה אותו דרך החלון. הוחזרה לדוד בכפייה, תוך שפלטיאל בעלה בוכה. בזה לדוד הרוקד לפני הארון — ומתה עקרה.'}},
  {{id:'ishbosh',   name:'אישבושת',  role:'בן שאול',                  cx:375,  cy:195, c:'#64748b', desc:'אישבושת (מלכי-בושת) בן שאול. מלך על ישראל 7 שנים בתמיכת אבנר, עד שנרצח על ידי בענה ורכב. דוד לא ידע על הרצח, ועינה את הרוצחים.'}},
  {{id:'merab',     name:'מרב',      role:'בת שאול',                  cx:525,  cy:195, c:'#78716c', desc:'מרב בת שאול — הובטחה לדוד אחרי גלית, אך נישאה לעדריאל המחלתי. חמישה מבניה נמסרו לגבעונים כפדיון דם.'}},
  {{id:'rizpah',    name:'רצפה',     role:'פילגש שאול',               cx:670,  cy:195, c:'#be185d', desc:'רצפה בת איה, פילגש שאול. שמרה על גופות שני בניה שנמסרו לגבעונים — מיממת הגשמים של ניסן עד ירידת הגשמים. מעשה זה הרגיש את דוד לקבור את שאול ויונתן.'}},
  {{id:'david',     name:'דוד המלך', role:'מלך יהודה וישראל',        cx:830,  cy:195, c:'#1d4ed8', desc:'דוד בן ישי — רועה שנמשח, גיבור, חוטא, מתחרט, משורר. מלך 40 שנה. כתב מזמורי תהילים מתוך כל שעה בחייו. חוט זהב: "כל עצירת יד מולידה כינור".',  main:true}},
  {{id:'zeruiah',   name:'צרויה',    role:'אחות דוד',                 cx:1000, cy:195, c:'#6b7280', desc:'צרויה אחות דוד ואם שלושת הגיבורים — יואב, אבישי ועשהאל. דוד אמר "קשים בני צרויה ממני" — היא מייצגת את הכוח שדוד לא יכול לרסן.'}},
  {{id:'ahinoam',   name:'אחינועם', role:'אשת דוד (א)',              cx:1180, cy:195, c:'#7c3aed', desc:'אחינועם היזרעאלית — אשתו הראשונה של דוד לאחר מיכל. ילדה לו את אמנון הבכור. הייתה עמו בגלות בגת ובצקלג.'}},
  {{id:'abigail',   name:'אביגיל',  role:'אשת דוד (ב)',              cx:1360, cy:195, c:'#ea580c', desc:'אביגיל אשת נבל הכרמלי — חכמה, יפה, ובעלת לשון. עצרה את דוד מלשפוך דם נבל. לאחר מותו נישאה לדוד. "ברוך ה׳ אלהי ישראל אשר שלחך היום".'}},
  {{id:'maacah',    name:'מעכה',    role:'אשת דוד (ג)',              cx:1550, cy:195, c:'#c026d3', desc:'מעכה בת תלמי מלך גשור, אשת דוד. ילדה לו את אבשלום ואת תמר. קשרי הנישואים לגשור אפשרו לאבשלום לברוח לשם אחרי רצח אמנון.'}},
  {{id:'haggith',   name:'חגית',    role:'אשת דוד (ד)',              cx:1730, cy:195, c:'#b45309', desc:'חגית אשת דוד, אם אדוניה. כמעט בנה אדוניה מלך לפני שלמה — אך בת-שבע ונתן הנביא הקדימו אותו אצל דוד הזקן.'}},
  {{id:'bathsheba', name:'בת-שבע',  role:'אשת דוד (ה)',              cx:1940, cy:195, c:'#0891b2', desc:'בת-שבע אשת אוריה החתי. נלקחה על ידי דוד שלח את אוריה למות. ילדה ארבעה בנים, מהם שלמה. נתן הנביא: "אתה האיש".'}},
  // Row 2 — grandchildren/nephews y=370
  {{id:'mephib',    name:'מפיבושת', role:'בן יונתן',                 cx:55,   cy:370, c:'#065f46', desc:'מפיבושת בן יונתן — נכה בשתי רגליו בגלל נפילה כשהיה בן חמש. דוד הזמינו לשלחנו לכל ימיו לזכות ברית יונתן. "ויאכל תמיד על שולחן המלך".'}},
  {{id:'joab',      name:'יואב',    role:'שר הצבא',                  cx:930,  cy:370, c:'#92400e', desc:'יואב בן צרויה — שר הצבא החזק. הרג את אבנר נקמה, את אבשלום בניגוד לפקודה. דוד: "ה׳ ישיב דמו בראשו" — ציוה לשלמה להרגו.'}},
  {{id:'abishai',   name:'אבישי',   role:'אח יואב',                  cx:1080, cy:370, c:'#78716c', desc:'אבישי בן צרויה — נאמן לדוד. רצה לשחוט את שמעי שקילל את דוד, אך דוד עצר אותו. הצילו מהפלשתי שרצה להכותו.'}},
  {{id:'asahel',    name:'עשהאל',   role:'אח יואב',                  cx:1230, cy:370, c:'#a8a29e', desc:'עשהאל בן צרויה — קל ברגליים כצבי. רדף אחרי אבנר ונהרג על ידו. מותו הצית את נקמת יואב שהרג את אבנר שנים לאחר מכן.'}},
  // Row 3 — David's children y=500
  {{id:'amnon',     name:'אמנון',   role:'בכור דוד (מאחינועם)',      cx:1180, cy:500, c:'#854d0e', desc:'אמנון בכור דוד מאחינועם. אנס את תמר אחותו למחצה ואחר כן שנאה שנאה גדולה. אבשלום נקם את כבוד תמר ורצח אותו שנתיים לאחר מכן.'}},
  {{id:'chileab',   name:'כלאב',    role:'בן דוד (מאביגיל)',         cx:1360, cy:500, c:'#7c6d5a', desc:'כלאב (דניאל בדה"א) בן דוד ואביגיל. כמעט לא מוזכר בכתוב — כנראה מת צעיר, או שהצניעות הגנה עליו מהמעורבות במאבקי הירושה.'}},
  {{id:'absalom',   name:'אבשלום',  role:'בן דוד (ממעכה)',           cx:1510, cy:500, c:'#be123c', desc:'אבשלום בן דוד ומעכה — יפה תואר. נקם את תמר אחותו, גלה, חזר, מרד ושכב עם פילגשי דוד על הגג. נהרג ע"י יואב. דוד: "בני בני אבשלום! מי יתן מותי אני תחתיך".'}},
  {{id:'tamar',     name:'תמר',     role:'בת דוד (ממעכה)',           cx:1660, cy:500, c:'#86198f', desc:'תמר בת דוד ומעכה — אחות אבשלום. נאנסה ע"י אמנון ואחר כך "ישבה שוממה בבית אבשלום אחיה". קולה נדם. אבשלום קרא לבתו "תמר" לזכרה.'}},
  {{id:'adonijah',  name:'אדוניה',  role:'בן דוד (מחגית)',           cx:1800, cy:500, c:'#374151', desc:'אדוניה בן דוד מחגית, יפה תואר אחרי אבשלום. ניסה למלוך לפני שלמה, אך שלמה הומלך תחתיו. לאחר מכן ביקש את אבישג ונהרג ע"י שלמה.'}},
  {{id:'solomon',   name:'שלמה',    role:'יורש המלכות (מבת-שבע)',    cx:1940, cy:500, c:'#047857', desc:'שלמה בן דוד ובת-שבע — יורש, בונה המקדש, המלך החכם. נתן הנביא קראו "ידידיה". שלמה = שלם = שלום. בנה את הבית שדוד חלם לבנות ולא הורשה.'}},
  // Row 4 — secondary figures y=590
  {{id:'samuel',    name:'שמואל',   role:'הנביא הגדול',              cx:150,  cy:590, c:'#1e3a5f', desc:'שמואל בן אלקנה — נביא ושופט. משח את שאול ואחר כך את דוד. ייצג את המעבר משופטים למלוכה. אפילו לאחר מותו קם מהאוב לנבא לשאול בעין-דור.'}},
  {{id:'nathan',    name:'נתן',     role:'הנביא',                    cx:330,  cy:590, c:'#4338ca', desc:'נתן הנביא — שלח לדוד את משל האיש העני ואמר "אתה האיש". ייצג הצפן המוסרי של המחזמר. גם מינה את שלמה וסייע לבת-שבע.'}},
  {{id:'doeg',      name:'דואג',    role:'עבד שאול / מלשין',         cx:505,  cy:590, c:'#7f1d1d', desc:'דואג האדומי, ראש רועי שאול. הלשין לשאול על אחימלך כהן נוב. שחט 85 כהנים. דוד כתב עליו תהילים נב: "מה תתהלל ברעה הגיבור — חסד ה׳ כל היום".'}},
  {{id:'shimei',    name:'שמעי',    role:'בן גרא הבנימיני',          cx:680,  cy:590, c:'#78350f', desc:'שמעי בן גרא ממשפחת שאול. קילל את דוד ואבק אבנים בו בשעת הבריחה. דוד: "ה׳ אמר לו קלל". סלח לו בשובו — אך בצוואה ציוה לשלמה לשלם לו.'}},
  {{id:'ahithophel',name:'אחיתופל',role:'היועץ הבוגד',               cx:1510, cy:590, c:'#1f2937', desc:'אחיתופל היועץ הנאמן שעבר לצד אבשלום. עצותיו נחשבו "כשאול ה׳". כשלא שמעו לו תלה עצמו. דוד ידע שבגד ואמר: "גם אתה אחיתופל" (תהילים נה).'}},
  {{id:'uriah',     name:'אוריה',   role:'החתי / בעל בת-שבע',       cx:1940, cy:590, c:'#44403c', desc:'אוריה החתי — לוחם נאמן ומסור. סירב לישון עם אשתו בשעה שהחיל במדינה. דוד שלח בידיו את גזר דינו. "נפלו מעבדי דוד — ויגוע גם אוריה החתי".'}}
];

const TEDGES = [
  // Saul → children (branch at y=125)
  {{t:'branch', from:'saul',      branch_y:125, children:['jonathan','michal','ishbosh','merab','rizpah']}},
  // Jesse → David + Zeruiah (branch at y=125)
  {{t:'branch', from:'jesse',     branch_y:125, children:['david','zeruiah']}},
  // Jonathan → Mephibosheth
  {{t:'parent', from:'jonathan', to:'mephib'}},
  // David ↔ Michal (marriage, dashed purple)
  {{t:'marriage', from:'michal', to:'david', color:'#9333ea'}},
  // David → wives (dashed from David up to each wife via line at y=155)
  {{t:'wives', david_cx:830, wives:['ahinoam','abigail','maacah','haggith','bathsheba'], bar_y:155}},
  // Zeruiah → sons
  {{t:'branch', from:'zeruiah', branch_y:283, children:['joab','abishai','asahel']}},
  // Children from each wife
  {{t:'parent', from:'ahinoam',   to:'amnon'}},
  {{t:'parent', from:'abigail',   to:'chileab'}},
  {{t:'branch', from:'maacah',    branch_y:430, children:['absalom','tamar']}},
  {{t:'parent', from:'haggith',   to:'adonijah'}},
  {{t:'parent', from:'bathsheba', to:'solomon'}},
];

function nodeById(id) {{ return TNODES.find(n => n.id===id); }}

function drawTree() {{
  const svg = document.getElementById('tree-svg');
  svg.innerHTML = '';
  const ns = 'http://www.w3.org/2000/svg';
  const W = 2060, H = 650;
  svg.setAttribute('viewBox', `0 0 ${{W}} ${{H}}`);

  function el(tag, attrs, text) {{
    const e = document.createElementNS(ns, tag);
    Object.entries(attrs).forEach(([k,v]) => e.setAttribute(k, v));
    if (text !== undefined) e.textContent = text;
    return e;
  }}
  function line(x1,y1,x2,y2,col,w,dash) {{
    const l = el('line', {{x1,y1,x2,y2,stroke:col||'#888','stroke-width':w||1.5}});
    if (dash) l.setAttribute('stroke-dasharray', dash);
    svg.appendChild(l);
  }}

  // Draw edges first (behind nodes)
  TEDGES.forEach(edge => {{
    if (edge.t === 'branch') {{
      const from = nodeById(edge.from);
      if (!from) return;
      const cxs = edge.children.map(id => nodeById(id)?.cx).filter(Boolean);
      if (!cxs.length) return;
      const minX = Math.min(...cxs), maxX = Math.max(...cxs);
      // Stem from parent down to branch_y
      line(from.cx, from.cy+22, from.cx, edge.branch_y, '#888', 2);
      // Horizontal bar
      line(minX, edge.branch_y, maxX, edge.branch_y, '#888', 1.5);
      // Down to each child
      edge.children.forEach(id => {{
        const ch = nodeById(id);
        if (ch) line(ch.cx, edge.branch_y, ch.cx, ch.cy-22, '#888', 1.5);
      }});
    }} else if (edge.t === 'parent') {{
      const from = nodeById(edge.from), to = nodeById(edge.to);
      if (!from || !to) return;
      if (from.cx === to.cx) {{
        line(from.cx, from.cy+22, to.cx, to.cy-22, '#888', 1.5);
      }} else {{
        // Elbow
        const midY = (from.cy+22 + to.cy-22) / 2;
        line(from.cx, from.cy+22, from.cx, midY, '#888', 1.5);
        line(from.cx, midY, to.cx, midY, '#888', 1.5);
        line(to.cx, midY, to.cx, to.cy-22, '#888', 1.5);
      }}
    }} else if (edge.t === 'marriage') {{
      const a = nodeById(edge.from), b = nodeById(edge.to);
      if (!a || !b) return;
      const x1 = Math.min(a.cx,b.cx)+60, x2 = Math.max(a.cx,b.cx)-60;
      const y = Math.min(a.cy,b.cy);
      const l = el('line', {{x1,y1:y,x2,y2:y,stroke:edge.color||'#9333ea','stroke-width':2}});
      l.setAttribute('stroke-dasharray','6,4');
      svg.appendChild(l);
    }} else if (edge.t === 'wives') {{
      // Horizontal bar at bar_y, from David right to last wife
      const lastWife = nodeById(edge.wives[edge.wives.length-1]);
      if (!lastWife) return;
      // Line from David top up to bar_y
      line(edge.david_cx, 195-22, edge.david_cx, edge.bar_y, '#0891b2', 1.5, '6,4');
      // Horizontal bar
      const wL = el('line', {{x1:edge.david_cx, y1:edge.bar_y, x2:lastWife.cx, y2:edge.bar_y, stroke:'#0891b2','stroke-width':1.5}});
      wL.setAttribute('stroke-dasharray','6,4');
      svg.appendChild(wL);
      // Down from bar to each wife
      edge.wives.forEach(id => {{
        const w = nodeById(id);
        if (w) {{
          const d = el('line', {{x1:w.cx, y1:edge.bar_y, x2:w.cx, y2:w.cy-22, stroke:'#0891b2','stroke-width':1.5}});
          d.setAttribute('stroke-dasharray','6,4');
          svg.appendChild(d);
        }}
      }});
    }}
  }});

  // Draw section labels
  [['שושלת שאול', 370, 16], ['משפחת ישי', 830, 16], ['נשות דוד', 1560, 16],
   ['נביאים ויועצים', 415, 580]].forEach(([txt, x, y]) => {{
    svg.appendChild(el('text', {{x, y, 'text-anchor':'middle', 'font-family':'Arial,sans-serif',
      'font-size':'11', fill:'#aaa', 'font-style':'italic'}}, txt));
  }});

  // Draw nodes
  TNODES.forEach(n => {{
    const g = document.createElementNS(ns, 'g');
    g.setAttribute('class','person-node');
    g.setAttribute('cursor','pointer');
    const w = n.main ? 150 : 120, h = 44;
    const rx = n.main ? 10 : 7;
    const rect = el('rect', {{
      x: n.cx-w/2, y: n.cy-h/2, width:w, height:h,
      fill: n.c, rx, ry:rx
    }});
    if (n.main) {{
      rect.setAttribute('stroke', '#fff');
      rect.setAttribute('stroke-width', '2');
    }}
    g.appendChild(rect);
    g.appendChild(el('text', {{
      x:n.cx, y:n.cy-5, 'text-anchor':'middle',
      'font-family':'Arial,sans-serif', 'font-size': n.main ? '14':'13',
      fill:'#fff', 'font-weight':'bold'
    }}, n.name));
    g.appendChild(el('text', {{
      x:n.cx, y:n.cy+11, 'text-anchor':'middle',
      'font-family':'Arial,sans-serif', 'font-size':'10',
      fill:'#ffffffcc'
    }}, n.role));
    g.addEventListener('click', (e) => {{ e.stopPropagation(); personClick(n, e); }});
    svg.appendChild(g);
  }});
}}

function personClick(n, evt) {{
  const tt = document.getElementById('tree-tooltip');
  if (tt.style.display==='block' && tt.dataset.person===n.id) {{
    tt.style.display='none'; return;
  }}
  const sceneList = CHARS[n.name] ? CHARS[n.name].scenes : [];
  const sceneLinks = sceneList.map(id => {{
    const s = SCENES.find(x => x.id===id);
    return s ? `<a href="#" onclick="jumpToScene('${{id}}');return false" style="color:var(--accent)">${{s.label}}</a>` : '';
  }}).filter(Boolean).join(', ');
  tt.innerHTML = `
    <div style="font-size:1rem;font-weight:bold;color:var(--accent);margin-bottom:4px">${{n.name}}</div>
    <div style="font-size:.8rem;color:var(--fg3);margin-bottom:8px">${{n.role}}</div>
    <div style="font-size:.88rem;line-height:1.55">${{n.desc}}</div>
    ${{sceneLinks ? `<div style="font-size:.8rem;margin-top:8px;border-top:1px solid var(--border);padding-top:6px"><strong>מופיע/ה בסצנות:</strong> ${{sceneLinks}}</div>` : ''}}
    <div style="font-size:.72rem;color:var(--fg3);margin-top:6px">לחץ שוב לסגירה</div>
  `;
  tt.style.display='block';
  tt.dataset.person=n.id;
  const margin = 16;
  let top = (evt?.clientY || 300) + 10;
  let left = (evt?.clientX || 400) - 150;
  if (left < margin) left = margin;
  if (left + 310 > window.innerWidth - margin) left = window.innerWidth - 310 - margin;
  if (top + 250 > window.innerHeight - margin) top = (evt?.clientY || 300) - 260;
  tt.style.top = top + 'px';
  tt.style.left = left + 'px';
  tt.style.right = 'auto';
}}

document.addEventListener('click', e => {{
  const tt = document.getElementById('tree-tooltip');
  if (!e.target.closest('.person-node') && !e.target.closest('#tree-tooltip')) {{
    tt.style.display = 'none';
  }}
}});

// Draw tree when view-tree becomes visible
const _origShowView = showView;
function showViewWrapped(name) {{
  _origShowView(name);
  if (name === 'tree') drawTree();
  if (name === 'relations') {{ if (!relDrawn) drawRelations(); relDrawn=true; }}
}}

// ── RELATIONS GRAPH ──
let relDrawn = false;
let activeRelTypes = new Set();

const REL_TYPES = {{
  'אהבה':         {{color:'#ec4899', emoji:'💗'}},
  'אהבת אב':      {{color:'#8b5cf6', emoji:'💜'}},
  'ידידות':       {{color:'#3b82f6', emoji:'🤝'}},
  'קנאה':         {{color:'#f97316', emoji:'🔶'}},
  'שנאה':         {{color:'#dc2626', emoji:'🔴'}},
  'נקמה':         {{color:'#7f1d1d', emoji:'💢'}},
  'בגידה':        {{color:'#111827', emoji:'🖤'}},
  'כבוד':         {{color:'#d97706', emoji:'🌟'}},
  'אשמה':         {{color:'#7c3aed', emoji:'😔'}},
  'תאווה':        {{color:'#db2777', emoji:'🔥'}},
  'הכרת טובה':   {{color:'#10b981', emoji:'🙏'}},
  'נאמנות':       {{color:'#047857', emoji:'🛡'}},
  'כעס':          {{color:'#b91c1c', emoji:'😠'}},
  'תלות':         {{color:'#92400e', emoji:'⛓'}},
  'ביקורת':       {{color:'#4338ca', emoji:'⚡'}},
  'אבל':          {{color:'#6b7280', emoji:'😢'}},
  'בוז':          {{color:'#78716c', emoji:'👎'}},
  'תאווה→שנאה':  {{color:'#9f1239', emoji:'💔'}},
}};

const RNODES = [
  // ring:-1=center, ring:0=inner(r=210), ring:1=outer(r=340)
  {{id:'david',        name:'דוד',       c:'#1d4ed8', ring:-1}},
  {{id:'nathan',       name:'נתן',       c:'#4338ca', ring:0, a:270}},
  {{id:'saul',         name:'שאול',      c:'#dc2626', ring:0, a:315}},
  {{id:'jonathan',     name:'יונתן',     c:'#16a34a', ring:0, a:0}},
  {{id:'michal',       name:'מיכל',      c:'#9333ea', ring:0, a:45}},
  {{id:'absalom',      name:'אבשלום',    c:'#be123c', ring:0, a:90}},
  {{id:'joab',         name:'יואב',      c:'#92400e', ring:0, a:135}},
  {{id:'ahithophel',   name:'אחיתופל',   c:'#1f2937', ring:0, a:180}},
  {{id:'abigail',      name:'אביגיל',    c:'#ea580c', ring:0, a:225}},
  {{id:'bathsheba',    name:'בת-שבע',    c:'#0891b2', ring:1, a:330}},
  {{id:'uriah',        name:'אוריה',     c:'#44403c', ring:1, a:290}},
  {{id:'amnon',        name:'אמנון',     c:'#854d0e', ring:1, a:30}},
  {{id:'tamar',        name:'תמר',       c:'#86198f', ring:1, a:70}},
  {{id:'mephibosheth', name:'מפיבושת',   c:'#065f46', ring:1, a:355}},
  {{id:'shimei',       name:'שמעי',      c:'#78350f', ring:1, a:155}},
  {{id:'rizpah',       name:'רצפה',      c:'#be185d', ring:1, a:200}},
];

// dir: 'fwd'=arrow from→to, 'bwd'=arrow to→from, 'both'=bidirectional, 'none'=undirected
const REDGES = [
  {{f:'david',      t:'jonathan',     type:'אהבה',        dir:'both', note:'ידידות עמוקה; יונתן ויתר על כתרו; "נפלאתה אהבתך לי"'}},
  {{f:'david',      t:'saul',         type:'כבוד',         dir:'fwd',  note:'דוד לא נגע במשיח ה׳ גם כשיכל להורגו'}},
  {{f:'saul',       t:'david',        type:'קנאה',         dir:'fwd',  note:'"שאול הכה באלפיו ודוד ברבבותיו" — הקנאה הרסה את שאול'}},
  {{f:'david',      t:'michal',       type:'אהבה',         dir:'fwd',  note:'אהבה ראשונה; היא הצילה אותו מחלון; הוחזרה בכפייה'}},
  {{f:'michal',     t:'david',        type:'בוז',          dir:'fwd',  note:'"ותבז לו בלבה" — בזה לו הרוקד לפני הארון; מתה עקרה'}},
  {{f:'david',      t:'bathsheba',    type:'תאווה',        dir:'fwd',  note:'ראה אותה רוחצת; שלח ולקחה; "ותבוא אליו" — כפייה?'}},
  {{f:'david',      t:'uriah',        type:'אשמה',         dir:'fwd',  note:'שלח בידיו את גזר דינו; "הדבר אשר עשה דוד רע"'}},
  {{f:'uriah',      t:'david',        type:'נאמנות',       dir:'fwd',  note:'"לא ארד אל ביתי" — נאמן לחיל בעוד דוד בוגד בו'}},
  {{f:'david',      t:'absalom',      type:'אהבת אב',      dir:'fwd',  note:'"בני בני אבשלום! מי יתן מותי אני תחתיך"'}},
  {{f:'absalom',    t:'david',        type:'כעס',          dir:'fwd',  note:'2 שנים לא ראה פני המלך; שרף שדה יואב; מרד'}},
  {{f:'david',      t:'joab',         type:'תלות',         dir:'fwd',  note:'יואב עשה את המלאכה המלוכלכת שדוד לא יכל לעשות'}},
  {{f:'joab',       t:'david',        type:'נאמנות',       dir:'fwd',  note:'נאמנות קרה ומניפולטיבית — "אני מגן עליך גם ממך"'}},
  {{f:'david',      t:'nathan',       type:'כבוד',         dir:'fwd',  note:'קיבל את ה"אתה האיש" בתשובה ולא בכעס'}},
  {{f:'nathan',     t:'david',        type:'ביקורת',       dir:'fwd',  note:'משל האיש העני — ביקורת נבואית ישירה'}},
  {{f:'david',      t:'abigail',      type:'אהבה',         dir:'both', note:'ראה בה חכמה; היא עצרה אותו מרצח; הוא שלח לה מייד'}},
  {{f:'david',      t:'mephibosheth', type:'הכרת טובה',   dir:'fwd',  note:'חסד לזכר יונתן: "ויאכל תמיד על שולחן המלך"'}},
  {{f:'mephibosheth',t:'david',       type:'הכרת טובה',   dir:'fwd',  note:'"כמלאך האלהים" — הכרת טובה עמוקה ויראה'}},
  {{f:'saul',       t:'jonathan',     type:'כעס',          dir:'fwd',  note:'"בן נעוות המרדות!" — כעס על בחירת יונתן בדוד'}},
  {{f:'jonathan',   t:'saul',         type:'אהבה',         dir:'fwd',  note:'אהב את אביו אבל בחר בדוד; מרד שקט מתוך אמונה'}},
  {{f:'amnon',      t:'tamar',        type:'תאווה→שנאה',  dir:'fwd',  note:'"שנאה גדולה מאד" — אחרי האונס; מנגנון בושה'}},
  {{f:'absalom',    t:'amnon',        type:'נקמה',         dir:'fwd',  note:'שתק שנתיים, הרג בחגיגת הגזזים; "כי אמנון שנא את תמר"'}},
  {{f:'absalom',    t:'tamar',        type:'אהבת אב',      dir:'fwd',  note:'קרא לבתו תמר; "ישב שמם" — שמר עליה בביתו'}},
  {{f:'ahithophel', t:'david',        type:'בגידה',        dir:'fwd',  note:'עבר לאבשלום; "עצת אחיתופל כשאל ה׳"'}},
  {{f:'shimei',     t:'david',        type:'שנאה',         dir:'fwd',  note:'קילל, האבין, ואמר "צא צא איש הדמים"'}},
  {{f:'david',      t:'shimei',       type:'כבוד',         dir:'fwd',  note:'"ה׳ אמר לו קלל" — קיבל את הקללה כגזרת שמים'}},
  {{f:'joab',       t:'absalom',      type:'בוז',          dir:'fwd',  note:'הרג אותו בניגוד לפקודה; לא חשב לו לחטא'}},
  {{f:'rizpah',     t:'saul',         type:'אהבה',         dir:'fwd',  note:'שמרה על גופות בניה — אהבת אם ופילגש; 5 חודשי שמירה'}},
  {{f:'david',      t:'rizpah',       type:'אבל',          dir:'fwd',  note:'שמע על מסירותה ונרגש לקבור את שאול ויונתן'}},
];

function rNodeById(id) {{ return RNODES.find(n => n.id===id); }}

function drawRelations() {{
  const svg = document.getElementById('rel-svg');
  svg.innerHTML = '';
  const ns = 'http://www.w3.org/2000/svg';
  const W=1100, H=720, CX=550, CY=360, R0=210, R1=340;
  svg.setAttribute('viewBox', `0 0 ${{W}} ${{H}}`);

  // Compute node positions
  RNODES.forEach(n => {{
    if (n.ring===-1) {{ n.cx=CX; n.cy=CY; }}
    else {{
      const r = n.ring===0 ? R0 : R1;
      const rad = (n.a-90)*Math.PI/180;
      n.cx = Math.round(CX + r*Math.cos(rad));
      n.cy = Math.round(CY + r*Math.sin(rad));
    }}
  }});

  function mkEl(tag, attrs) {{
    const e = document.createElementNS(ns, tag);
    Object.entries(attrs).forEach(([k,v]) => e.setAttribute(k,v));
    return e;
  }}

  // Build legend + filter buttons
  const legend = document.getElementById('rel-legend');
  const filterBar = document.getElementById('rel-filter-bar');
  legend.innerHTML = '';
  filterBar.innerHTML = '';
  const typeSet = new Set(REDGES.map(e=>e.type));
  typeSet.forEach(type => {{
    const info = REL_TYPES[type] || {{color:'#888', emoji:'•'}};
    activeRelTypes.add(type);
    // legend
    const li = document.createElement('span');
    li.className = 'rel-legend-item';
    li.innerHTML = `<span class="rel-legend-dot" style="background:${{info.color}}"></span>${{info.emoji}} ${{type}}`;
    legend.appendChild(li);
    // filter button
    const btn = document.createElement('button');
    btn.className = 'rel-filter-btn';
    btn.textContent = info.emoji + ' ' + type;
    btn.style.borderColor = info.color;
    btn.style.color = info.color;
    btn.style.background = info.color + '15';
    btn.dataset.type = type;
    btn.onclick = () => {{
      if (activeRelTypes.has(type)) activeRelTypes.delete(type);
      else activeRelTypes.add(type);
      btn.classList.toggle('off', !activeRelTypes.has(type));
      updateEdgeVisibility();
    }};
    filterBar.appendChild(btn);
  }});

  // Track edge pairs for curve offset (to separate bidirectional)
  const pairCurve = {{}};

  // Draw edges
  REDGES.forEach((edge, i) => {{
    const a = rNodeById(edge.f), b = rNodeById(edge.t);
    if (!a || !b) return;
    const info = REL_TYPES[edge.type] || {{color:'#888'}};
    const key = [a.id,b.id].sort().join('|');
    if (!pairCurve[key]) pairCurve[key] = 0;
    const curveDir = pairCurve[key] % 2 === 0 ? 1 : -1;
    pairCurve[key]++;

    const dx = b.cx-a.cx, dy = b.cy-a.cy;
    const len = Math.sqrt(dx*dx+dy*dy);
    const nx = -dy/len, ny = dx/len;
    const curve = curveDir * Math.min(40, len*0.25);
    const mx = (a.cx+b.cx)/2 + nx*curve;
    const my = (a.cy+b.cy)/2 + ny*curve;

    // Path (quadratic bezier)
    const path = mkEl('path', {{
      d:`M ${{a.cx}} ${{a.cy}} Q ${{mx}} ${{my}} ${{b.cx}} ${{b.cy}}`,
      stroke: info.color,
      'stroke-width': '2.2',
      fill: 'none',
      opacity: '0.75',
      'marker-end': edge.dir!=='bwd' ? `url(#arr-${{CSS.escape(edge.type)}})` : 'none',
      'marker-start': edge.dir==='both' ? `url(#arr-rev-${{CSS.escape(edge.type)}})` : 'none',
    }});
    path.setAttribute('data-type', edge.type);
    path.setAttribute('class', 'rel-edge');

    // Label at midpoint
    const label = mkEl('text', {{
      x: Math.round((a.cx+b.cx)/2 + nx*curve*0.5 + nx*12),
      y: Math.round((a.cy+b.cy)/2 + ny*curve*0.5 + ny*12),
      'text-anchor': 'middle',
      'font-family': 'Arial,sans-serif',
      'font-size': '9.5',
      fill: info.color,
      'data-type': edge.type,
      class: 'rel-edge-label',
    }}, edge.type);

    // Hover for note
    const g = mkEl('g', {{'data-type': edge.type, class:'rel-edge-grp'}});
    // Invisible fat line for easier hover
    const hitLine = mkEl('path', {{
      d:`M ${{a.cx}} ${{a.cy}} Q ${{mx}} ${{my}} ${{b.cx}} ${{b.cy}}`,
      stroke:'transparent', 'stroke-width':'14', fill:'none',
      style:'cursor:pointer'
    }});
    hitLine.addEventListener('mouseenter', (evt) => showRelTooltip(edge, info, evt));
    hitLine.addEventListener('mouseleave', () => {{
      document.getElementById('rel-tooltip').style.display='none';
    }});
    g.appendChild(path);
    g.appendChild(label);
    g.appendChild(hitLine);
    svg.appendChild(g);
  }});

  // Arrow markers
  typeSet.forEach(type => {{
    const info = REL_TYPES[type] || {{color:'#888'}};
    const defs = svg.querySelector('defs') || (() => {{
      const d = mkEl('defs',{{}}); svg.insertBefore(d, svg.firstChild); return d;
    }})();
    // Forward arrow
    const m = mkEl('marker', {{
      id:`arr-${{type}}`, markerWidth:'8', markerHeight:'8',
      refX:'6', refY:'3', orient:'auto'
    }});
    const poly = mkEl('polygon', {{points:'0 0, 6 3, 0 6', fill:info.color}});
    m.appendChild(poly); defs.appendChild(m);
    // Reverse arrow
    const m2 = mkEl('marker', {{
      id:`arr-rev-${{type}}`, markerWidth:'8', markerHeight:'8',
      refX:'0', refY:'3', orient:'auto-start-reverse'
    }});
    const poly2 = mkEl('polygon', {{points:'0 0, 6 3, 0 6', fill:info.color}});
    m2.appendChild(poly2); defs.appendChild(m2);
  }});

  // Draw section ring labels
  svg.appendChild((() => {{
    const t = mkEl('text', {{x:CX, y:CY-R0-12, 'text-anchor':'middle',
      'font-family':'Arial,sans-serif','font-size':'10',fill:'#bbb','font-style':'italic'}});
    t.textContent='טבעת פנימית — דמויות מרכזיות';
    return t;
  }})());

  // Draw nodes (on top of edges)
  RNODES.forEach(n => {{
    const g = mkEl('g', {{class:'rel-node', cursor:'pointer'}});
    const isMain = n.ring===-1;
    const r = isMain ? 38 : (n.ring===0 ? 30 : 26);
    const circle = mkEl('circle', {{
      cx:n.cx, cy:n.cy, r, fill:n.c,
      stroke: isMain ? '#fff' : n.c,
      'stroke-width': isMain ? '3' : '1'
    }});
    g.appendChild(circle);
    // Name (split if long)
    const words = n.name.split('-');
    if (words.length > 1) {{
      words.forEach((w,i) => {{
        const t = mkEl('text', {{
          x:n.cx, y:n.cy-5+(i*13),
          'text-anchor':'middle','font-family':'Arial,sans-serif',
          'font-size': isMain?'13':'11', fill:'#fff','font-weight':'bold'
        }});
        t.textContent=w;
        g.appendChild(t);
      }});
    }} else {{
      const t = mkEl('text', {{
        x:n.cx, y:n.cy+4,
        'text-anchor':'middle','font-family':'Arial,sans-serif',
        'font-size': isMain?'14':'12', fill:'#fff','font-weight':'bold'
      }});
      t.textContent=n.name;
      g.appendChild(t);
    }}
    g.addEventListener('click', (e) => {{ e.stopPropagation(); showNodeRelations(n, e); }});
    svg.appendChild(g);
  }});
}}

function updateEdgeVisibility() {{
  document.querySelectorAll('.rel-edge-grp').forEach(g => {{
    const type = g.getAttribute('data-type');
    g.style.display = activeRelTypes.has(type) ? '' : 'none';
  }});
}}

function showRelTooltip(edge, info, evt) {{
  const tt = document.getElementById('rel-tooltip');
  const a = rNodeById(edge.f), b = rNodeById(edge.t);
  const arrow = edge.dir==='both' ? '⟷' : edge.dir==='bwd' ? '←' : '→';
  tt.innerHTML = `
    <div style="font-weight:bold;color:${{info.color}};margin-bottom:4px">
      ${{info.emoji}} ${{edge.type}}
    </div>
    <div style="font-size:.82rem;margin-bottom:6px">
      ${{a?.name}} ${{arrow}} ${{b?.name}}
    </div>
    <div style="font-size:.85rem;line-height:1.5">${{edge.note}}</div>
  `;
  tt.style.display='block';
  posTooltip(tt, evt);
}}

function showNodeRelations(n, evt) {{
  const tt = document.getElementById('rel-tooltip');
  const rels = REDGES.filter(e => e.f===n.id || e.t===n.id);
  const lines = rels.map(e => {{
    const info = REL_TYPES[e.type]||{{color:'#888',emoji:'•'}};
    const other = rNodeById(e.f===n.id ? e.t : e.f);
    const arrow = e.f===n.id ? '→' : '←';
    return `<div style="font-size:.8rem;margin:3px 0">
      <span style="color:${{info.color}}">${{info.emoji}} ${{e.type}}</span>
      <span style="color:var(--fg2)"> ${{arrow}} ${{other?.name}}</span>
    </div>`;
  }}).join('');
  tt.innerHTML = `
    <div style="font-weight:bold;color:${{n.c}};font-size:1rem;margin-bottom:8px">${{n.name}}</div>
    ${{lines || '<div style="color:var(--fg3)">אין קשרים מוגדרים</div>'}}
  `;
  tt.style.display='block';
  posTooltip(tt, evt);
}}

function posTooltip(tt, evt) {{
  const margin=16;
  let top = (evt?.clientY||300)+12;
  let left = (evt?.clientX||300)-150;
  if (left<margin) left=margin;
  if (left+300>window.innerWidth-margin) left=window.innerWidth-300-margin;
  if (top+250>window.innerHeight-margin) top=(evt?.clientY||300)-260;
  tt.style.top=top+'px'; tt.style.left=left+'px'; tt.style.right='auto';
}}

document.addEventListener('click', e => {{
  if (!e.target.closest('.rel-node') && !e.target.closest('#rel-tooltip') && !e.target.closest('.rel-edge-grp'))
    document.getElementById('rel-tooltip').style.display='none';
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
