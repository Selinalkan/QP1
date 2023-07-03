#!/usr/bin/env python

"""This script splits the Maori verbs with passive suffixes into two columns
        the first of which with the lemmas and the second of which with the 
        unhyphenated passive endings. The verbs going through internal
        change have not been included in this data set."""

import argparse
import re
import csv


def main(args: argparse.Namespace) -> None:
    with open(args.input, "r") as source, open(args.output, "w") as sink:
        tsv_reader = csv.reader(source, delimiter="\t")
        tsv_writer = csv.writer(sink, delimiter="\t")
        for row in tsv_reader:
            match_obj = re.match(r"(\w+)(\-)(\w+)", row[1])
            if match_obj:
                row = [
                    match_obj.group(1),
                    # match_obj.group(1) + match_obj.group(3),
                    match_obj.group(3)
                ]
            assert row[0] != ""
            tsv_writer.writerow(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="BR_7-4-2023.tsv", help="input Maori file")
    parser.add_argument(
        "--output", default="lemma-suffix_only.tsv", help="output Maori file as lemmas"
    )
    main(parser.parse_args())
