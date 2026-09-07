import os
import glob
import re

services_dir = "/Users/anatolichastik/Documents/WEB-QUINTE-SMART-HOMES/WEB-QUINTE-SMART-HOMES/src/services"
html_files = sorted(glob.glob(os.path.join(services_dir, "*.html")))

print(f"Deep-combing all {len(html_files)} service files for phrase & sentence redundancies...\n")

def clean_text(raw_html):
    text = re.sub(r'<[^>]+>', ' ', raw_html)
    return re.sub(r'\s+', ' ', text).strip()

def get_sentences(text):
    # Split into sentences or clauses of 5+ words
    raw_sents = re.split(r'[.!?;\n]', text)
    valid = []
    for s in raw_sents:
        cleaned = re.sub(r'[^\w\s]', '', s).strip().lower()
        words = cleaned.split()
        if len(words) >= 5:
            valid.append((cleaned, s.strip()))
    return valid

all_file_sentences = {}

for filepath in html_files:
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Strip script and style blocks
    content_clean = re.sub(r'<script.*?>.*?</script>', '', content, flags=re.DOTALL)
    content_clean = re.sub(r'<style.*?>.*?</style>', '', content_clean, flags=re.DOTALL)
    content_text = clean_text(content_clean)
    
    sentences = get_sentences(content_text)
    
    # Check internal redundancies within the file
    seen = {}
    duplicates_internal = []
    for norm, orig in sentences:
        if norm in seen:
            duplicates_internal.append((norm, orig, seen[norm]))
        else:
            seen[norm] = orig

    if duplicates_internal:
        print(f"[REDUNDANCIES IN {filename}]:")
        for norm, orig, first_seen in duplicates_internal:
            # Filter out common short navigation/button labels if any
            if norm not in ["request pricing", "learn more", "get network quote", "request home security pricing"]:
                print(f"  • Duplicated phrase/sentence: \"{orig}\"")
        print()
    else:
        print(f"✓ {filename}: 0 internal redundancies.")

