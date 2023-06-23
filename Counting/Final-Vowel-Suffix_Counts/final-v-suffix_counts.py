#!/usr/bin/env python

"""This script counts stem-final vowels and final-vowel & passive-suffix pairs
attached to verbs in Maori.The verbs going through various internal changes
are not accounted for in this script. The counts are written into two separate
tsv files."""

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
    # Counter for stem-final vowels
    final_vowel_counts = collections.Counter()
    # Counter for stem-final vowels and suffixes
    final_v_suffix_counts = collections.Counter()
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
                    final_vowel_counts[vowel] += 1
                    final_v_suffix_counts[(vowel, suffix)] += 1
        # Writing the vowel-vowel counts into a tsv file
        for vowel, count in final_vowel_counts.most_common():
            tsv_writer1.writerow([vowel, count])
            print(f"{vowel}:\t{count}")
        # print(final_vowel_counts)
        # print("\n")

        # Writing the vowel-suffix counts into a tsv file
        for (vowel, suffix), count in final_v_suffix_counts.most_common():
            tsv_writer2.writerow([vowel, suffix, count])
            # print(f"{vowel}\t{suffix}:\t{count}")

        # Dividing and outputting the vowel counts by the vowel-suffix counts
        for vowel1, count1 in final_vowel_counts.items():
            for (vowel2, suffix), count2 in final_v_suffix_counts.items():
                if vowel1 == vowel2:
                    p = count1 / count2
                tsv_writer3.writerow([vowel1, vowel2, suffix, p])


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
