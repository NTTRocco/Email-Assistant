# Project Brief: Email Context Agent

## Purpose
This repository provides an agent and supporting scripts to parse, preprocess, and structure email data (from EML files) for downstream analysis, search, and LLM-based question answering. The system is designed to enable efficient, reliable, and explainable analysis of large volumes of emails, supporting both incremental and full reprocessing workflows.

## Scope
- Input: Raw EML files placed in a dedicated folder.
- Output: Clean, chunked, and metadata-rich context files in Markdown format, one per email, for use as a "memory bank" for LLMs or other agents.
- Excludes: Storage of actual email content in the memory bank (the canonical source is the emails_context/ folder).
- **Policy**: The folder `emails_context/` MUST be used as the exclusive and authoritative source for all email context, chunk extraction, and evidence. Every LLM or agent request MUST search and extract matching chunks only from the files in `emails_context/`. Raw emails and other sources must NOT be used for analysis or evidence.
- Focus: Robust, reproducible, and transparent email parsing and context generation, with clear documentation and agent support for users.

## Core Goals
- Enable users to efficiently parse and analyze emails for business, compliance, or research purposes.
- Provide a clear, auditable, and explainable context structure for LLM-based agents.
- Support incremental updates and full resets for scalable workflows.
- Maintain separation between system documentation (memory bank) and email content (emails_context/).
