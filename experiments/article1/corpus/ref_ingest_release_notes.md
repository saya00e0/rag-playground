# Harborline Ingest Service Release Notes

Fictional evaluation document; it describes no real organization, person, or product.

## 4.13.2 (2026-08-19)

- Fixed: the dedupe window was ignored for records whose key contained non-ASCII characters (HLN-2340).
- Changed: the default of ingest.flush_interval_ms was lowered from 2000 to 1000.

## 4.13.0 (2026-07-30)

- Added: the export.max_batch_bytes setting.
- Added: the --since-cursor option for hlctl export.

## 4.12.3 (2026-07-08)

- Fixed: the retry delay could exceed ingest.retry_backoff_max_ms when the host clock was adjusted during a retry (HLN-2291).
- Security: upgraded the bundled TLS library.

## 4.12.0 (2026-06-10)

- Added: the --dry-merge option for hlctl import.
- Deprecated: the --merge-preview option, which will be removed in 5.0.

## 4.1.23 (2025-02-14, legacy branch)

- Fixed: a memory leak in the CSV parser when a file ended without a newline (HLN-1123).
