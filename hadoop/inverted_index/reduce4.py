#!/usr/bin/env python3
"""Reduce 4."""

import sys
import itertools


def reduce_one_group(key, group):
    # Get word and inverse doc frequency form first line
    word, out_num, inverse_doc_freq, doc_id, frequency, norm_factor= next(group).split()
    output = word + " " + inverse_doc_freq + " " + doc_id + " " + frequency + " " + norm_factor + " "
    
    # Just get doc specific info from rest of lines
    for line in group:
        _, _, _, doc_id, frequency, norm_factor= line.split()
        output += doc_id + " " + frequency + " " + norm_factor + " "
    
    # Print key = docid % 3, value = line in inverted index
    print(f"{out_num}\t {output}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()