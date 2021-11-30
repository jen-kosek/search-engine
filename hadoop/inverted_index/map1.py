#!/usr/bin/env python3
"""Map 1."""
import sys
import re
import csv

csv.field_size_limit(sys.maxsize)

for line in sys.stdin:
    # Clean the input
    doc_id, title, body = line.split("\",\"")
    text = title.strip("\"") + " " + body.strip("\"")
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text).casefold()
    doc_id = doc_id.strip("\"")

    # Get stop words
    stop_words = []
    with open("stopwords.txt", "r") as file:
        stop_words = [line.rstrip() for line in file]
    
    # For each word, output {(word, docid), 1 } pair
    for word in text.split():
        if word in stop_words:
            continue
        print(f"{word} {int(doc_id)}\t 1")

