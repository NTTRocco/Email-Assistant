# Progress: Email Context Agent

## What Works
- The agent and script reliably parse all EML files in the input directory, generating clean, chunked, and metadata-rich context files in Markdown format.
- Context files are grouped in subfolders by week (e.g. `emails_context/2025,week46/`), based on the sent or received date of each email, enabling fast retrieval and analysis by time range.
- Incremental processing is fully functional: only new emails are parsed on each run.
- Reset mode is available: all emails can be reprocessed with the `--reset` flag.
- The system is well-documented, with a clear separation between system logic (memory bank) and email content (emails_context/).
- Output files are consistently named and structured for easy downstream analysis.
- Hybrid analysis strategy is defined: direct file analysis for small volumes; custom Python scripts (placed under `custom logic/`) for large volumes.
- Mandatory user validation for any large-scale processing or when the agent will run custom scripts.

## Recent Changes (this session)
- prepare_context.py now records attachment metadata for each processed email (filename, mime_type, size in bytes, and sha256 hash of the attachment payload). Attachment content is NOT stored — only metadata is written into the generated context files in an "## Attachments" section.
- prepare_context.py now permanently deletes processed raw `.eml` files from `emails_raw/` immediately after successful processing and context-file creation (irreversible). The script also attempts to remove now-empty subdirectories under `emails_raw/` up to the `emails_raw` root.
- Both incremental and reset runs will delete processed raw files under the new behavior (user-approved during this session).
- Memory bank files updated to record these behavioral and policy decisions: `memory-bank/projectbrief.md` and `memory-bank/activeContext.md` were updated to reflect attachment-metadata indexing and the new deletion policy. This `progress.md` file now also documents the change.

## What's Left to Build / Improve
- Optional: Add advanced search, filtering, or query capabilities for context files.
- Optional: Integrate with LLMs or other agents for automated Q&A or summarization (ensure searches read only from `emails_context/`).
- Optional: Add more robust HTML parsing (e.g., via `beautifulsoup4`) if needed.
- Optional: Implement automated tests for parsing, chunking, and the deletion/cleanup steps.
- Optional: Add a configurable cleanup policy (archive vs delete) or a `--no-delete` flag if reversible behavior is later desired.

## Current Status
- System is stable and ready for parsing and analyzing large volumes of emails.
- Attachment metadata indexing is enabled and context files have been re-generated in this session.
- The raw EML cleanup behavior is now destructive by design — backups are strongly advised before running reset mode.

## Known Issues / Limitations
- Basic HTML parsing may not handle all edge cases; consider installing `beautifulsoup4` for complex emails.
- The system records attachment metadata only; it does not extract or index attachment content.
- Deletion of raw `.eml` files is irreversible; there is no built-in backup in the script. Users must backup `emails_raw/` manually if they want to keep raw copies.
- No deduplication of emails; identical emails with different filenames will both be processed.

## Evolution of Project Decisions
- Initial focus: robust parsing and transparent context generation.
- Added incremental and reset workflows for operational flexibility.
- Weekly grouping introduced for time-based retrieval.
- Hybrid analysis strategy adopted to balance context-window limits vs large-scale processing.
- This session: added attachment-metadata indexing and enabled permanent deletion of processed raw `.eml` files (user-approved). These decisions are recorded in the memory bank for auditing and compliance.

## Recommendations (updated)
- Treat `emails_context/` as the single source of truth for parsed email evidence and search.
- Before running `python3 prepare_context.py --reset`, create a manual backup of `emails_raw/` if you want to retain original .eml files.
- Use incremental mode for daily/ongoing parsing; use reset mode only when needed and with backups if raw copies are required.
- If attachment content extraction becomes required, implement it as a separate custom script under `custom logic/` and obtain explicit approval before running.
