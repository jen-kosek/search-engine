#!/usr/bin/env python3
"""Reduce 2."""

import sys
import itertools
import math

total_num_docs = 0

def reduce_one_group(key, group):
    group = list(group)
    num_docs = 0
    for line in group:
        num_docs += 1
    
    inverse_doc_freq = math.log(total_num_docs/num_docs)

    for line in group:
        word, doc_id, frequency = line.split()
        print(f"{doc_id}\t{word} {frequency} {inverse_doc_freq}")



def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    # Get num documents
    with open("total_document_count.txt", "r") as file:
        num_docs = file.readline.split()[0]


    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()