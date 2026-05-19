# SafariBooks

Download and generate *EPUB* files from your [O'Reilly Learning](https://learning.oreilly.com) library.

> **For personal and educational use only.** Please read O'Reilly's [Terms of Service](https://learning.oreilly.com/terms/) before use.

---

## Overview

- [Requirements & Setup](#requirements--setup)
- [Authentication](#authentication)
- [Usage](#usage)
- [Calibre EPUB conversion](#calibre-epub-conversion)

---

## Requirements & Setup

Requires Python 3.12+ and `pip3` or `pipenv`.

```shell
git clone https://github.com/rock-yu/safaribooks.git
cd safaribooks/

pip3 install -r requirements.txt
# OR
pipenv install && pipenv shell
```

Dependencies:

```
lxml>=5.0.0
requests>=2.32.0
```

---

## Authentication

Direct credential login no longer works due to O'Reilly API changes. Use the cookie-based flow instead:

1. Log in to [learning.oreilly.com](https://learning.oreilly.com) in your browser.
2. Copy your session cookies into `cookies.json` in the project root, **or** run the helper script:

```shell
uv run --with browser_cookie3 python retrieve_cookies.py
```

The helper reads cookies directly from your default browser profile and writes `cookies.json` automatically.

> ⚠️ Keep `cookies.json` private — it grants full access to your account session.

---

## Usage

```shell
python3 safaribooks.py <BOOK ID>
```

The book ID is the numeric string in the O'Reilly URL:
`https://learning.oreilly.com/library/view/book-name/XXXXXXXXXXXXX/`

#### Options

```
usage: safaribooks.py [--cred <EMAIL:PASS> | --login] [--no-cookies]
                      [--kindle] [--preserve-log] [--help]
                      <BOOK ID>

positional arguments:
  <BOOK ID>            Book digits ID to download.

optional arguments:
  --cred <EMAIL:PASS>  Credentials for auth login.
  --login              Prompt for credentials interactively.
  --no-cookies         Do not save session cookies to cookies.json.
  --kindle             Add CSS rules to block overflow on table/pre elements
                       (recommended for Kindle export).
  --preserve-log       Keep the info log file even when there are no errors.
  --help               Show this help message.
```

You can configure a proxy via the `HTTPS_PROXY` environment variable or the `USE_PROXY` constant in `safaribooks.py`.

---

## Calibre EPUB conversion

The script produces a raw EPUB. For best results on e-readers, convert it with [Calibre](https://calibre-ebook.com/):

```bash
ebook-convert "Books/<title>/<id>.epub" "Books/<title>/<id>_CLEAR.epub"
```

For Kindle export, use `--kindle` when downloading, then convert to AZW3/MOBI in Calibre with **Ignore margins** selected.

---

## Credits

Originally created by [Lorenzo Di Fuccia](https://github.com/lorenzodifuccia).
This fork continues development from that foundation.
