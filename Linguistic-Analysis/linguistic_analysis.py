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
# vowel_features_dict = {
#     "a": ("low", "back", "unround", "short"),
#     "ā": ("low", "back", "unround", "long"),
#     "e": ("mid", "front", "unround", "short"),
#     "ē": ("mid", "front", "unround", "long"),
#     "i": ("high", "front", "unround", "short"),
#     "ī": ("high", "front", "unround", "long"),
#     "o": ("mid", "back", "round", "short"),
#     "ō": ("mid", "back", "round", "long"),
#     "u": ("high", "central", "round", "short"),
#     "ū": ("high", "central", "round", "long"),
# }

# Created the version below to save the vowel features
# as a string to get rid of the mypy error, as Kyle
# suggested, but I couldn't figure it out.
# This made thing more readable, though
vowel_features_dict = {
    "a": "low, back, unround, short",
    "ā": "low, back, unround, long",
    "e": "mid, front, unround, short",
    "ē": "mid, front, unround, long",
    "i": "high, front, unround, short",
    "ī": "high, front, unround, long",
    "o": "mid, back, round, short",
    "ō": "mid, back, round, long",
    "u": "high, central, round, short",
    "ū": "high, central, round, long",
}

# consonant_features_dict = {
#     "h": ("voiceless", "glottal", "oral", "fricative"),
#     "k": ("voiceless", "velar", "oral", "stop"),
#     "m": ("voiced", "bilabial", "nasal", "stop"),
#     "n": ("voiced", "dental", "nasal", "stop"),
#     "ng": ("voiced", "velar", "nasal", "stop"),
#     "p": ("voiceless", "bilabial", "oral", "stop"),
#     "r": ("voiced", "dental-alveolar", "oral", "flap"),
#     "t": ("voiceless", "dental", "oral", "stop"),
#     "w": ("voiced", "bilabial", "oral", "approximant"),
#     "wh": ("voiceless", "labio-dental", "oral", "fricative"),
# }

# Turning consonant values into strings for readability
consonant_features_dict = {
    "h": "voiceless, glottal, oral, fricative",
    "k": "voiceless, velar, oral, stop",
    "m": "voiced, bilabial, nasal, stop",
    "n": "voiced, dental, nasal, stop",
    "ng": "voiced, velar, nasal, stop",
    "p": "voiceless, bilabial, oral, stop",
    "r": "voiced, dental-alveolar, oral, flap",
    "t": "voiceless, dental, oral, stop",
    "w": "voiced, bilabial, oral, approximant",
    "wh": "voiceless, labio-dental, oral, fricative",
}


