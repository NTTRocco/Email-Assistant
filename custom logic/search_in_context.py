"""
search_in_context.py

Cerca una parola o frase (case-insensitive di default) in tutti i file context di emails_context/.
Stampa la lista dei file trovati e un estratto del contesto.

USO:
python3 "custom logic/search_in_context.py" "query" [--case]

Esempio:
python3 "custom logic/search_in_context.py" oneerp
python3 "custom logic/search_in_context.py" "project EXT-304292-12345" --case
"""

import os
import re
import sys

CONTEXT_DIR = './emails_context'

def search_in_file(fpath, query, case_sensitive=False):
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        flags = 0 if case_sensitive else re.IGNORECASE
        matches = list(re.finditer(re.escape(query), content, flags))
        if matches:
            # For each match, show a snippet of 40 chars before/after
            snippets = []
            for m in matches:
                start = max(0, m.start() - 40)
                end = min(len(content), m.end() + 40)
                snippet = content[start:end].replace('\n', ' ')
                snippets.append(snippet)
            return snippets
        return None
    except Exception as e:
        print(f"Error reading {fpath}: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 'custom logic/search_in_context.py' 'query' [--case]")
        sys.exit(1)
    query = sys.argv[1]
    case_sensitive = '--case' in sys.argv[2:]
    found = []
    for week_folder in os.listdir(CONTEXT_DIR):
        week_path = os.path.join(CONTEXT_DIR, week_folder)
        if not os.path.isdir(week_path):
            continue
        for fname in os.listdir(week_path):
            if not fname.endswith('_context.txt'):
                continue
            fpath = os.path.join(week_path, fname)
            snippets = search_in_file(fpath, query, case_sensitive)
            if snippets:
                found.append((f"{week_folder}/{fname}", snippets))
    if not found:
        print(f"Nessuna email trovata che parli di '{query}'.")
    else:
        print(f"Trovate {len(found)} email che contengono '{query}':\n")
        for f, snippets in found:
            print(f"- {f}")
            for s in snippets:
                print(f"    ...{s}...")
            print()
if __name__ == "__main__":
    main()
