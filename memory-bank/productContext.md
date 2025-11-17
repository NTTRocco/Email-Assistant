# Product Context: Email Context Agent

## Why This Project Exists
Organizations and individuals often need to analyze, audit, or search large volumes of emails for compliance, business intelligence, or research. Raw email files (EML) are difficult to process and search directly, especially when dealing with mixed formats, signatures, replies, and attachments.

## Problems Solved
- Converts raw EML files into structured, clean, and chunked context files for easy analysis.
- Extracts key metadata (sender, subject, date) and readable body text, removing noise and irrelevant content.
- Enables incremental processing, so only new emails are parsed, saving time and resources.
- Supports full resets for complete reprocessing when needed.
- Provides a transparent, auditable workflow for downstream LLM or agent-based analysis.

## How It Should Work
- Users place EML files in the designated input folder.
- The agent/script parses each email, extracts metadata and clean text, chunks the content, and writes a Markdown context file to the output folder.
- Users can run the process incrementally or reset all context files as needed.
- The agent supports queries and analysis by referencing only the context files, not the raw emails.

## User Experience Goals
- Simple, reliable workflow for parsing and analyzing emails.
- Clear separation between system documentation (memory bank) and email content (emails_context/).
- Fast, incremental updates for ongoing email streams.
- Full transparency and traceability of parsing logic and context structure.
- No need to manually inspect or clean raw emails; the agent handles all preprocessing.
