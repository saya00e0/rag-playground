# Harborline Ingest Service Configuration Reference

Fictional evaluation document; it describes no real organization, person, or product.

Each setting is listed with its default value and meaning.

- ingest.max_batch_size: default 500 records. Maximum number of records sent in one batch.
- ingest.max_batch_bytes: default 8 MiB. Maximum serialized size of one ingest batch.
- export.max_batch_bytes: default 32 MiB. Maximum serialized size of one export batch.
- ingest.retry_backoff_ms: default 250. Initial delay before retrying a failed batch.
- ingest.retry_backoff_max_ms: default 30000. Upper bound on the retry delay.
- ingest.retry_limit: default 6. Number of retries before a batch is moved to the dead-letter queue.
- ingest.dedupe_window_s: default 120. Window in which records with the same key are treated as duplicates.
- ingest.flush_interval_ms: default 1000. Maximum time a partial batch waits before it is sent.
- export.flush_interval_ms: default 5000. Maximum time a partial export batch waits before it is written.
