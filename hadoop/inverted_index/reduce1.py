#!/usr/bin/env python3
"""Reduce 1."""

import sys
import itertools


def reduce_one_group(key, group):
    # Cacluate and print the frequency of the word in the document
    frequency = 0
    for line in group:
        _, value = line.split("\t")
        frequency += int(value)
    print(f"{key}\t{frequency}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()