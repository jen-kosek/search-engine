#!/usr/bin/env python3
"""Map 2."""
import sys
import re


for line in sys.stdin:    
    word, doc_id, frequency = line.split()
    print(f"{word}\t{doc_id} {frequency}")

