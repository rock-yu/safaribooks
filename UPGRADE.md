# Python Stack Upgrade

Tracking the upgrade of this repo from Python 3.6 + stale deps to a current, supported stack.

## Target versions

| Component | From | To |
|---|---|---|
| Python | 3.6 | 3.14 |
| requests | 2.27.1 | 2.34.2 |
| urllib3 | 1.26.20 | 2.7.0 |
| lxml | 5.4.0 | 6.1.1 |
| charset-normalizer | 2.0.12 (transitive) | 3.4.7 |
| certifi | 2025.4.26 (transitive) | 2026.4.22 |
| idna | 3.10 (transitive) | 3.15 |

## Checklist

- [x] **1. Bump Python version** — `Pipfile`: `python_version = "3.6"` → `"3.14"`
- [x] **2. Update requests floor** — `requirements.txt`: `>=2.20.0` → `>=2.32.0`
- [x] **3. Update urllib3 minimum** — `Pipfile`: `urllib3 = ">=1.26.5"` → `">=2.0.0"`
- [x] **4. Update lxml floor** — `requirements.txt`: `>=4.1.1` → `>=5.0.0`
- [x] **5. Code compatibility audit** — no direct urllib3 imports; no removed Python 3.12+ stdlib used; all clear
- [x] **6. Regenerate Pipfile.lock** — resolved against Python 3.14
- [x] **7. Smoke test** — `python3 safaribooks.py --help` passes cleanly

✅ **Upgrade complete.**

---

## Notes

- Python 3.12 was the original target but only 3.14 was available locally; upgraded to 3.14.
- `urllib3` 1.x → 2.x is a **major breaking change** but `safaribooks.py` uses only the `requests` high-level API — no direct `urllib3` imports, so no source changes were required.
- `lxml` 6.x requires Python ≥ 3.9 — satisfied by Python 3.14.
- `requests` 2.32+ requires Python ≥ 3.8 — satisfied by Python 3.14.
- `charset-normalizer` 3.x resolved automatically as a transitive dep of `requests`.
