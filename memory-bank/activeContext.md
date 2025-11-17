# Active Context: Email Context Agent

## Current Work Focus
- The agent and script are now fully configured to support both incremental and full reset parsing of EML files.
- All context files are generated in Markdown format, with clear metadata and chunking for LLM compatibility.
- The system is designed to support users in parsing, searching, and analyzing emails efficiently, without storing email content in the memory bank.

## Recent Changes
- Added incremental processing: only new emails are parsed on each run.
- Added reset mode: all emails can be reprocessed by running the script with `--reset`.
- Improved documentation and separation between system logic (memory bank) and email content (emails_context/).

## Next Steps
- Maintain the input/output folder structure and keep context files up to date.
- Document any changes to parsing, chunking, or output logic in the memory bank.
- Consider extending the agent to support advanced search, filtering, or integration with LLMs.

## Active Decisions and Patterns
- Email content is never stored in the memory bank; only system logic, patterns, and documentation are maintained.
- All context files use a standardized Markdown format for easy parsing and analysis.
- Incremental and reset modes are the default operational patterns.

## Learnings and Insights
- Separation of concerns between documentation and data enables scalable, auditable workflows.
- Incremental processing saves time and resources for ongoing email streams.
- Reset mode ensures data integrity and supports major updates or corrections.
- Clear documentation in the memory bank is essential for maintainability and user support.

## Recommendations
- The folder `emails_context/` MUST be used as the exclusive source for all email context, chunk extraction, and evidence. Every LLM or agent request MUST search and extract matching chunks only from the files in `emails_context/`. Raw emails and other sources must NOT be used for analysis or evidence.
- Always reference context files in `emails_context/` for analysis; do not use raw emails directly.
- Use incremental mode for daily/ongoing parsing; use reset mode for full reprocessing.
- Update the memory bank whenever system logic or workflow changes.
