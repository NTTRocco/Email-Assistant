# Project Brief: Email Context Agent

## Purpose
This repository provides an agent and supporting scripts to parse, preprocess, and structure email data (from EML files) for downstream analysis, search, and LLM-based question answering. The system is designed to enable efficient, reliable, and explainable analysis of large volumes of emails, supporting both incremental and full reprocessing workflows.

## Scope
- Input: Raw EML files placed in a dedicated folder.
- Output: Clean, chunked, and metadata-rich context files in Markdown format, one per email, for use as a "memory bank" for LLMs or other agents.
- Excludes: Storage of actual email content in the memory bank (the canonical source is the emails_context/ folder).
- Policy: The folder `emails_context/` MUST be used as the exclusive and authoritative source for all email context, chunk extraction, and evidence. Every LLM or agent request MUST search and extract matching chunks only from the files in `emails_context/`. Raw emails and other sources must NOT be used for analysis or evidence.
- Focus: Robust, reproducible, and transparent email parsing and context generation, with clear documentation and agent support for users.

## Core Goals
- Enable users to efficiently parse and analyze emails for business, compliance, or research purposes.
- Provide a clear, auditable, and explainable context structure for LLM-based agents.
- Support incremental updates and full resets for scalable workflows.
- Maintain separation between system documentation (memory bank) and email content (emails_context/).

## Recent behavioral changes (recorded)
- prepare_context.py now records attachment metadata for each processed email (filename, mime_type, size in bytes, and sha256 hash of the attachment payload). Attachment content is NOT stored — only metadata is written into the generated context files in an "## Attachments" section.
- prepare_context.py now permanently deletes processed raw `.eml` files from `emails_raw/` immediately after successful processing and context-file creation (irreversible). This behavior was enabled with explicit user approval in the latest session.
- Because raw `.eml` files are deleted after processing, `emails_context/` becomes the canonical store of parsed email evidence; maintain backups of `emails_raw/` before running a full reset if raw copies are required.

## Operational notes
- Incremental mode (python3 prepare_context.py) processes only new/unprocessed emails and will delete them after successful processing.
- Reset mode (python3 prepare_context.py --reset) reprocesses all emails and will delete processed raw files as well — use with caution and consider backups.
- Attachment metadata is included in the context files to allow indexing and search over attachments without storing attachment payloads in the memory bank.

## Auditing & Compliance
- The system purposefully avoids storing attachment content in the memory bank to reduce privacy risk; only metadata is recorded.
- Any future requirement to extract attachment content (e.g., PDF→text, DOCX→text, OCR) must be implemented as a separate custom script under `custom logic/` and requires explicit user approval before execution.
- Keep the `emails_context/` folder under access controls appropriate to the sensitivity of the parsed contents.

## Focus going forward
- Continue to treat `emails_context/` as the single source of truth for parsed email context and evidence.
- Keep memory bank files up to date whenever the parsing behavior, storage policy, or folder structure changes.
- Preserve the practice of documenting operational and privacy-relevant decisions in the memory bank.
