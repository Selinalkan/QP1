#!/usr/bin/env python
"""Demonstration using B-K trees for nearest neighbor computation.
The Wikipedia page has a good introduction:
    https://en.wikipedia.org/wiki/BK-tree
"""

from typing import Any, List

import numpy

# Found here:
#     https://github.com/benhoyt/pybktree
# and on PyPI (i.e. via pip).
import pybktree
# import argparse

DATA = [
    "animus",
    "melodious",
    "Tupian",
    "turnscrew" "acidyl",
    "allheal",
    "handsome",
    "suaharo",
    "Muhlenbergia",
    "Choluteca",
    "Alouatta",
    "submetering",
    "shoppy",
    "chillroom",
    "Nisaean",
    "olefin",
    "arthrosporic",
    "conjugable",
    "anacephalize",
    "prozone",
]

# If there are no candidates within this bound we error out so this doesn't
# go on infinitely.
UPPER_BOUND = 10


class Error(Exception):
    pass


def edit_distance(x: List[Any], y: List[Any]) -> int:
    # For a more expressive version of the same, see:
    #
    #     https://gist.github.com/kylebgorman/8034009
    idim = len(x) + 1
    jdim = len(y) + 1
    table = numpy.zeros((idim, jdim), dtype=numpy.uint8)
    table[1:, 0] = 1
    table[0, 1:] = 1
    for i in range(1, idim):
        for j in range(1, jdim):
            if x[i - 1] == y[j - 1]:
                table[i][j] = table[i - 1][j - 1]
            else:
                c1 = table[i - 1][j]
                c2 = table[i][j - 1]
                c3 = table[i - 1][j - 1]
                table[i][j] = min(c1, c2, c3) + 1
    return int(table[-1][-1])


def main() -> None:
    # We pass the distance metric and the data during construction.
    tree = pybktree.BKTree(edit_distance, DATA)
    # The author has not provided us a nearest neighbor function. What
    # they have provided us with is a `find` method which gives us all
    # neighbors within a certain distance. By slowly increasing this until this
    # set is non-empty we can find the nearest neighbors. Sicne there may be
    # more than one, we return them all.
    lookup = "prozone"
    found_something = False
    for bound in range(1, 1 + UPPER_BOUND):
        found = tree.find(lookup, bound)
        if len(found) > 1:
            found_something = True
        else:
            continue
        for distance, match in found:
            # We have to take special care not to return a word as its own
            # nearest neighbor.
            if distance == 0:
                continue
            else:
                print(f"Nearest neigbhor: {match}")
        break
    if not found_something:
        raise Error(f"no match found within {UPPER_BOUND} edits")


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "-i",
    #     "--input",
    #     default="lemma-suffix_only.tsv",
    #     help="input Maori TSV file",
    # )
    # parser.add_argument(
    #     "-o1",
    #     "--output1",
    #     default="00_bktree_Kyle.tsv",
    #     help="outputs stem-final vowel counts",
    # )
    # main(parser.parse_args())
    main()