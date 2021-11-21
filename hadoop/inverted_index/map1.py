#!/usr/bin/env python3
"""Map 1."""
import sys
import re


for line in sys.stdin:
    # Clean the input
    doc_id, title, body = line.split(",")
    text = title + " " + body
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)
    
    # For each word, output {(word, docid), 1 } pair
    for word in text:
        print(f"{word} {doc_id}\t 1")

