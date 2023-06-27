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
from typing import Counter, Tuple, Any

# The alphabet is based on Biggs 2013 English-Māori Māori-English
# Dictionary. <ng> and <wh> are diagraphs, but I treat them as
# separete characters; they correspond to [ŋ] and [ɸ] respectively.
vowels = {
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

consonants = {
    "h",
    "k",
    "m",
    "n",
    "g",
    "p",
    "r",
    "t",
    "w",
    # Consonantal phonemes that correspond to the two diagraphs,
    # <ng> and <wh>, respectively
    # "ŋ",
    # "ɸ",
}

suffixes = {
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

# Sound features are based on Harlow 1996, Māori
vowel_features_dict = {
    "a": ("low", "back", "unround", "short"),
    "ā": ("low", "back", "unround", "long"),
    "e": ("mid", "front", "unround", "short"),
    "ē": ("mid", "front", "unround", "long"),
    "i": ("high", "front", "unround", "short"),
    "ī": ("high", "front", "unround", "long"),
    "o": ("mid", "back", "round", "short"),
    "ō": ("mid", "back", "round", "long"),
    "u": ("high", "central", "round", "short"),
    "ū": ("high", "central", "round", "long"),
}

consonant_features_dict = {
    "h": ("voiceless", "glottal", "oral", "fricative"),
    "k": ("voiceless", "velar", "oral", "stop"),
    "m": ("voiced", "bilabial", "nasal", "stop"),
    "n": ("voiced", "dental", "nasal", "stop"),
    "ng": ("voiced", "velar", "nasal", "stop"),
    "p": ("voiceless", "bilabial", "oral", "stop"),
    "r": ("voiced", "dental-alveolar", "oral", "flap"),
    "t": ("voiceless", "dental", "oral", "stop"),
    "w": ("voiced", "bilabial", "oral", "approximant"),
    "wh": ("voiceless", "labio-dental", "oral", "fricative"),
}


def main(args: argparse.Namespace) -> None:
    # PART 1 - Stem-final vowels and passives
    # Counter for stem-final vowels
    final_vowel: Counter[str] = collections.Counter()
    # Counter for stem-final vowels and suffixes
    final_vowel_suffix: Counter[Tuple[str, str]] = collections.Counter()
    # Reading from an input file and writing into .tsv files

    # PART 2 – Vowel sequences and passives
    # Vowel sequences
    vowel_seq: Counter[str] = collections.Counter()
    # Vowel sequence-passive counter
    vowel_seq_suffix: Counter[Tuple[str, str]] = collections.Counter()

    # PART 3 - Consonant sequences and passives
    # Consonant sequences
    cons_seq: Counter[str] = collections.Counter()
    # Consonant sequence-passive counter
    cons_seq_suffix: Counter[Tuple[str, str]] = collections.Counter()

    # PART 4 – Vowel features and passives
    # Vowel features
    vowel_features: Counter[Tuple[str, ...]] = collections.Counter()
    # Vowel feature-passive counter
    vowel_features_suffix: Counter[Tuple[Any, ...]] = collections.Counter()

    # PART 5 – Consonant features and passives
    # Consonant features
    cons_features: Counter[Tuple[str, ...]] = collections.Counter()
    # Consonant feature-passive counter
    cons_features_suffix: Counter[Tuple[Any, ...]] = collections.Counter()

    # PART 1 – Stem-final vowels and passives
    with open(args.input, "r") as source, open(
        args.output1, "w"
    ) as sink1, open(args.output2, "w") as sink2, open(
        args.output3, "w"
    ) as sink3:
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
            for vowel in vowels:
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
        for (vowel, suffix), count in final_vowel_suffix.items():
            p = count / final_vowel[vowel]
            tsv_writer3.writerow([vowel, suffix, p])

    # PART 2 – Vowel sequences and passives
    with open(args.input, "r") as source, open(
        args.output4, "w"
    ) as sink4, open(args.output5, "w") as sink5, open(
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
                if char in vowels:
                    current_sequence += char
            # I unindented the following statement once, as well.
            if current_sequence:
                vowel_seq[current_sequence] += 1
                vowel_seq_suffix[(current_sequence, suffix)] += 1
        # Writing the vowel sequences into a tsv file
        for seq, count in vowel_seq.most_common():
            tsv_writer4.writerow([seq, count])
        # Writing the vowel seq-suffix counts into a tsv file
        for (
            current_sequence,
            suffix,
        ), count in vowel_seq_suffix.most_common():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            tsv_writer5.writerow([current_sequence, suffix, count])
        # Conditional Probability: p(passive|vowel_sequence)
        for (sequence, suffix), count in vowel_seq_suffix.items():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            p = count / vowel_seq[sequence]
            tsv_writer6.writerow([sequence, suffix, p])

    # PART 3 – Consonant sequences and passives
    with open(args.input, "r") as source, open(
        args.output7, "w"
    ) as sink7, open(args.output8, "w") as sink8, open(
        args.output9, "w"
    ) as sink9:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Consonant sequence: output7
        tsv_writer7 = csv.writer(sink7, delimiter="\t")
        # Consonant seq-passive: output8
        tsv_writer8 = csv.writer(sink8, delimiter="\t")
        # Consonant seq-passive conditional probabilities: output9
        tsv_writer9 = csv.writer(sink9, delimiter="\t")

        # Filling the counters for consonant sequences and passives
        for lemma, suffix in tsv_reader:
            current_sequence = ""
            for char in lemma:
                if char in consonants:
                    current_sequence += char
            # I unindented the following statement once to count each
            # sequence only once rather than counting everything
            # incrementally, which is what happened before
            if current_sequence:
                cons_seq[current_sequence] += 1
                cons_seq_suffix[(current_sequence, suffix)] += 1
        # Writing the consonant sequences into a tsv file
        for seq, count in cons_seq.most_common():
            tsv_writer7.writerow([seq, count])
        # Writing the consonant seq-suffix counts into a tsv file
        for (
            current_sequence,
            suffix,
        ), count in cons_seq_suffix.most_common():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            tsv_writer8.writerow([current_sequence, suffix, count])
        # Conditional Probability: p(passive|vowel_sequence)
        for (sequence, suffix), count in cons_seq_suffix.items():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            p = count / cons_seq[sequence]
            tsv_writer9.writerow([sequence, suffix, p])

    # PART 4 – Vowel features and passives
    with open(args.input, "r") as source, open(
        args.output10, "w"
    ) as sink10, open(args.output11, "w") as sink11, open(
        args.output12, "w"
    ) as sink12:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Vowel features: output10
        tsv_writer10 = csv.writer(sink10, delimiter="\t")
        # Vowel features-passive: output11
        tsv_writer11 = csv.writer(sink11, delimiter="\t")
        # Vowel features-passive conditional probabilities: output12
        tsv_writer12 = csv.writer(sink12, delimiter="\t")

        # Filling the counters for vowel features and passives
        for lemma, suffix in tsv_reader:
            # vowel_feature_sequence: tuple[Any, ...] = ()
            vowel_feature_sequence = []
            for char in lemma:
                if char in vowel_features_dict:
                    vowel_feature_sequence.append(vowel_features_dict[char])
            # I unindented the following statement once to count each
            # sequence only once rather than counting everything
            # incrementally, which is what happened before
            if vowel_feature_sequence:
                vowel_features[tuple(vowel_feature_sequence)] += 1
                vowel_features_suffix[
                    (tuple(vowel_feature_sequence), suffix)
                ] += 1
        # Writing the vowel features into a tsv file
        for feature, count in vowel_features.most_common():
            tsv_writer10.writerow([feature, count])
        # Writing the vowel feature-suffix counts into a tsv file
        for (
            feature,
            suffix,
        ), count in vowel_features_suffix.most_common():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            tsv_writer11.writerow([feature, suffix, count])
        # Conditional Probability: p(passive|vowel_features)
        for (vowel_feature, suffix), count in vowel_features_suffix.items():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            p = count / vowel_features[vowel_feature]
            tsv_writer12.writerow([vowel_feature, suffix, p])

    # PART 5 – Consonant features and passives
    with open(args.input, "r") as source, open(
        args.output13, "w"
    ) as sink13, open(args.output14, "w") as sink14, open(
        args.output15, "w"
    ) as sink15:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Vowel features: output10
        tsv_writer13 = csv.writer(sink13, delimiter="\t")
        # Vowel features-passive: output11
        tsv_writer14 = csv.writer(sink14, delimiter="\t")
        # Vowel features-passive conditional probabilities: output12
        tsv_writer15 = csv.writer(sink15, delimiter="\t")

        # Filling the counters for consonant features and passives
        for lemma, suffix in tsv_reader:
            consonant_feature_sequence = []
            # Traversing each character for the digraphs and the rest
            i = 0
            while i < len(lemma):
                char = lemma[i]
                # Checking for <ng> digraph
                if char == "n" and i + 1 < len(lemma) and lemma[i + 1] == "g":
                    consonant_feature_sequence.append(
                        consonant_features_dict["ng"]
                    )
                    i += 2
                    continue
                # Checking for <wh> digraph
                if char == "w" and i + 1 < len(lemma) and lemma[i + 1] == "h":
                    consonant_feature_sequence.append(
                        consonant_features_dict["wh"]
                    )
                    i += 2
                    continue
                # Checking for other consonantal segments
                if char in consonant_features_dict:
                    consonant_feature_sequence.append(
                        consonant_features_dict[char]
                    )
                i += 1
            # Handling the counter
            if consonant_feature_sequence:
                cons_features[tuple(consonant_feature_sequence)] += 1
                cons_features_suffix[
                    (tuple(consonant_feature_sequence), suffix)
                ] += 1
        # Writing the consonant features into a tsv file
        for feature, count in cons_features.most_common():
            tsv_writer13.writerow([feature, count])
            # print(f"{feature}:\t{count}")
        # Writing the consonant feature seq-suffix counts into a tsv file
        for (
            feature,
            suffix,
        ), count in cons_features_suffix.most_common():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            tsv_writer14.writerow([feature, suffix, count])
        # Conditional Probability: p(passive|consonant_features)
        for (consonant_feature, suffix), count in cons_features_suffix.items():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            p = count / cons_features[consonant_feature]
            tsv_writer15.writerow([consonant_feature, suffix, p])
                # print(f"{consonant_feature}\t{suffix}:\t{count}\t{p}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", required=True, help="input Maori TSV file"
    )
    parser.add_argument(
        "-o1",
        "--output1",
        required=True,
        help="outputs stem-final vowel counts",
    )
    parser.add_argument(
        "-o2",
        "--output2",
        required=True,
        help="outputs the final vowel-suffix counts",
    )
    parser.add_argument(
        "-o3",
        "--output3",
        required=True,
        help="outputs p(passive|final_vowel)",
    )
    parser.add_argument(
        "-o4",
        "--output4",
        required=True,
        help="outputs vowel sequence counts",
    )
    parser.add_argument(
        "-o5",
        "--output5",
        required=True,
        help="outputs vowel sequence-passive counts",
    )
    parser.add_argument(
        "-o6",
        "--output6",
        required=True,
        help="outputs p(passive|vowel_sequence)",
    )
    parser.add_argument(
        "-o7",
        "--output7",
        required=True,
        help="outputs consonant sequence counts",
    )
    parser.add_argument(
        "-o8",
        "--output8",
        required=True,
        help="outputs consonant sequence-passive counts",
    )
    parser.add_argument(
        "-o9",
        "--output9",
        required=True,
        help="outputs p(passive|consonant_sequence)",
    )
    parser.add_argument(
        "-o10",
        "--output10",
        required=True,
        help="outputs vowel feature counts",
    )
    parser.add_argument(
        "-o11",
        "--output11",
        required=True,
        help="outputs vowel feature-passive counts",
    )
    parser.add_argument(
        "-o12",
        "--output12",
        required=True,
        help="outputs p(passive|vowel_feature)",
    )
    parser.add_argument(
        "-o13",
        "--output13",
        required=True,
        help="outputs consonant feature counts",
    )
    parser.add_argument(
        "-o14",
        "--output14",
        required=True,
        help="outputs consonant feature-passive counts",
    )
    parser.add_argument(
        "-o15",
        "--output15",
        required=True,
        help="outputs p(passive|consonant_feature)",
    )
    main(parser.parse_args())