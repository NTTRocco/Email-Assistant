# Email Context Agent

## Important: Axet Plugin Setup

This Email Assistant is designed to be used with the Axet Plugin.

**Before using the agent, you MUST:**
- Open the file `memory-bank-system-prompt` in this repository.
- Copy its entire content into the "Custom Instruction" section of the Axet Plugin Settings.

This step is mandatory for the correct execution and behavior of the agent.

---

## Quick Start

This repository provides an agent to help you parse, preprocess, and analyze email files (EML format) for search and LLM-based question answering.  
**The parsing process will also organize the context files by week, making it easy to retrieve emails for a specific time range.**

## How to Use

1. **Add Your Emails**
   - Simply drag and drop the selected emails from Outlook into the `emails_raw/` folder using Finder (on Mac) or File Explorer (on Windows). This will automatically export them as `.eml` files.
   - Alternatively, you can manually place your `.eml` files in the `emails_raw/` folder (subfolders are supported).

2. **Run the Agent**
   - From the repository root, run:
     ```
     python3 prepare_context.py
     ```
   - By default, only new emails are processed.  
   - To reprocess all emails (reset), run:
     ```
     python3 prepare_context.py --reset
     ```

3. **Find Results**
   - Processed email context files are saved in the `emails_context/` folder, **organized in subfolders by week** (e.g. `emails_context/2025,week46/`).
   - Each file contains clean, chunked text and metadata for easy analysis.

4. **Ask Questions**
   - Use the files in `emails_context/` as the source for any search, analysis, or LLM-based queries.
   - The agent and LLMs will always use this folder to find and extract relevant information.

## Example Questions

Here are some example questions you can ask the agent (the answer will always be based on the content of the files in `emails_context/`):

- "Which emails mention the project EXT-304292-12345?"
- "Show me all emails sent by alice@example.com in November 2025."
- "What is the subject and main content of the email with ID `2025,week46__Deep Dive necessario sull’adozione della GenAI nei progetti_context.txt`?"
- "Please summarize the activitues related the GenAI adoption."
- "Find the chunk where the sender requests a meeting about AI compliance."

## Documentation

- For full details on system logic, architecture, and best practices, see the `memory-bank/` folder.

---
**Note:**  
- The agent never stores email content outside of `emails_context/`.
- All analysis and evidence must come from the files in `emails_context/`.
