# hlctl Command-Line Reference

Fictional evaluation document; it describes no real organization, person, or product.

hlctl is the command-line client for the Harborline Ingest Service.

## hlctl import options

- --dry-run: validates the input files and prints the planned batches without sending anything.
- --dry-merge: computes the merge of incoming records with existing records and writes a diff report to merge-report.json without committing any change.
- --force-merge: commits the merge even when conflicting fields are detected; conflicts are resolved in favour of the incoming records.
- --merge-preview: deprecated alias that prints a short merge summary to the terminal.
- --max-parallel N: number of concurrent batches; default 4, maximum 32.

## hlctl export options

- --since TIMESTAMP: accepts an RFC 3339 timestamp and exports records changed after that time.
- --since-cursor CURSOR: accepts the opaque cursor string printed at the end of a previous hlctl export run and exports only records changed after that cursor.
- --format FORMAT: one of jsonl, csv, or parquet; default jsonl.
