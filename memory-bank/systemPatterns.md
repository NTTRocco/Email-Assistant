# System Patterns: Email Context Agent

## Architecture Overview
- **Input Layer**: Raw EML files are placed in the `emails_raw/` directory (supports subfolders).
- **Processing Layer**: The `prepare_context.py` script parses each EML file, extracts metadata and clean text, applies cleaning and chunking logic, and generates a Markdown context file.
- **Output Layer**: Structured context files are written to `emails_context/`, grouped in subfolders by week (e.g. `emails_context/2025,week46/`), one per email, using a consistent naming convention.

## Key Patterns and Workflows
- **Incremental Processing**: On each run, only new emails (those without a corresponding context file) are processed, enabling efficient updates.
- **Reset Mode**: By running the script with `--reset`, all emails are reprocessed and context files are regenerated, ensuring a clean state.
- **Weekly Grouping**: Each context file is saved in a subfolder named by year and ISO week (e.g. `2025,week46`), based on the sent or received date of the email. This enables fast retrieval and analysis by time range.
- **Chunking Strategy**: Email body text is split into logical chunks (paragraphs, sentences) to fit LLM context windows, preserving readability and semantic boundaries.
- **Metadata Extraction**: Each context file includes standardized metadata (ID, sender, subject, date) for traceability and search.
- **Markdown Output**: Context files use Markdown headers and chunk delimiters for easy parsing by agents and LLMs.

## Component Relationships
- **Script ↔ Input Folder**: The script scans the input folder recursively for EML files.
- **Script ↔ Output Folder**: For each processed email, a context file is created in the output folder.
- **Agent/LLM ↔ Context Files**: The agent (or LLM) MUST use the `emails_context/` folder as the exclusive and authoritative source for all email context, search, and chunk extraction. Every LLM request must reference and extract matching chunks only from the files in `emails_context/`. Raw emails and other sources must NOT be used for context or evidence.

## Implementation Patterns
- **Separation of Concerns**: Email content is stored only in context files; system documentation and logic are maintained in the memory bank.
- **Auditability**: All parsing, cleaning, and chunking logic is documented and reproducible.
- **Extensibility**: The system can be extended to support new parsing rules, chunking strategies, or output formats without affecting the core workflow.

## Critical Paths
- Input → Parse → Clean → Chunk → Output → Analysis
- Incremental/Reset logic ensures data integrity and efficient processing.

## Transparency
- All processing steps and logic are documented in the memory bank.
- Users can trace every output file back to its source and understand the transformation applied.
