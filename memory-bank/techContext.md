# Tech Context: Email Context Agent

## Technologies Used
- **Language**: Python 3.x (Python 3 must be installed on the user system; see README for setup instructions)
- **Libraries**: Only standard Python libraries (os, re, email, sys, etc.) are used for maximum portability and ease of setup.
- **Optional**: For more robust HTML parsing, users may install `beautifulsoup4` (not required for baseline functionality).

## Development Setup
- Place raw EML files in the `emails_raw/` directory.
- Run the main script (`prepare_context.py`) from the repository root.
- Output context files are generated in the `emails_context/` directory, grouped in subfolders by week (e.g. `emails_context/2025,week46/`).
- No external dependencies required for core functionality; install `beautifulsoup4` only if needed.
- **Recommended:** Use a Python virtual environment to keep dependencies isolated:
  ```
  python3 -m venv .venv
  source .venv/bin/activate   # On Windows: .venv\Scripts\activate
  ```

## Output Structure
- Context files are now grouped in subfolders by week, based on the sent or received date of each email. For example: `emails_context/2025,week46/[filename]_context.txt`.
- This structure enables fast retrieval and analysis by time range.

## Technical Constraints
- No email content is stored in the memory bank; all content is in context files.
- Script supports both incremental and full reset processing modes.
- Output files use Markdown for easy parsing and LLM compatibility.
- Chunking logic is designed to respect paragraph and sentence boundaries, with a configurable character limit.

## Tool Usage Patterns
- **Incremental Mode**: Processes only new emails, skipping those already parsed.
- **Reset Mode**: Reprocesses all emails, regenerating all context files.
- **Error Handling**: Script prints errors for any files it cannot process, allowing for manual review.

## Dependencies
- Python 3.x (recommended)
- Standard library only (no pip install required for baseline)
- Optional: `beautifulsoup4` for advanced HTML parsing

## Extensibility
- Parsing, cleaning, and chunking logic can be extended or customized as needed.
- Additional output formats or metadata fields can be added without breaking the core workflow.
- The agent can be integrated with other LLMs or search tools by referencing the context files.

## Best Practices
- The folder `emails_context/` is the ONLY valid source for email context, chunk extraction, and evidence. Every LLM or agent request MUST search and extract matching chunks exclusively from the files in `emails_context/`. Raw emails and other sources must NOT be used for analysis or evidence.
- Keep the input and output folders organized and separate.
- Use incremental mode for ongoing email streams; use reset mode for major updates or corrections.
- Document any changes to parsing logic or output structure in the memory bank for future maintainers.
