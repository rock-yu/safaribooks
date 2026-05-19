# Agent Context — safaribooks

> Concise reference for AI agents and contributors working on this repo.

## What this project does

`safaribooks` downloads books from [O'Reilly Learning](https://learning.oreilly.com) (formerly Safari Books Online) and produces EPUB files locally.  
It is a **single-script CLI tool** (`safaribooks.py`) with a thin helper (`retrieve_cookies.py`) for extracting browser session cookies.

> ⚠️ The project is no longer actively maintained upstream. Direct login via credentials no longer works due to API changes. The download flow still works when you supply a valid `cookies.json` (copied from a live browser session).

---

## Repo layout

```
safaribooks.py          # Main CLI — all core logic lives here (~46 KB)
retrieve_cookies.py     # Helper: reads cookies from the browser via browser_cookie3
requirements.txt        # pip install path (lxml, requests floor pins)
Pipfile / Pipfile.lock  # pipenv path (includes urllib3 as direct dep)
cookies.json            # Runtime-generated session cookie store (gitignored)
Books/                  # Output directory for downloaded EPUBs
```

## Key source files

### `safaribooks.py`
- **`Display`** class — logging/output formatting, progress bar, ANSI colours
- **`SafariBooks`** class — HTTP session, login, API calls, chapter/CSS/image download, EPUB assembly
- **`WinQueue`** — Windows workaround for `multiprocessing.Queue` pickling issue
- Uses `multiprocessing.Process` + `Queue` for parallel chapter downloads
- Uses `requests.Session` for all HTTP; no direct `urllib3` import
- Uses `lxml.html` + `lxml.etree` for HTML/XML parsing and EPUB XML generation
- Cookies are stored to / loaded from `cookies.json`

### `retrieve_cookies.py`
- Optional helper; requires `browser_cookie3` (not in requirements.txt — installed on demand via `uv run --with browser_cookie3`)
- Loads all cookies from the default browser profile and dumps them to `cookies.json`

---

## Dependencies

| Package | Role | Current lock |
|---|---|---|
| `requests` | HTTP client | 2.34.2 |
| `lxml` | HTML/XML parse + EPUB build | 6.1.1 |
| `urllib3` | Pinned directly in Pipfile; transitively used by requests | 2.7.0 |
| `certifi` | CA bundle (transitive) | 2026.4.22 |
| `charset-normalizer` | Encoding detection (transitive) | 3.4.7 |
| `idna` | Internationalised domain names (transitive) | 3.15 |

## Python version

- **Declared**: Python 3.14 (Pipfile + Pipfile.lock `_meta`)

---

## How to run

```bash
# Install deps
pip3 install -r requirements.txt
# OR
pipenv install && pipenv shell

# Download a book (requires valid cookies.json)
python3 safaribooks.py 9781491958698

# Retrieve cookies from browser session
uv run --with browser_cookie3 python retrieve_cookies.py

# Help
python3 safaribooks.py --help
```

---

## Working with plans

All plans live in the [`plans/`](./plans/) directory. Plans are numbered sequentially with a zero-padded prefix (e.g. `001-`, `002-`).

### Agent instructions

1. **Always check for open plans first.** Before starting any new work, scan `plans/` for plan files whose checklist contains unchecked items (`- [ ]`). Resume the oldest incomplete plan before creating a new one.

   ```bash
   grep -rl "- \[ \]" plans/
   ```

2. **Creating a new plan.** Determine the next sequence number (`ls plans/ | sort | tail -1`), then create the file as `plans/NNN-short-description.md`. Follow this template:

   ```markdown
   # <Title>

   ## Goal
   <One-paragraph description of what this plan achieves and why.>

   ## Checklist
   - [ ] Step one
   - [ ] Step two
   ...

   ## Notes
   <Risks, decisions, context.>
   ```

3. **Tick items as you complete them** — change `- [ ]` to `- [x]` in the plan file and commit the update alongside the work.

---

## Conventions & notes

- No test suite exists; validation is done via `--help` and manual smoke tests
- No build system — the project is a single script, no compilation step
- `cookies.json`, `Books/`, and `*.log` files are runtime artefacts (see `.gitignore`)
- Windows is partially supported (`WinQueue` workaround); ANSI colour codes are disabled on Windows
- The `USE_PROXY` / `PROXIES` constants at the top of `safaribooks.py` are debug-only toggles
