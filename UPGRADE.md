# Python Stack Upgrade

Tracking the upgrade of this repo from Python 3.6 + stale deps to a current, supported stack.

## Target versions

| Component | From | To |
|---|---|---|
| Python | 3.6 | 3.12 |
| requests | 2.27.1 | ≥ 2.32.0 (latest: 2.34.2) |
| urllib3 | 1.26.20 | ≥ 2.0.0 (latest: 2.7.0) |
| lxml | 5.4.0 | ≥ 5.0.0 floor (latest: 6.1.1) |
| charset-normalizer | 2.0.12 (transitive) | 3.x (pulled in automatically) |

---

## Checklist

- [ ] **1. Bump Python version** — `Pipfile`: `python_version = "3.6"` → `"3.12"`
- [ ] **2. Update requests floor** — `requirements.txt`: `>=2.20.0` → `>=2.32.0`
- [ ] **3. Update urllib3 minimum** — `Pipfile`: `urllib3 = ">=1.26.5"` → `">=2.0.0"`
- [ ] **4. Update lxml floor** — `requirements.txt`: `>=4.1.1` → `>=5.0.0`
- [ ] **5. Code compatibility audit** — verify no removed Python 3.12 stdlib or urllib3 2.x API usage in source files
- [ ] **6. Regenerate Pipfile.lock** — `pipenv lock` under Python 3.12
- [ ] **7. Smoke test** — `python3 safaribooks.py --help` passes cleanly

---

## Notes

- `urllib3` 1.x → 2.x is a **major breaking change** but `safaribooks.py` uses only the `requests` high-level API — no direct `urllib3` imports were found, so no source changes are expected from this bump.
- `lxml` 6.x requires Python ≥ 3.9 — satisfied by the Python 3.12 target.
- `requests` 2.32+ requires Python ≥ 3.8 — satisfied by the Python 3.12 target.
- `charset-normalizer` 3.x will resolve automatically as a transitive dep of `requests`.
- No test suite exists; the smoke test (`--help`) plus a manual download attempt are the validation steps.
- `retrieve_cookies.py` has no dependency concerns — it imports only `json` (stdlib) and `browser_cookie3` (optional, installed on demand).

---

## Context

- **Why now**: Python 3.6 reached end-of-life in December 2021. `urllib3` 1.x is in security-fix-only mode.
- **Scope**: dependency metadata files only (`Pipfile`, `requirements.txt`, `Pipfile.lock`). No functional source changes expected.
- **Tracked in**: session SQL todos (7 items, ids: `python-version`, `requests-floor`, `urllib3-pipfile`, `lxml-floor`, `code-audit`, `lock-regen`, `smoke-test`)
