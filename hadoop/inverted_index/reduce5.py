#!/usr/bin/env python3
"""Reduce 4."""

import sys
import itertools


def reduce_one_group(key, group):    
    # Just print the inverted index info 
    for line in group:
        _, output= line.split("\t")
        print(output.strip())


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()