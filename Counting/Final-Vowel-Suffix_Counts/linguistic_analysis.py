#!/usr/bin/env python

"""
This script examines the Māori verb stem properties and their
correspondences with the suffixes building conditional probabilities
of the form P(suffix|property of the stem). The linguistic features
examined are stem-final vowels, vowel sequences, consonant sequences,
...
"""

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
    # Consonantal phonemes that correspond to the two diagraphs,
    # <ng> and <wh>, respectively
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
    # PART 1 - Stem-final vowels and passives
    # Counter for stem-final vowels
    final_vowel: Counter[str] = collections.Counter()
    # Counter for stem-final vowels and suffixes
    final_vowel_suffix: Counter[Tuple[str, str]] = collections.Counter()
    # Reading from an input file and writing into .tsv files

    # PART 2 – Sounds sequences and passives
    # Vowel sequences
    vowel_seq: Counter[str] = collections.Counter()
    # Vowel sequence-passive counter
    vowel_seq_suffix: Counter[Tuple[str, str]] = collections.Counter()
    # Consonant sequences
    cons_seq: Counter[str] = collections.Counter()
    # Consonant sequence-passive counter
    cons_seq_suffix: Counter[Tuple[str, str]] = collections.Counter()

    # PART 1 – Stem-final vowels and passives
    with open(args.input, "r") as source, open(
        args.output1, "w"
    ) as sink1, open(args.output2, "w") as sink2, open(
        args.output3, "w") as sink3:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Vowel-count output file: output1
        tsv_writer1 = csv.writer(sink1, delimiter="\t")
        # Vowel-suffix count output file: output2
        tsv_writer2 = csv.writer(sink2, delimiter="\t")
        # Stem-final vowel-suffix probability output file: output3
        tsv_writer3 = csv.writer(sink3, delimiter="\t")

        # Filling in the counters
        for lemma, suffix in tsv_reader:
            for vowel in vowel_dict:
                if lemma.endswith(vowel):
                    final_vowel[vowel] += 1
                    final_vowel_suffix[(vowel, suffix)] += 1
        # Writing the final vowel counts into a tsv file
        for vowel, count in final_vowel.most_common():
            tsv_writer1.writerow([vowel, count])
            # print(f"{vowel}:\t{count}")
        # Writing the vowel-suffix counts into a tsv file
        for (vowel, suffix), count in final_vowel_suffix.most_common():
            tsv_writer2.writerow([vowel, suffix, count])
            # print(f"{vowel}\t{suffix}:\t{count}")
        # Conditional Probability: p(passive|final_vowel)
        for (vowel1, suffix), count1 in final_vowel_suffix.items():
            p = count1 / final_vowel[vowel1]
            tsv_writer3.writerow([vowel1, suffix, p])

    # PART 2 – Sound sequences and passives
    with open(args.input, "r") as source, open(
        args.output4, "w"
    ) as sink4, open(
        args.output5, "w"
    ) as sink5, open(
        args.output6, "w"
    ) as sink6:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Vowel sequence: output4
        tsv_writer4 = csv.writer(sink4, delimiter="\t")
        # Vowel seq-passive: output5
        tsv_writer5 = csv.writer(sink5, delimiter="\t")
        # Vowel seq-passive conditional probabilities: output6
        tsv_writer6 = csv.writer(sink6, delimiter="\t")

        # Filling the counters for vowel sequences and passives
        for lemma, suffix in tsv_reader:
            current_sequence = ""
            for char in lemma:
                if char in vowel_dict:
                    current_sequence += char
                if current_sequence:
                    vowel_seq[current_sequence] += 1
                    vowel_seq_suffix[(current_sequence, suffix)] += 1
        # Writing the vowel sequences into a tsv file
        for seq, count in vowel_seq.most_common():
                tsv_writer4.writerow([seq, count])
        # Writing the vowel seq-suffix counts into a tsv file
        for (current_sequence, suffix), count in vowel_seq_suffix.most_common():
            if suffix in ["hia", "mia", "ria"]:
                tsv_writer5.writerow([current_sequence, suffix, count])
        # Conditional Probability: p(passive|vowel_sequence)
        for (sequence1, suffix), count1 in vowel_seq_suffix.items():
            # I left the inner loop and the if-statement because otherwise
            # the vowel order is messed up in the output file
            if suffix in ["hia", "mia", "ria"]:
                p = count1 / vowel_seq[sequence1]
                tsv_writer6.writerow([sequence1, suffix, p])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="input Maori TSV file")
    parser.add_argument("-o1", 
        "--output1",
        required=True,
        help="outputs stem-final vowel counts",
    )
    parser.add_argument("-o2", 
        "--output2", required=True, help="outputs the final vowel-suffix counts"
    )
    parser.add_argument("-o3", 
        "--output3",
        required=True,
        help="outputs p(passive|final_vowel)",
    )
    parser.add_argument("-o4", 
        "--output4",
        required=True,
        help="outputs vowel sequence counts",
    )
    parser.add_argument("-o5", 
        "--output5",
        required=True,
        help="outputs vowel sequence-passive counts",
    )
    parser.add_argument("-o6", 
        "--output6",
        required=True,
        help="outputs p(passive|vowel_sequence)",
    )
    main(parser.parse_args())