# Active Context: Email Context Agent

## Current Work Focus
- The agent and script now group context files by week, creating subfolders in `emails_context/` (e.g. `2025,week46/`) based on the sent or received date of each email.
- This enables fast retrieval and analysis by time range.
- All context files are generated in Markdown format, with clear metadata and chunking for LLM compatibility.
- The system is designed to support users in parsing, searching, and analyzing emails efficiently, without storing email content in the memory bank.
- **Context preparation can be triggered at any time by simply asking the agent (via Axet Plugin input prompt): `prepare context`. The agent will run the parsing script automatically using the VSCode terminal.**
- **Hybrid analysis strategy:** For reporting or analytics tasks on emails_context/, the agent will:
  - Use only its own context window and file reading capabilities for manageable data volumes (e.g., a few dozen files per week).
  - If the data volume is high (risk of context saturation), develop and execute a custom Python script to process the data, then report only the final result to the user.
  - **All custom scripts must be placed in the `custom logic/` folder to ensure clear separation from the core codebase.**
- **MANDATORY:** For every user request involving analysis or reporting on emails_context/, the agent MUST always explicitly explain to the user which part of the task will be handled directly (context window) and which part will be delegated to custom code execution. This choice must be shared and validated with the user before proceeding.

## Recent Changes
- Added weekly grouping: context files are now saved in subfolders by year and ISO week.
- Added incremental processing: only new emails are parsed on each run.
- Added reset mode: all emails can be reprocessed by running the script with `--reset`.
- Improved documentation and separation between system logic (memory bank) and email content (emails_context/).
- **Hybrid analysis strategy for reporting and analytics tasks.**
- **Mandatory user validation of analysis strategy before execution.**
- **All custom scripts for analytics/reporting are now placed in the `custom logic/` folder.**

## Next Steps
- Maintain the input/output folder structure and keep context files up to date.
- Document any changes to parsing, chunking, or output logic in the memory bank.
- Consider extending the agent to support advanced search, filtering, or integration with LLMs.
- **Continue to apply and explicitly communicate the hybrid analysis strategy for all future reporting or analytics tasks, always sharing the approach with the user for validation.**
- **Continue to segregate all custom analytics/reporting scripts in the `custom logic/` folder.**

## Active Decisions and Patterns
- Email content is never stored in the memory bank; only system logic, patterns, and documentation are maintained.
- All context files use a standardized Markdown format for easy parsing and analysis.
- Incremental and reset modes are the default operational patterns.
- Weekly grouping is now the standard for output organization.
- **Hybrid analysis: context window for small data, Python script for large data.**
- **Mandatory: Always explain and share the chosen analysis strategy with the user before proceeding.**
- **All custom scripts for analytics/reporting must be placed in the `custom logic/` folder.**

## Learnings and Insights
- Separation of concerns between documentation and data enables scalable, auditable workflows.
- Incremental processing saves time and resources for ongoing email streams.
- Reset mode ensures data integrity and supports major updates or corrections.
- Weekly grouping makes it easier to retrieve and analyze emails by time range.
- Clear documentation in the memory bank is essential for maintainability and user support.
- **Hybrid analysis ensures both efficiency and scalability for reporting tasks, and explicit user validation ensures transparency and trust.**
- **Segregating custom scripts in `custom logic/` keeps the codebase clean and maintainable.**

## Recommendations
- The folder `emails_context/` MUST be used as the exclusive source for all email context, chunk extraction, and evidence. Every LLM or agent request MUST search and extract matching chunks only from the files in `emails_context/`. Raw emails and other sources must NOT be used for analysis or evidence.
- Use the weekly subfolders in `emails_context/` to quickly find emails for a specific time range.
- Always reference context files in `emails_context/` for analysis; do not use raw emails directly.
- Use incremental mode for daily/ongoing parsing; use reset mode for full reprocessing.
- Update the memory bank whenever system logic or workflow changes.
- **For reporting/analytics, prefer direct analysis for small data, and use a custom script for large data.**
- **Always communicate and share the chosen analysis strategy with the user for validation before executing the task.**
- **All custom scripts for analytics/reporting must be placed in the `custom logic/` folder.**
