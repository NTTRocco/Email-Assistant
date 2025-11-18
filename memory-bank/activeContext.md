# Active Context: Email Context Agent

## Current Work Focus
- The agent and script now group context files by week, creating subfolders in `emails_context/` (e.g. `2025,week46/`) based on the sent or received date of each email.
- This enables fast retrieval and analysis by time range.
- All context files are generated in Markdown format, with clear metadata and chunking for LLM compatibility.
- The system is designed to support users in parsing, searching, and analyzing emails efficiently, without storing email content in the memory bank.
- **Context preparation can be triggered at any time by simply asking the agent (via Axet Plugin input prompt): `prepare context`. The agent will run the parsing script automatically using the VSCode terminal.**
- **Hybrid analysis strategy:** For reporting or analytics tasks on `emails_context/`, the agent will:
  - Use only its own context window and file reading capabilities for manageable data volumes (e.g., a few dozen files per week).
  - If the data volume is high (risk of context saturation), develop and execute a custom Python script to process the data, then report only the final result to the user.
  - **All custom scripts must be placed in the `custom logic/` folder to ensure clear separation from the core codebase.**
- **MANDATORY:** For every user request involving analysis or reporting on `emails_context/`, the agent MUST always explicitly explain to the user which part of the task will be handled directly (context window) and which part will be delegated to custom code execution. This choice must be shared and validated with the user before proceeding.

## Recent Changes (this session)
- prepare_context.py was updated to record attachment metadata for each email: filename, mime_type, size (bytes), and sha256 hash of the attachment payload. The metadata is written into the generated context files in an "## Attachments" section when attachments are present.
- prepare_context.py was updated to permanently delete processed raw `.eml` files from `emails_raw/` immediately after successful processing and context-file creation (irreversible). The script also attempts to remove now-empty subdirectories under `emails_raw/` up to the `emails_raw` root.
- The deletion behavior is implemented as the default irreversible behavior in the current script (user-approved in this session). Both incremental runs (`python3 prepare_context.py`) and reset runs (`python3 prepare_context.py --reset`) will delete processed raw `.eml` files after writing context files. Users should backup raw files if they want to keep them.
- The repository now documents and enforces the pattern that attachment content is not stored in the memory bank — only metadata is recorded (controlled metadata indexing policy).

## Next Steps
- Maintain the input/output folder structure and keep context files up to date.
- Document any future changes to parsing, chunking, or output logic in the memory bank.
- If the user requests attachment content extraction (PDF → text, DOCX → text, OCR for images), create a custom script under `custom logic/` and obtain explicit user approval before running (due to privacy/compliance and possible large-scale processing).
- Ensure memory bank files reflect all behavioral changes to the core scripts; update them whenever workflow, privacy, or storage policies change.

## Active Decisions and Patterns
- Email content is never stored in the memory bank; only system logic, patterns, and documentation are maintained.
- All context files use a standardized Markdown format for easy parsing and analysis.
- Incremental and reset modes are the default operational patterns.
- Weekly grouping is now the standard for output organization.
- The system now permanently deletes processed raw `.eml` files after successful parsing (user approved). This makes `emails_context/` the canonical store of parsed email evidence.
- **Hybrid analysis: context window for small data, Python script for large data.**
- **Mandatory: Always explain and share the chosen analysis strategy with the user before proceeding.**
- **All custom scripts for analytics/reporting must be placed in the `custom logic/` folder.**

## Learnings and Insights
- Separation of concerns between documentation and data enables scalable, auditable workflows.
- Incremental processing saves time and resources for ongoing email streams.
- Reset mode ensures data integrity and supports major updates or corrections but will also delete raw copies under the new policy — back up before running reset if you need originals.
- Weekly grouping makes it easier to retrieve and analyze emails by time range.
- Clear documentation in the memory bank is essential for maintainability and user support.
- **Segregating custom scripts in `custom logic/` keeps the codebase clean and maintainable.**

## Recommendations (updated)
- The folder `emails_context/` MUST be used as the exclusive source for all email context, chunk extraction, and evidence. Every LLM or agent request MUST search and extract matching chunks only from the files in `emails_context/`. Raw emails and other sources must NOT be used for analysis or evidence.
- Because the parsing script now deletes processed raw `.eml` files, make a manual backup of `emails_raw/` before running a `--reset` if you want to preserve originals.
- Use incremental mode for daily/ongoing parsing; use reset mode for full reprocessing (with backups if you care about raw files).
- Update the memory bank whenever system logic or workflow changes.
- **For reporting/analytics, prefer direct analysis for small data, and use a custom script for large data.**
- **Always communicate and share the chosen analysis strategy with the user for validation before executing the task.**
- **All custom scripts for analytics/reporting must be placed in the `custom logic/` folder.**
