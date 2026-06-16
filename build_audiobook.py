#!/usr/bin/env python3
"""
build_audiobook.py — בונה אודיו בוק מסצנות המחזה "מזמור לדוד"
משתמש ב-espeak-ng עם קול עברי
"""

import os
import re
import subprocess
import wave
import struct
from pathlib import Path

BASE = Path("/home/user/King_David")
OUT  = BASE / "audiobook"
OUT.mkdir(exist_ok=True)

# סצנות לפי סדר המחזה (כותרת, שם קובץ)
SCENES = [
    ("פרולוג",                    "scenes/prologue.md"),
    ("תמונות א-ה — השנים הראשונות", "scenes/scene-01-05-full.md"),
    ("דוד בגת — המשוגע",          "scenes/scene-gath-madness.md"),
    ("טבח נוב — אנכי סבותי",      "scenes/scene-nob-massacre.md"),
    ("נבל ואביגיל",               "scenes/scene-nabal-abigail.md"),
    ("המדבר — תוספות",            "scenes/scene-04b-wilderness-additions.md"),
    ("המערה",                     "scenes/scene-04-the-cave.md"),
    ("אנדת עין-דור",               "scenes/scene-05b-witch-endor.md"),
    ("קינת דוד",                  "scenes/scene-06-lament.md"),
    ("מלחמת האחים",               "scenes/scene-07-brothers-war.md"),
    ("ריקוד הארון",               "scenes/scene-08-dance.md"),
    ("לא אתה — שלמה",             "scenes/scene-09-not-you.md"),
    ("מפיבושת",                   "scenes/scene-10-mephibosheth.md"),
    ("מלחמת עמון",                "scenes/scene-10b-ammon-war.md"),
    ("אמנון ותמר",                "scenes/scene-13b-amnon-tamar.md"),
    ("המרד — אבשלום",             "scenes/scene-13c-revolt.md"),
    ("מות אבשלום",                "scenes/scene-13d-absalom.md"),
    ("שיבת אבשלום",               "scenes/scene-13e-absalom-return.md"),
    ("שיבת דוד",                  "scenes/scene-13f-david-return.md"),
    ("רצפה",                      "scenes/scene-13g-rizpah.md"),
    ("הללויה",                    "scenes/scene-14-hallelujah.md"),
    ("הצוואה",                    "scenes/scene-15-testament.md"),
    ("צרויה ודוד",                "scenes/scene-tzruya-david.md"),
]

# ---- ניקוי טקסט ----

def strip_nikud(text):
    """הסרת ניקוד (U+0591–U+05C7)"""
    return re.sub(r'[֑-ׇ]', '', text)

def clean_text(raw):
    """מחלץ טקסט נקי מ-Markdown לקריאה בקול"""
    lines = raw.splitlines()
    out = []
    for line in lines:
        # דילוג על כותרות
        if line.startswith('#'):
            # שמור כותרת ראשית כהכרזה
            title = re.sub(r'^#+\s*', '', line).strip()
            title = re.sub(r'[—–\-].*', '', title).strip()
            if title:
                out.append(title + '.')
            continue
        # דילוג על הוראות בימוי *(...)* ו-*(טקסט)*
        line = re.sub(r'\*\([^)]*\)\*', '', line)
        line = re.sub(r'\*[^*]+\*', '', line)
        # דילוג על code blocks
        if line.strip().startswith('```') or line.strip().endswith('```'):
            continue
        # דילוג על הערות ---
        if re.match(r'^---+$', line.strip()):
            out.append('')
            continue
        # דילוג על שורות מטא (## הערות, ## מבנה)
        if re.search(r'הערות|מבנה|מקור:|זמן:|מיקום:|לחן:|מוסיקה:|מקורות:', line):
            continue
        # דילוג על שורות [לאמת] ועיגולים
        line = re.sub(r'\[לאמת[^\]]*\]', '', line)
        line = re.sub(r'\[[^\]]+\]', '', line)  # [הערת במאי]
        # הסרת bold/italic markers
        line = re.sub(r'\*+', '', line)
        line = re.sub(r'_{1,2}', '', line)
        # הסרת אמוג'י בסיסי
        line = re.sub(r'[🎵🎶🎼🎹🎸🎷🎺🎻🥁🪕]', '', line)
        # ניקוי שורות ריקות מרובות
        line = line.strip()
        if line:
            out.append(line)
        elif out and out[-1] != '':
            out.append('')

    return '\n'.join(out).strip()