def main(args: argparse.Namespace) -> None:
    # PART 1 - Stem-final vowels and passives
    # Stem-final vowels counter
    final_vowel: Counter[str] = collections.Counter()
    # Stem-final vowels and suffixes counter
    final_vowel_suffix: Counter[Tuple[str, str]] = collections.Counter()
    # Stem-final vowel features counter
    final_vowel_features: Counter[Tuple[str, ...]] = collections.Counter()
    # Stem-final vowel feature-passive counter
    final_vowel_features_suffix: Counter[Tuple[Any, ...]] = collections.Counter()

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
    ) as sink3, open(args.output4, "w") as sink4, open(args.output5, "w") as sink5, open(args.output6, "w") as sink6:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Vowel-count output file: output1
        tsv_writer1 = csv.writer(sink1, delimiter="\t")
        # Vowel-suffix count output file: output2
        tsv_writer2 = csv.writer(sink2, delimiter="\t")
        # Stem-final vowel-suffix probability output file: output3
        tsv_writer3 = csv.writer(sink3, delimiter="\t")
        # FEATURES
        # Stem-final vowel features: output4
        tsv_writer4 = csv.writer(sink4, delimiter="\t")
        # Stem-final vowel features-suffix: output5
        tsv_writer5 = csv.writer(sink5, delimiter="\t")
        # Stem-final vowel features-suffix probability: output6
        tsv_writer6 = csv.writer(sink6, delimiter="\t")

        # Filling in the counters
        for lemma, suffix in tsv_reader:
            final_vowel_feature_sequence = []
            for vowel in vowels:
                if lemma.endswith(vowel):
                    final_vowel[vowel] += 1
                    final_vowel_suffix[(vowel, suffix)] += 1
                    # Collecting final-vowel features
                    if vowel in vowel_features_dict:
                        final_vowel_feature_sequence.append(vowel_features_dict[vowel])
            
            # FEATURES
            # Checking if the final_vowel_features_seq is non-empty
            if final_vowel_feature_sequence:
                final_vowel_features[tuple(final_vowel_feature_sequence)] += 1
                final_vowel_features_suffix[(tuple(final_vowel_feature_sequence), suffix)] += 1

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
            # Outputting vowel, suffix, total final vowel count per vowel,
            # and the probabilities
            tsv_writer3.writerow([vowel, suffix, final_vowel[vowel], p])

        # FEATURES
        # Writing the final vowel feature counts into a tsv file
        for feature, count in final_vowel_features.most_common():
            tsv_writer4.writerow([feature, count])
        # Writing the final vowel feature-suffix counts into a tsv file
        for (
            feature,
            suffix,
        ), count in final_vowel_features_suffix.most_common():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            tsv_writer5.writerow([feature, suffix, count])
        # Conditional Probability: p(passive|final_vowel_features)
        for (feature, suffix), count in final_vowel_features_suffix.items():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            p = count / final_vowel_features[feature]
            # Outputting vowel features, suffix, total vowel
            # feature sequence counts, and the probabilities
            tsv_writer6.writerow([feature, suffix, final_vowel_features[feature], p])

    # PART 2 – Vowel sequences and passives
    with open(args.input, "r") as source, open(
        args.output7, "w"
    ) as sink7, open(args.output8, "w") as sink8, open(
        args.output9, "w"
    ) as sink9:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Vowel sequence: output4
        tsv_writer7 = csv.writer(sink7, delimiter="\t")
        # Vowel seq-passive: output5
        tsv_writer8 = csv.writer(sink8, delimiter="\t")
        # Vowel seq-passive conditional probabilities: output6
        tsv_writer9 = csv.writer(sink9, delimiter="\t")

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
            tsv_writer7.writerow([seq, count])
        # Writing the vowel seq-suffix counts into a tsv file
        for (
            current_sequence,
            suffix,
        ), count in vowel_seq_suffix.most_common():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            tsv_writer8.writerow([current_sequence, suffix, count])
        # Conditional Probability: p(passive|vowel_sequence)
        for (sequence, suffix), count in vowel_seq_suffix.items():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            p = count / vowel_seq[sequence]
            # Outputting vowel sequence, suffix, total vowel seq counts,
            # and the probabilities
            tsv_writer9.writerow([sequence, suffix, vowel_seq[sequence], p])

    # PART 3 – Consonant sequences and passives
    with open(args.input, "r") as source, open(
        args.output10, "w"
    ) as sink10, open(args.output11, "w") as sink11, open(
        args.output12, "w"
    ) as sink12:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Consonant sequence: output7
        tsv_writer10 = csv.writer(sink10, delimiter="\t")
        # Consonant seq-passive: output8
        tsv_writer11 = csv.writer(sink11, delimiter="\t")
        # Consonant seq-passive conditional probabilities: output9
        tsv_writer12 = csv.writer(sink12, delimiter="\t")

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
            tsv_writer10.writerow([seq, count])
        # Writing the consonant seq-suffix counts into a tsv file
        for (
            current_sequence,
            suffix,
        ), count in cons_seq_suffix.most_common():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            tsv_writer11.writerow([current_sequence, suffix, count])
        # Conditional Probability: p(passive|vowel_sequence)
        for (sequence, suffix), count in cons_seq_suffix.items():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            p = count / cons_seq[sequence]
            # Outputting consonant sequence, suffix, total consonant
            # seq counts, and the probabilities
            tsv_writer12.writerow([sequence, suffix, cons_seq[sequence], p])

    # PART 4 – Vowel features and passives
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
                # converting the list to a string as Kyle suggested
                # vowel_features[vowel_feature_sequence] += 1
                vowel_features_suffix[
                    (tuple(vowel_feature_sequence), suffix)
                ] += 1
        # Writing the vowel features into a tsv file
        for feature, count in vowel_features.most_common():
            tsv_writer13.writerow([feature, count])
        # Writing the vowel feature-suffix counts into a tsv file
        for (
            feature,
            suffix,
        ), count in vowel_features_suffix.most_common():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            tsv_writer14.writerow([feature, suffix, count])
        # Conditional Probability: p(passive|vowel_features)
        for (vowel_feature, suffix), count in vowel_features_suffix.items():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            p = count / vowel_features[vowel_feature]
            # Outputting vowel features, suffix, total vowel
            # feature sequence counts, and the probabilities
            tsv_writer15.writerow([vowel_feature, suffix, vowel_features[vowel_feature], p])

    # PART 5 – Consonant features and passives
    with open(args.input, "r") as source, open(
        args.output16, "w"
    ) as sink16, open(args.output17, "w") as sink17, open(
        args.output18, "w"
    ) as sink18:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Vowel features: output10
        tsv_writer16 = csv.writer(sink16, delimiter="\t")
        # Vowel features-passive: output11
        tsv_writer17 = csv.writer(sink17, delimiter="\t")
        # Vowel features-passive conditional probabilities: output12
        tsv_writer18 = csv.writer(sink18, delimiter="\t")

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
            tsv_writer16.writerow([feature, count])
            # print(f"{feature}:\t{count}")
        # Writing the consonant feature seq-suffix counts into a tsv file
        for (
            feature,
            suffix,
        ), count in cons_features_suffix.most_common():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            tsv_writer17.writerow([feature, suffix, count])
        # Conditional Probability: p(passive|consonant_features)
        for (consonant_feature, suffix), count in cons_features_suffix.items():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            p = count / cons_features[consonant_feature]
            # Outputting consontn features, suffix, total consonant
            # feature sequence counts, and the probabilities
            tsv_writer18.writerow([consonant_feature, suffix, cons_features[consonant_feature], p])
                # print(f"{consonant_feature}\t{suffix}:\t{count}\t{p}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", default="lemma-suffix_only.tsv", help="input Maori TSV file"
    )
    parser.add_argument(
        "-o1",
        "--output1",
        default="1_final-V_counts.tsv",
        help="outputs stem-final vowel counts",
    )
    parser.add_argument(
        "-o2",
        "--output2",
        default="1_final-V-suffix_counts.tsv",
        help="outputs the final vowel-suffix counts",
    )
    parser.add_argument(
        "-o3",
        "--output3",
        default="1_final-V-suffix_prob.tsv",
        help="outputs p(passive|final_vowel)",
    )
    parser.add_argument(
        "-o4",
        "--output4",
        default="1_final-V-feat_counts.tsv",
        help="outputs stem-final vowel feature counts",
    )
    parser.add_argument(
        "-o5",
        "--output5",
        default="1_final-V-feat-suffix_counts.tsv",
        help="outputs the final vowel feature-suffix counts",
    )
    parser.add_argument(
        "-o6",
        "--output6",
        default="1_final-V-feat-suffix_prob.tsv",
        help="outputs p(passive|final_vowel_feature)",
    )
    parser.add_argument(
        "-o7",
        "--output7",
        default="2_V-seq_counts.tsv",
        help="outputs vowel sequence counts",
    )
    parser.add_argument(
        "-o8",
        "--output8",
        default="2_V-seq-suffix_counts.tsv",
        help="outputs vowel sequence-passive counts",
    )
    parser.add_argument(
        "-o9",
        "--output9",
        default="2_V-seq-suffix_prob.tsv",
        help="outputs p(passive|vowel_sequence)",
    )
    parser.add_argument(
        "-o10",
        "--output10",
        default="3_C-seq_counts.tsv",
        help="outputs consonant sequence counts",
    )
    parser.add_argument(
        "-o11",
        "--output11",
        default="3_C-seq-suffix_counts.tsv",
        help="outputs consonant sequence-passive counts",
    )
    parser.add_argument(
        "-o12",
        "--output12",
        default="3_C-seq-suffix_prob.tsv",
        help="outputs p(passive|consonant_sequence)",
    )
    parser.add_argument(
        "-o13",
        "--output13",
        default="4_V-feat_counts.tsv",
        help="outputs vowel feature counts",
    )
    parser.add_argument(
        "-o14",
        "--output14",
        default="4_V-feat-suffix_counts.tsv",
        help="outputs vowel feature-passive counts",
    )
    parser.add_argument(
        "-o15",
        "--output15",
        default="4_V-feat-suffix_prob.tsv",
        help="outputs p(passive|vowel_feature)",
    )
    parser.add_argument(
        "-o16",
        "--output16",
        default="5_C-feat_counts.tsv",
        help="outputs consonant feature counts",
    )
    parser.add_argument(
        "-o17",
        "--output17",
        default="5_C-feat-suffix_counts.tsv",
        help="outputs consonant feature-passive counts",
    )
    parser.add_argument(
        "-o18",
        "--output18",
        default="5_C-feat-suffix_prob.tsv",
        help="outputs p(passive|consonant_feature)",
    )
    main(parser.parse_args())
