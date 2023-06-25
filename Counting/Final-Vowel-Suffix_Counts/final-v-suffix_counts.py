#!/usr/bin/env python

"""This script counts stem-final vowels and final-vowel & passive-suffix pairs
attached to verbs in Maori.The verbs going through various internal changes
are not accounted for in this script. The counts are written into two separate
tsv files."""

import argparse
import collections
import csv
from typing import Counter, Tuple

# The alphabet: https://teara.govt.nz/en/interactive/41063/the-maori-alphabet
# <ng> and <wh> are diagraphs, but we treat them as separete characters 
# while including their corresponding phonemes.
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

consonant_dict = {
    # Adding <f> for fakarārangi from Parker Jones' list
    "f",
    "h",
    "k",
    "m",
    "n",
    "g",
    "p",
    "r",
    "t",
    "w",
    "ā",
    "ē",
    "ī",
    "ō",
    "ū",
    # Consonantal phonemes that correspond to the two diagraphs, <ng> and <wh>, respectively
    "ŋ",
    "ɸ",
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
    # Counter for stem-final vowels
    final_vowel: Counter[str] = collections.Counter()
    # Counter for stem-final vowels and suffixes
    final_vowel_suffix = collections.Counter()
    # Reading from an input file and writing into 3 tsv files
    with open(args.input, "r") as source, open(
        args.output1, "w"
    ) as sink1, open(args.output2, "w") as sink2, open(
        args.output3, "w"
    ) as sink3:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Vowel-count output file
        tsv_writer1 = csv.writer(sink1, delimiter="\t")
        # Vowel-suffix count output file
        tsv_writer2 = csv.writer(sink2, delimiter="\t")
        # Probability output file
        tsv_writer3 = csv.writer(sink3, delimiter="\t")
        for lemma, suffix in tsv_reader:
            for vowel in vowel_dict:
                if lemma.endswith(vowel):
                    final_vowel[vowel] += 1
                    final_vowel_suffix[(vowel, suffix)] += 1
        # Writing the vowel-vowel counts into a tsv file
        for vowel, count in final_vowel.most_common():
            tsv_writer1.writerow([vowel, count])
            # print(f"{vowel}:\t{count}")
        # print(final_vowel_counts)
        # print("\n")

        # Writing the vowel-suffix counts into a tsv file
        for (vowel, suffix), count in final_vowel_suffix.most_common():
            tsv_writer2.writerow([vowel, suffix, count])
            # print(f"{vowel}\t{suffix}:\t{count}")

        # Conditional probabilities of suffixes given stem-final vowel
        for (vowel1, suffix), count1 in final_vowel_suffix.items():
            for vowel2, count2 in final_vowel.items():
                if vowel1 == vowel2:
                    # The following only outputs the probabilities for "hia", "mia", "ria"
                    # if suffix in ["hia", "mia", "ria"]:
                    p = count1 / count2
                    tsv_writer3.writerow([vowel1, suffix, p])
                        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="input Maori TSV file")
    parser.add_argument(
        "--output1",
        required=True,
        help="output stem-final vowels and vowel-suffix pairs with counts",
    )
    parser.add_argument(
        "--output2", required=True, help="outputs the vowel-suffix counts"
    )
    parser.add_argument(
        "--output3",
        required=True,
        help="outputs vowel/suffix count probabilities",
    )
    main(parser.parse_args())
