# הגנת מעברות פתיים: סרטון הסבר

סרטון באורך כ-15 דקות, בעברית, עם קריינות וכתוביות, על הספר "הגנת מעברות פתיים" מאת סר א.ד. סווינטון. הוא עובר על כל ששת החלומות ועל כל 22 השיעורים, ומסתיים בסיכום של שישה רעיונות גדולים.

- **הסרטון:** `out/duffers-drift.mp4` (1920×1080, 30fps)
- **התסריט המלא עם זמנים:** [`SCRIPT.md`](SCRIPT.md)

## איך זה בנוי

הסרטון נבנה עם [HyperFrames](https://github.com/heygen-com/hyperframes) (סקילים `hyperframes`, `hyperframes-cli`, `media-use`). כל סצנה היא קובץ HTML עם GSAP תחת `compositions/`, ו-`index.html` מרכיב אותן יחד עם הקריינות, המוזיקה והאפקטים. העיצוב נעשה לפי הסקיל `frontend-design`.

| שלב | קובץ | מה הוא עושה |
|---|---|---|
| 1 | `script/script.json` | התסריט. השדה `say` הוא הטקסט לקריין, עם ניקוד במילים קשות, והשדה `sub` הוא הכתובית. |
| 2 | `tools/tts.py` | מפיק קריינות עברית (edge-tts, קול `he-IL-AvriNeural`) עם זמני מילים. |
| 3 | `tools/build_timeline.py` | מניח כל משפט על ציר הזמן, מרכיב את `assets/audio/narration.mp3` ובונה כתוביות. |
| 4 | `tools/gen_art.py` + `tools/render_art.cjs` | מצייר את שולחן החול, לוח האבן והחותמות לתמונות ב-`assets/art/`. |
| 5 | `tools/gen.py` | כותב את `compositions/*.html` ואת `index.html` מתוך הסצנות (`tools/scenes_*.py`, `tools/blocks.py`, `tools/kit.py`). |
| 6 | `tools/build_music.py` | מרכיב את פס המוזיקה, כולל מעברים והנמכה מתחת לקריינות. |
| 7 | `tools/synth_sfx.py` | מסנתז אפקטים שלא היו זמינים בספריות חופשיות (יריות, אזמל, מדורה). |

לבנייה מחדש מריצים: `python tools/tts.py`, ‏`python tools/build_timeline.py`, ‏`python tools/gen.py`, ‏`python tools/build_music.py` ואז `npx hyperframes render`. לפני רינדור כדאי להריץ `npx hyperframes check`.

## קרדיטים

- הספר: "הגנת מעברות פתיים", סר א.ד. סווינטון, הוצאת מערכות. הכריכה והמפות מתוך הסריקה.
- מוזיקה: Kevin MacLeod ([incompetech.com](https://incompetech.com)), ברישיון CC BY 4.0. הרצועות: Investigations, Sneaky Snitch, Hidden Agenda, Thinking Music, Heroic Age, Achaidh Cheide.
- אפקטים: Freesound ו-Wikimedia Commons (CC0 ונחלת הכלל). יריות, אזמל, מדורה ושריקה סונתזו בקוד.
- גופנים: Karantina,‏ Frank Ruhl Libre ו-Rubik (SIL Open Font License).
- קריינות: קול סינתטי, Microsoft Edge TTS (Avri).

> הרצועות המקוריות של המוזיקה לא נשמרות בריפו (`assets/music/` ב-gitignore). כדי לבנות מחדש את `music.mp3`, מורידים אותן מ-`https://incompetech.com/music/royalty-free/mp3-royaltyfree/<שם>.mp3` לתיקייה `assets/music/` (שמות הקבצים מופיעים ב-`tools/build_music.py`).
