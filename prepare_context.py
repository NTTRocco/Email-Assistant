"""
prepare_context.py

This script processes all .eml files in the ./emails_raw/ directory and its subfolders, extracts metadata and clean text, chunks the text for LLM context, and writes structured context files to ./emails_context/, grouped by week (sent or received date).

USAGE:
1. Place your .eml files into the ./emails_raw/ folder (must exist in the workspace root). Subfolders are supported.
2. Run the script: python prepare_context.py
   - By default, only new emails (not yet processed) are parsed.
   - To force a full reset and re-parse all emails, run: python prepare_context.py --reset
3. The script will create ./emails_context/ (if it doesn't exist) and write output files there, grouped by week (e.g. ./emails_context/2025,week46/).
4. Ask the AI agent a question by referencing the generated context files in ./emails_context/.

Dependencies: Only standard Python libraries are used. If you encounter issues with HTML parsing, consider installing beautifulsoup4 for more robust handling.
"""

import os
import re
import email
from email import policy
from email.parser import BytesParser
import sys
import datetime

RAW_DIR = './emails_raw'
CONTEXT_DIR = './emails_context'
CHUNK_CHAR_LIMIT = 500  # Max characters per chunk

def context_filename(rel_filename):
    safe_name = rel_filename.replace(os.sep, '__')
    base = os.path.splitext(safe_name)[0]
    return f"{base}_context.txt"

def ensure_directories():
    if not os.path.exists(RAW_DIR):
        raise FileNotFoundError(f"Input directory '{RAW_DIR}' does not exist. Please create it and add .eml files.")
    if not os.path.exists(CONTEXT_DIR):
        os.makedirs(CONTEXT_DIR)

def list_eml_files():
    """
    Recursively find all .eml files in RAW_DIR and its subfolders.
    Returns a list of (full_path, rel_path) tuples.
    """
    eml_files = []
    for root, dirs, files in os.walk(RAW_DIR):
        for f in files:
            if f.lower().endswith('.eml'):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, RAW_DIR)
                eml_files.append((full_path, rel_path))
    return eml_files

def extract_metadata(msg, filename):
    sender = msg.get('From', '').strip()
    subject = msg.get('Subject', '').strip()
    date = msg.get('Date', '').strip()
    return {
        'ID': filename,
        'Sender': sender,
        'Subject': subject,
        'Date': date
    }

def strip_html(html):
    # Basic HTML tag stripper using regex
    # For more robust parsing, install beautifulsoup4 and use BeautifulSoup(html, "html.parser").get_text()
    text = re.sub(r'(?is)<(script|style).*?>.*?(</\1>)', '', html)  # Remove script/style
    text = re.sub(r'<[^>]+>', '', text)  # Remove tags
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&', '&', text)
    text = re.sub(r'<', '<', text)
    text = re.sub(r'>', '>', text)
    return text

def extract_body(msg):
    # Prefer text/plain, else fallback to text/html
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == 'text/plain':
                return part.get_content().strip()
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == 'text/html':
                html = part.get_content()
                return strip_html(html).strip()
    else:
        ctype = msg.get_content_type()
        if ctype == 'text/plain':
            return msg.get_content().strip()
        elif ctype == 'text/html':
            html = msg.get_content()
            return strip_html(html).strip()
    return ""

def clean_text(text):
    # Remove reply headers (e.g., "On [Date], [Sender] wrote:")
    text = re.sub(r'On .{0,100}?wrote:', '', text)
    # Remove common signature delimiters
    text = re.sub(r'(?m)^--\s*\n.*', '', text)
    # Remove excessive newlines/whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = text.strip()
    return text

def split_into_chunks(text):
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    chunks = []
    for para in paragraphs:
        if len(para) <= CHUNK_CHAR_LIMIT:
            chunks.append(para)
        else:
            # Split long paragraphs by sentence, try to keep sentences together
            sentences = re.split(r'(?<=[.!?]) +', para)
            chunk = ""
            for sent in sentences:
                if len(chunk) + len(sent) + 1 <= CHUNK_CHAR_LIMIT:
                    chunk = (chunk + " " + sent).strip()
                else:
                    if chunk:
                        chunks.append(chunk)
                    chunk = sent
            if chunk:
                chunks.append(chunk)
    return chunks

def get_year_week(date_str):
    """
    Parse the email date string and return (YYYY, weekWW) as strings.
    If parsing fails, fallback to 'unknown'.
    """
    try:
        # Try parsing with email.utils
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(date_str)
        iso_year, iso_week, _ = dt.isocalendar()
        return f"{iso_year}", f"week{iso_week:02d}"
    except Exception:
        return "unknown", "week00"

def write_context_file(metadata, chunks, rel_filename, year, week):
    week_dir = os.path.join(CONTEXT_DIR, f"{year},{week}")
    if not os.path.exists(week_dir):
        os.makedirs(week_dir)
    out_filename = context_filename(rel_filename)
    out_path = os.path.join(week_dir, out_filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f"# EMAIL CONTEXT: {rel_filename}\n\n")
        f.write("## Metadata\n")
        f.write(f"- ID: {metadata['ID']}\n")
        f.write(f"- Sender: {metadata['Sender']}\n")
        f.write(f"- Subject: {metadata['Subject']}\n")
        f.write(f"- Date: {metadata['Date']}\n\n")
        f.write("## Content Chunks\n\n")
        for i, chunk in enumerate(chunks, 1):
            f.write(f"--- CHUNK {i} ---\n")
            f.write(chunk + "\n\n")

def process_eml_file(full_path, rel_filename):
    with open(full_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    metadata = extract_metadata(msg, rel_filename)
    body = extract_body(msg)
    clean_body = clean_text(body)
    chunks = split_into_chunks(clean_body)
    year, week = get_year_week(metadata['Date'])
    write_context_file(metadata, chunks, rel_filename, year, week)

def main():
    ensure_directories()
    eml_files = list_eml_files()
    if not eml_files:
        print(f"No .eml files found in {RAW_DIR} or its subfolders. Please add files and rerun.")
        return

    reset_mode = len(sys.argv) > 1 and sys.argv[1] == "--reset"
    if reset_mode:
        print("Reset mode: all emails will be re-parsed and context files regenerated.")
    else:
        print("Incremental mode: only new emails (not yet processed) will be parsed.")

    processed = 0
    skipped = 0
    for full_path, rel_filename in eml_files:
        # Determine year/week for output path
        with open(full_path, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)
        metadata = extract_metadata(msg, rel_filename)
        year, week = get_year_week(metadata['Date'])
        week_dir = os.path.join(CONTEXT_DIR, f"{year},{week}")
        out_filename = context_filename(rel_filename)
        out_path = os.path.join(week_dir, out_filename)
        if not reset_mode and os.path.exists(out_path):
            print(f"Skipped (already processed): {rel_filename}")
            skipped += 1
            continue
        try:
            process_eml_file(full_path, rel_filename)
            print(f"Processed: {rel_filename} -> {year},{week}/")
            processed += 1
        except Exception as e:
            print(f"Error processing {rel_filename}: {e}")
    print(f"\nSummary: {processed} processed, {skipped} skipped.")

if __name__ == "__main__":
    main()
