#!/usr/bin/env python3
"""
Convert Chrome DevTools request headers to cookies.json.

How to get the headers:
  1. Open https://learning.oreilly.com in Chrome while logged in.
  2. Open DevTools (F12) → Network tab.
  3. Click any request to learning.oreilly.com.
  4. Right-click the request → Copy → Copy request headers.
  5. Run this script and paste when prompted (then Ctrl+D / Ctrl+Z+Enter).

Usage:
    # Interactive paste:
    python3 headers_to_cookies.py

    # From a saved file:
    python3 headers_to_cookies.py headers.txt

    # From clipboard (macOS):
    pbpaste | python3 headers_to_cookies.py
"""

import json
import re
import sys
from pathlib import Path

COOKIES_FILE = Path(__file__).parent / "cookies.json"

AUTH_COOKIES = ("orm-jwt", "orm-rt")


def parse_cookie_header(text: str) -> dict:
    """Extract the Cookie: header and return a name→value dict."""
    match = re.search(r"(?im)^Cookie:\s*(.+)$", text)
    if not match:
        raise ValueError("No 'Cookie:' header found in the pasted text.")

    cookies: dict[str, str] = {}
    for part in match.group(1).strip().split("; "):
        name, sep, value = part.partition("=")
        if sep:
            cookies[name.strip()] = value.strip()
    return cookies


def main() -> None:
    if len(sys.argv) > 1:
        text = Path(sys.argv[1]).read_text(encoding="utf-8")
    else:
        print("Paste Chrome request headers below.")
        print("Press Ctrl+D (macOS/Linux) or Ctrl+Z then Enter (Windows) when done.\n")
        text = sys.stdin.read()

    try:
        cookies = parse_cookie_header(text)
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)

    COOKIES_FILE.write_text(json.dumps(cookies, indent=2), encoding="utf-8")
    print(f"✓ Saved {len(cookies)} cookies → {COOKIES_FILE}")

    for key in AUTH_COOKIES:
        if key in cookies:
            preview = cookies[key][:40]
            print(f"  {key}: {preview}…")
        else:
            print(f"  ⚠ '{key}' not found — authentication may fail.")


if __name__ == "__main__":
    main()
