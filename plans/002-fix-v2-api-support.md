# 002 — Fix v2 API support for newer ISBN-13 (979-prefix) books

## Problem
Books with 979-prefix ISBNs (e.g. `9798341640368`) return HTTP 404 from the
legacy v1 API (`/api/v1/book/{id}/`). The script crashed with a `JSONDecodeError`
because it called `response.json()` on the 404 HTML response.

## Root cause
O'Reilly migrated newer publications to a v2 epubs API:
```
GET /api/v2/epubs/urn:orm:book:{id}/          ← book metadata
GET /api/v2/epubs/urn:orm:book:{id}/table-of-contents/  ← TOC / chapter list
```
Chapter HTML content is still served from the v1 endpoint:
```
GET /api/v1/book/{id}/chapter/{filename}      ← still works ✅
```

## Solution (implemented in commit e796f70)
- `get_book_info()`: detect 404 → retry via v2, set `self.api_version = 2`
- `_normalize_v2_book_info()`: map v2 JSON to the v1-compatible schema
- `get_book_chapters()`: delegate to `_get_book_chapters_v2()` for v2 books
- `_get_book_chapters_v2()` + `_collect_chapters_v2()`: build chapter list
  from the v2 TOC; deduplicate by filename
- `_normalize_v2_toc_entry()`: convert v2 TOC entries to v1 format for `parse_toc()`
- `create_toc()`: use cached `self._v2_toc` when `api_version == 2`

## Checklist
- [x] Identified correct v2 API endpoints
- [x] Implemented fallback in `get_book_info()`
- [x] Implemented v2 chapter list via `_get_book_chapters_v2()`
- [x] Implemented v2 TOC normalisation for `create_toc()`
- [x] Smoke-tested CLI loads without errors
- [x] Committed and pushed (e796f70)
- [ ] End-to-end test with fresh cookies (cookies expire ~1 hour)

## Known limitations
- Author / publisher metadata is not available in the v2 book info response.
  The generated EPUB will have an empty `<dc:creator>` field for v2 books.
