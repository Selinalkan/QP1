#!/usr/bin/env python

"""This script counts stem-final vowels and final-vowel & passive-suffix pairs attached to verbs in
     Maori.The verbs going through various internal changes are not accounted
     for in this script."""

import argparse
import collections
import csv

vowel_dict = {
    # Short vowels
    "a",
    "e",
    "i",
    "o",
    "u",
    # Long vowels
    "ā",
    "ē",
    "ī",
    "ō",
    "ū",
}

suffix_dict = {
    "tia",
    "a",
    "hia",
    "ia",
    "ina",
    "kia",
    "mia",
    "na",
    "nga",
    "ngia",
    "ria",
    "kina",
}


def main(args: argparse.Namespace) -> None:
    final_vowel_counts = collections.Counter()
    final_v_suffix_counts = collections.Counter()
    with open(args.input, "r") as source, open(args.output, "w") as sink:
        tsv_reader = csv.reader(source, delimiter="\t")
        tsv_writer = csv.writer(sink, delimiter="\t")
        for lemma, suffix in tsv_reader:
            for vowel in vowel_dict:
                if lemma.endswith(vowel):
                    final_vowel_counts[vowel] += 1
                    final_v_suffix_counts[(vowel, suffix)] += 1
        for vowel, count in final_vowel_counts.most_common():
            tsv_writer.writerow(
                [vowel, count]
            )  # need to give a list as an argument
        for (vowel, suffix), count in final_v_suffix_counts.most_common():
            tsv_writer.writerow([vowel, suffix, count])
            print(f"{vowel}:\t{count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="input Maori TSV file")
    parser.add_argument(
        "--output", required=True, help="output stem-final vowels with counts"
    )
    main(parser.parse_args())