# ---- יצור קול ----

ESPEAK_RATE  = 145   # מילים לדקה (קצב קריאה נוח)
ESPEAK_PITCH = 50    # גובה קול (0-99)

def text_to_wav(text, wav_path):
    """ממיר טקסט ל-WAV באמצעות espeak-ng"""
    clean = strip_nikud(text)
    # כתוב לקובץ זמני
    tmp_txt = str(wav_path) + ".txt"
    with open(tmp_txt, 'w', encoding='utf-8') as f:
        f.write(clean)
    cmd = [
        'espeak-ng',
        '-v', 'he',
        '-s', str(ESPEAK_RATE),
        '-p', str(ESPEAK_PITCH),
        '-f', tmp_txt,
        '-w', str(wav_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    os.unlink(tmp_txt)
    if result.returncode != 0:
        print(f"  ⚠ שגיאת espeak: {result.stderr[:200]}")
        return False
    return True

def concat_wavs(wav_paths, out_path):
    """מאחד קבצי WAV לקובץ אחד"""
    silence = b'\x00' * 22050 * 2  # ~0.5 שניות שקט בין סצנות (22050 Hz, 16-bit mono)

    out_frames = b''
    params = None

    for p in wav_paths:
        if not Path(p).exists():
            continue
        with wave.open(str(p), 'rb') as wf:
            if params is None:
                params = wf.getparams()
            out_frames += wf.readframes(wf.getnframes())
            out_frames += silence

    if params is None:
        return False

    with wave.open(str(out_path), 'wb') as wf:
        wf.setparams(params)
        wf.writeframes(out_frames)
    return True

# ---- ראשי ----

def main():
    print("בונה אודיו בוק — מזמור לדוד")
    print("=" * 40)

    scene_wavs = []

    for i, (title, rel_path) in enumerate(SCENES, 1):
        md_path = BASE / rel_path
        if not md_path.exists():
            print(f"  [{i:02d}] ⚠ חסר: {rel_path}")
            continue

        raw = md_path.read_text(encoding='utf-8')
        text = clean_text(raw)

        if not text.strip():
            print(f"  [{i:02d}] ⚠ טקסט ריק: {title}")
            continue

        safe_name = re.sub(r'[^\w֐-׿]', '_', title)[:30]
        wav_path = OUT / f"{i:02d}_{safe_name}.wav"

        print(f"  [{i:02d}] {title} ({len(text)} תווים)...", end=' ', flush=True)

        if text_to_wav(text, wav_path):
            size = wav_path.stat().st_size / 1024
            print(f"✓ {size:.0f}KB")
            scene_wavs.append(wav_path)
        else:
            print("✗")

    # קובץ אודיו שלם
    if scene_wavs:
        full_path = OUT / "מזמור-לדוד-מלא.wav"
        print(f"\nמאחד {len(scene_wavs)} סצנות לקובץ שלם...", end=' ', flush=True)
        if concat_wavs(scene_wavs, full_path):
            size_mb = full_path.stat().st_size / 1024 / 1024
            print(f"✓ {size_mb:.1f}MB")
        else:
            print("✗")

    # רשימת תוכן
    toc_path = OUT / "תוכן-עניינים.txt"
    with open(toc_path, 'w', encoding='utf-8') as f:
        f.write("מזמור לדוד — אודיו בוק\n")
        f.write("=" * 30 + "\n\n")
        for i, (title, _) in enumerate(SCENES, 1):
            f.write(f"{i:02d}. {title}\n")

    print(f"\nסיום. קבצים ב: {OUT}")
    print(f"סצנות שנוצרו: {len(scene_wavs)}/{len(SCENES)}")

if __name__ == '__main__':
    main()
