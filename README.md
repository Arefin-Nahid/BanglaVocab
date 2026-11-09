# বাংলা শব্দভাণ্ডার (Bangla Vocab)

A single-page, offline-capable vocabulary trainer for Bangladesh BCS and other competitive exams.
All 2,360 entries come from `source/bengali_bcs_vocabulary.md`; nothing was added, translated or corrected.

## Run it

Open `index.html` in a browser. There is no server and no install step.
Progress is saved in the browser. When you sign in with Google (Settings → Profile), it is also saved to Firebase and shared between your phone and laptop. Setup: see `FIREBASE_SETUP.md`.
Fonts load from Google Fonts when online and fall back to system fonts offline.

## Folder layout

| Path | What it is |
|---|---|
| `index.html` | The finished site (data embedded). This is what you open or host. |
| `manifest.webmanifest`, `sw.js`, `icons/` | Make the site installable on a phone and usable offline |
| `FIREBASE_SETUP.md` | Step-by-step Firebase setup (Google sign-in, Firestore, rules, GitHub Pages) |
| `firestore.rules` | Security rules to paste in the Firebase console |
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
- **Scheduling:** SM-2 ease factor with a 3, 7, 14, 30 day ladder (Forgot = shown again, Hard = 3 days, Got it = 7 then 14), plus Leitner boxes.
- **Modes:** flashcards (with optional typed recall), MCQ, type-the-answer, weak-word practice.
- **Cloud sync:** Google sign-in, newest change per card wins, works offline and syncs later.
- **Daily plan:** new words per day come only from the "new words per day" setting; new words pause while 60 or more reviews are waiting.

## Publish on GitHub Pages

Push the repository, then in GitHub: Settings → Pages → Deploy from branch → `main` → `/ (root)`.
Sign-in only works on the hosted site (or `localhost`), not when `index.html` is opened as a file.

## Install on your phone

After the site is live on GitHub Pages (https://arefin-nahid.github.io/BanglaVocab/):

- **Android (Chrome):** open the site → menu (⋮) → **Install app** (or **Add to Home screen**). Settings inside the app also has an Install button.
- **iPhone (Safari):** open the site → Share button → **Add to Home Screen**.

The installed app opens full screen and works offline. Progress is saved on the phone; sign in with Google to sync it.

When you push a new version, installed apps pick it up the next time they are opened with internet.
To force every phone to drop old cached files, change `CACHE = 'bangla-vocab-v1'` in `sw.js` (for example to `v2`).
