#!/usr/bin/env python3
"""Reduce 3."""

import sys
import itertools
import math


def reduce_one_group(key, group):
    group = list(group)
    norm_factor = 0
    for line in group:
        _, _, frequency, inverse_doc_freq = line.split()
        norm_factor += math.pow(float(frequency) * float(inverse_doc_freq), 2)

    for line in group:
        doc_id, word, frequency, inverse_doc_freq = line.split()
        print(f"{word} {int(doc_id) % 3}\t{inverse_doc_freq} {doc_id} {frequency} {norm_factor}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()