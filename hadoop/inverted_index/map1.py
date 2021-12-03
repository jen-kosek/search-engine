#!/usr/bin/env python3
"""Map 1."""
import sys
import re
import csv

csv.field_size_limit(sys.maxsize)

for line in csv.reader(sys.stdin):
    # Clean the input
    text = line[1] + " " + line[2]
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text).casefold()
    doc_id = line[0]

    # Get stop words
    stop_words = []
    with open("stopwords.txt", "r") as file:
        stop_words = [word.rstrip() for word in file]
    
    # For each word, output {(word, docid), 1 } pair
    for word in text.split():
        if word in stop_words:
            continue
        print(f"{word} {int(doc_id)}\t 1")

