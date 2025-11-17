"""
report_email_stats.py

Report: Number of emails sent and received per week.

- Scans all context files in emails_context/YYYY,weekWW/
- For each file, reads the "Sender" metadata
- If "Sender" contains "rocco.mellino", counts as SENT, else as RECEIVED
- Aggregates counts per week (YYYY,weekWW)
- Prints a Markdown table with the results

USAGE:
python3 report_email_stats.py

You can change the SENDER_KEYWORD variable to match your own email identifier.
"""

import os
import re

CONTEXT_DIR = './emails_context'
SENDER_KEYWORD = 'rocco.mellino'  # Change this if needed

def scan_context_files():
    stats = {}
    for week_folder in os.listdir(CONTEXT_DIR):
        week_path = os.path.join(CONTEXT_DIR, week_folder)
        if not os.path.isdir(week_path):
            continue
        sent = 0
        received = 0
        for fname in os.listdir(week_path):
            if not fname.endswith('_context.txt'):
                continue
            fpath = os.path.join(week_path, fname)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Extract Sender from metadata
                m = re.search(r'- Sender: (.+)', content)
                sender = m.group(1).strip() if m else ''
                if SENDER_KEYWORD.lower() in sender.lower():
                    sent += 1
                else:
                    received += 1
            except Exception as e:
                print(f"Error reading {fpath}: {e}")
        stats[week_folder] = {'sent': sent, 'received': received}
    return stats

def print_report(stats):
    print("| Week           | Sent | Received |")
    print("|:---------------|-----:|---------:|")
    for week in sorted(stats.keys()):
        sent = stats[week]['sent']
        received = stats[week]['received']
        print(f"| {week:<14} | {sent:>4} | {received:>8} |")

if __name__ == "__main__":
    stats = scan_context_files()
    print_report(stats)
