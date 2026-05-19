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
| `requests` | HTTP client | 2.27.1 |
| `lxml` | HTML/XML parse + EPUB build | 5.4.0 |
| `urllib3` | Transitive via requests; pinned directly in Pipfile | 1.26.20 |
| `certifi` | CA bundle (transitive) | 2025.4.26 |
| `charset-normalizer` | Encoding detection (transitive) | 2.0.12 |
| `idna` | Internationalised domain names (transitive) | 3.10 |

## Python version

- **Declared**: Python 3.6 (Pipfile + Pipfile.lock `_meta`)
- **Runtime**: Any modern `python3` works at the script level — 3.6 is EOL

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

## Active work

See [`UPGRADE.md`](./UPGRADE.md) for the in-progress Python stack upgrade plan and checklist.

---

## Conventions & notes

- No test suite exists; validation is done via `--help` and manual smoke tests
- No build system — the project is a single script, no compilation step
- `cookies.json`, `Books/`, and `*.log` files are runtime artefacts (see `.gitignore`)
- Windows is partially supported (`WinQueue` workaround); ANSI colour codes are disabled on Windows
- The `USE_PROXY` / `PROXIES` constants at the top of `safaribooks.py` are debug-only toggles
