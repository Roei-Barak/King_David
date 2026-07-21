# תוכנית אצוות — קו ייצור המהדורה השלמה (`edition-v1/`)

> סוכני Sonnet כותבים → Fable מבקר ומתקן → המשתמש מכריע. הקאנון (`scenes/`, `songs/`) לא נגעת עד הכרעה.

## מיפוי תמונה → קבצים

| אצווה | תמונה | סצנה קנונית | workshop | station | שירים לכתוב |
|---|---|---|---|---|---|
| פיילוט | 6 קינת הנפילה | scene-06-lament.md | scene-06-lament-workshop.md | station-06* | #11 בעין דור (קיים בסצנה 05b — בדיקה בלבד) |
| פיילוט | — | — | — | — | #2 מוזר הייתי לאחי |
| א' | פרולוג | prologue.md | prologue-workshop.md | station-01,02 | — |
| א' | 1 | scene-01-05-full (ח"1) | scene-01-05-full-workshop | station-01 | #2 ✦פיילוט |
| א' | 2 | scene-01-05-full (ח"2) | ״ | station-02 | #3, #4, #5 |
| א' | 3 | scene-01-05-full (ח"3) | ״ | station-03 | #6 ברית אחים |
| א' | 4 | scene-01-05-full (ח"4) + scene-04* | scene-04*-workshop | station-04 | #8 חצי הפרדה |
| א' | 5 | scene-01-05-full (ח"5) + gibeat-hachila-full | ״ | station-05 | #9, #10 |
| ב' | מונטאז'+6 | scene-05b-witch-endor, gilboa, 06-lament | תואמים | station-06 | #11 (בדיקה), #12 מאושר |
| ב' | 7 | scene-07-brothers-war, ishbosheth | תואמים | station-07 | #13 קינה על אבנר, #23 ✅ |
| ב' | 8 | scene-08-dance, jerusalem | תואמים | station-08 | #7, #14, #15 |
| ב' | 9 | scene-09-not-you | תואם | station-09 | #16 |
| ב' | 10 | scene-10-mephibosheth | תואם | — | #17 |
| ג' | 11–12 | scene-bathhouse, bathsheba-uriah, water-libation | תואמים | station-10 | #18 (קיים — בדיקה) |
| ג' | 13א | (בתוך bathsheba-uriah) | ״ | station-10 | #19 חטאתי (טיוטה קיימת) |
| ג' | 13ב | scene-13b-amnon-tamar | תואם | station-11 | — (אין שיר, הכרעה קיימת) |
| ד' | 13ג | scene-13c-revolt | תואם | station-12 | #20 ממעמקים |
| ד' | 13ד | scene-13d-absalom (+13e,13f,13g) | תואמים | station-12 | #21 בני אבשלום |
| ד' | 14 | scene-14-hallelujah | תואם | — | #22 מעודכן (בדיקה) |
| ד' | 15 | scene-15-testament, 22-23-david-song | תואמים | — | רפריז #23 ✅ |

סצנות-גשר (נבל ואביגיל, גת, צקלג, צרויה-דוד, שבע בן בכרי, רצפה...) משולבות באצווה של התמונה הסמוכה להן.

## תהליך לכל אצווה
1. סוכן Sonnet לכל תמונה (פרומפט: `agent-prompt-scene.md`) → `edition-v1/scene-XX.md`
2. סוכן Sonnet לכל שיר חסר (פרומפט: `agent-prompt-song.md`) → `edition-v1/songs/song-XX.md`
3. ביקורת Fable לכל תוצר: שפה, מקורות, ארבע השפות, שלמות מול הקנון — תיקון ישיר בקובץ
4. commit + דוח למשתמש: מה נבנה, רשימת `[הכרעה נדרשת]` ו-`[לאמת]`
5. הכרעת המשתמש → אצווה הבאה

## שער יציאה (שלב 3)
`edition-v1/00-full-play.md` מורכב מכל הסצנות ברצף + הרצת check-muzmar על המהדורה + בניית web.
