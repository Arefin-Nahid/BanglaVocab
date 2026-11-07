# BCS শব্দভাণ্ডার (BCS Vocabulary Trainer)

A single-page, offline-capable vocabulary trainer for Bangladesh BCS and other competitive exams.
All 2,360 entries come from `source/bengali_bcs_vocabulary.md`; nothing was added, translated or corrected.

## Run it

Open `index.html` in a browser. There is no server and no install step.
Progress is saved in the browser's localStorage (Settings has a copy/paste backup for moving to another device).
Fonts load from Google Fonts when online and fall back to system fonts offline.

## Folder layout

| Path | What it is |
|---|---|
| `index.html` | The finished site (data embedded). This is what you open or host. |
| `src/app.template.html` | The app (HTML, CSS, JS) with `__DATA__` / `__REPORT__` placeholders |
| `source/bengali_bcs_vocabulary.md` | Your original Markdown, untouched |
| `data/data.json` | Extracted entries |
| `data/report.json` | Completeness report: rows in file vs extracted vs verified, unclear entries, repeated words |
| `tools/parse_vocab.py` | Extracts the Markdown into `data/` and verifies it |
| `tools/build.py` | Builds `index.html` from the template and `data/` |

## Rebuild after changing the Markdown or the app

```bash
python3 tools/parse_vocab.py   # prints per-section counts: in file / extracted / verified
python3 tools/build.py         # writes index.html
```

`parse_vocab.py` uses only the Python standard library.

## Data check (current file)

| Section | In file | Extracted | Verified |
|---|---|---|---|
| Synonyms | 80 | 80 | 80 |
| Synonym table | 128 | 128 | 128 |
| Antonyms | 366 | 366 | 366 |
| One-word substitution | 518 | 518 | 518 |
| Calls and sounds | 26 | 26 | 26 |
| Idioms | 508 | 508 | 508 |
| Idiom groups | 23 | 23 | 23 |
| Proverbs | 146 | 146 | 146 |
| Terminology | 565 | 565 | 565 |
| **Total** | **2360** | **2360** | **2360** |

"Verified" means each entry's text matches its source line character for character.
Six entries are marked unclear by the Markdown itself (`ধন`, `কুন্তলা`, `খেদ`, `রাম`, `ক্ষমা করার ইচ্ছা`, the first idiom group). They are kept as written and tagged in the app.
This confirms a match with the Markdown, not with the printed book.

## How studying works

- **New words:** read the day's batch as one numbered list (answers can be covered), then take a test on the same words.
- **Scheduling:** SM-2 ease factor with a 1, 3, 7, 14, 30 day ladder, plus Leitner boxes.
- **Modes:** flashcards (with optional typed recall), MCQ, type-the-answer, weak-word practice.
- **Planner:** daily new-word target from your study hours and measured speed; optional exam date check.

## Publish on GitHub Pages

Push the repository, then in GitHub: Settings → Pages → Deploy from branch → `main` → `/ (root)`.
