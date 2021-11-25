#!/usr/bin/env python3
"""Map 2."""
import sys


for line in sys.stdin:    
    key, frequency = line.strip().split("\t")
    word, doc_id = key.split()
    print(f"{word}\t{doc_id} {frequency}")

