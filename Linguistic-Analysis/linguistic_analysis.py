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
# Dictionary. Even though I have <n, g, w, h> as single entries
# in the consonant dictionary, they are handled as diagraphs in
# the consonant sequences.
vowels = {
    # Diphthongs
    "ae",
    "aae",
    "ai",
    "aai",
    "ao",
    "aao",
    "au",
    "aau",
    "ou",
    "oou",
    "ei",
    "ie",
    "eo",
    "eu",
    "ea",
    "ia",
    "oa",
    "ua",
    "oi",
    "oe",
    "iu",
    "io"
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
}

# Diphthongs are also based on Biggs 2013. They are used
# to handle syllable counts.
# diphthongs = {
#     "ae",
#     "aae",
#     "ai",
#     "aai",
#     "ao",
#     "aao",
#     "au",
#     "aau",
#     "ou",
#     "oou",
#     "ei",
#     "ie",
#     "eo",
#     "eu",
#     "ea",
#     "ia",
#     "oa",
#     "ua",
#     "oi",
#     "oe",
#     "iu",
#     "io"
# }

reduplications = {
    "ahuahu",
    "akiaki",
    "ākirikiri",
    "amuamu",
    "apoapo",
    "aruaru",
    "haehae",
    "hakuhaku",
    "herehere",
    "heuheu",
    "hiahia",
    "hihira",
    "hihiri",
    "hirihiri",
    "hokohoko",
    "hongihongi",
    "houhou",
    "huihui",
    "hukihuki",
    "hunuhunu",
    "iheuheu",
    "ihiihi",
    "kakaro",
    "kakau",
    "kaukau",
    "ketuketu",
    "kikini",
    "kohikohi",
    "māharahara",
    "mahimahi",
    "mātakitaki",
    "mekemeke",
    "memeke",
    "mitimiti",
    "muimui",
    "mukumuku",
    "mutumutu",
    "nanao",
    "nekeneke",
    "ngaungau",
    "nukunuku",
    "pākarukaru",
    "panipani",
    "pehipehi",
    "piupiu",
    "poipoi",
    "pōpopo",
    "poroporo",
    "purupuru",
    "rahoraho",
    "rangirangi",
    "rārangi",
    "rarapi",
    "rarawhi",
    "riringi",
    "rurerure",
    "ruruku",
    "tāhawahawa",
    "tahitahi",
    "taitai",
    "takitaki",
    "tāmuimui",
    "tamumu",
    "tāpapa",
    "tāpāpā",
    "tapatapa",
    "tapatapahi",
    "tautohetohe",
    "titokotoko",
    "tokotoko",
    "toutou",
    "tuhituhi",
    "tuitui",
    "tuketuke",
    "tukutuku",
    "tunutunu",
    "uiui",
    "uwhiuwhi",
    "waawaahi",
    "wareware",
    "wawata",
    "wehewehe",
    "wetewete",
    "whaawhaa",
    "whaiwhai",
    "whakahohori",
    "whakahohoro",
    "whakahorohoro",
    "whakaipoipo",
    "whakakakara",
    "whakakopakopa",
    "whakakorokoro",
    "whakamātaotao",
    "whakamātautau",
    "whakapaipai",
    "whakapakeke",
    "whakapakoko",
    "whakapōhēhē",
    "whakarāpopoto",
    "whakataetae",
    "whakatakitaki",
    "whakatākotokoto",
    "whakatangitangi",
    "whakataratara",
    "whakatikatika",
    "whanowhano",
    "whatiwhati",
    "whāwhā",
    "whawhai",
    "whāwhāi",
    "whiriwhiri",
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
    # FINAL VOWEL FEATURES
    # Stem-final vowel features counter
    final_vowel_features: Counter[Tuple[str, ...]] = collections.Counter()
    # Stem-final vowel feature-passive counter
    final_vowel_features_suffix: Counter[
        Tuple[Any, ...]
    ] = collections.Counter()

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

    # PART 6 – Final consonant features and passives
    # Final consonant features counter
    final_cons_features: Counter[Tuple[str, ...]] = collections.Counter()
    # Final consonant feature-passive counter
    final_cons_features_suffix: Counter[
        Tuple[Any, ...]
    ] = collections.Counter()

    # PART 7 – Syllable counts and passives
    # Syllable counter
    syllable_count: Counter[str] = collections.Counter()
    # Syllable-passive counter
    syllable_suffix_count: Counter[Tuple[str, str]] = collections.Counter()

    # PART 1 – Stem-final vowels and passives
    with open(args.input, "r") as source, open(
        args.output1, "w"
    ) as sink1, open(args.output2, "w") as sink2, open(
        args.output3, "w"
    ) as sink3, open(
        args.output4, "w"
    ) as sink4, open(
        args.output5, "w"
    ) as sink5, open(
        args.output6, "w"
    ) as sink6:
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
                        final_vowel_feature_sequence.append(
                            vowel_features_dict[vowel]
                        )

            # FEATURES
            # Checking if the final_vowel_features_seq is non-empty
            if final_vowel_feature_sequence:
                final_vowel_features[tuple(final_vowel_feature_sequence)] += 1
                final_vowel_features_suffix[
                    (tuple(final_vowel_feature_sequence), suffix)
                ] += 1

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
            p = round(count / final_vowel[vowel], 4)
            # Outputting vowel, suffix, total final vowel count per suffix,
            # the probabilities, and total final vowel count out of 890
            tsv_writer3.writerow(
                [
                    vowel,
                    suffix,
                    final_vowel_suffix[(vowel, suffix)],
                    p,
                    final_vowel[vowel],
                ]
            )

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
            p = round(count / final_vowel_features[feature], 4)
            # Outputting vowel features, suffix, total vowel
            # feature sequence-suffix counts, the probabilities,
            # and total vowel feature counts out of 890
            tsv_writer6.writerow(
                [
                    feature,
                    suffix,
                    final_vowel_features_suffix[(feature, suffix)],
                    p,
                    final_vowel_features[feature],
                ]
            )

    # PART 2 – Vowel sequences and passives
    with open(args.input, "r") as source, open(
        args.output7, "w"
    ) as sink7, open(args.output8, "w") as sink8, open(
        args.output9, "w"
    ) as sink9:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Vowel sequence: output7
        tsv_writer7 = csv.writer(sink7, delimiter="\t")
        # Vowel seq-passive: output8
        tsv_writer8 = csv.writer(sink8, delimiter="\t")
        # Vowel seq-passive conditional probabilities: output9
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
            sequence,
            suffix,
        ), count in vowel_seq_suffix.most_common():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            tsv_writer8.writerow([sequence, suffix, count])
        # Conditional Probability: p(passive|vowel_sequence)
        for (sequence, suffix), count in vowel_seq_suffix.items():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            p = round(count / vowel_seq[sequence], 4)
            # Outputting vowel sequence, suffix, vowel seq-suffix counts,
            # the probabilities, and total vowel seq counts out of 890
            tsv_writer9.writerow(
                [
                    sequence,
                    suffix,
                    vowel_seq_suffix[(sequence, suffix)],
                    p,
                    vowel_seq[sequence],
                ]
            )

    # PART 3 – Consonant sequences and passives
    with open(args.input, "r") as source, open(
        args.output10, "w"
    ) as sink10, open(args.output11, "w") as sink11, open(
        args.output12, "w"
    ) as sink12:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Consonant sequence: output10
        tsv_writer10 = csv.writer(sink10, delimiter="\t")
        # Consonant seq-passive: output11
        tsv_writer11 = csv.writer(sink11, delimiter="\t")
        # Consonant seq-passive conditional probabilities: output12
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
            sequence,
            suffix,
        ), count in cons_seq_suffix.most_common():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            tsv_writer11.writerow([sequence, suffix, count])
        # Conditional Probability: p(passive|vowel_sequence)
        for (sequence, suffix), count in cons_seq_suffix.items():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            p = round(count / cons_seq[sequence], 4)
            # Outputting consonant sequence, suffix, consonant seq-suffix
            # counts, the probabilities, and cons seq-suffix counts out of 890
            tsv_writer12.writerow(
                [
                    sequence,
                    suffix,
                    cons_seq_suffix[(sequence, suffix)],
                    p,
                    cons_seq[sequence],
                ]
            )

    # PART 4 – Vowel features and passives
    with open(args.input, "r") as source, open(
        args.output13, "w"
    ) as sink13, open(args.output14, "w") as sink14, open(
        args.output15, "w"
    ) as sink15:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Vowel features: output112
        tsv_writer13 = csv.writer(sink13, delimiter="\t")
        # Vowel features-passive: output14
        tsv_writer14 = csv.writer(sink14, delimiter="\t")
        # Vowel features-passive conditional probabilities: output15
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
        for v_feature, count in vowel_features.most_common():
            tsv_writer13.writerow([v_feature, count])
        # Writing the vowel feature-suffix counts into a tsv file
        for (
            v_feature,
            suffix,
        ), count in vowel_features_suffix.most_common():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            tsv_writer14.writerow([v_feature, suffix, count])
        # Conditional Probability: p(passive|vowel_features)
        for (v_feature, suffix), count in vowel_features_suffix.items():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            p = round(count / vowel_features[v_feature], 4)
            # Outputting vowel features, suffix, vowel feat-suffix counts,
            # the probabilities, and vowel feat counts out of 890
            tsv_writer15.writerow(
                [
                    v_feature,
                    suffix,
                    vowel_features_suffix[(v_feature, suffix)],
                    p,
                    vowel_features[v_feature],
                ]
            )

    # PART 5 & 6 – Consonant features and passives
    with open(args.input, "r") as source, open(
        args.output16, "w"
    ) as sink16, open(args.output17, "w") as sink17, open(
        args.output18, "w"
    ) as sink18, open(
        args.output19, "w"
    ) as sink19, open(
        args.output20, "w"
    ) as sink20, open(
        args.output21, "w"
    ) as sink21:
        # open(args.output22, "w") as sink22:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Consonant features: output16
        tsv_writer16 = csv.writer(sink16, delimiter="\t")
        # Consonant features-passive: output17
        tsv_writer17 = csv.writer(sink17, delimiter="\t")
        # Consonant features-passive conditional probabilities: output18
        tsv_writer18 = csv.writer(sink18, delimiter="\t")

        # PART 6 – Final consonant features
        # Final consonant feature counts: output19
        tsv_writer19 = csv.writer(sink19, delimiter="\t")
        # Final consonant feature-suffix counts: output20
        tsv_writer20 = csv.writer(sink20, delimiter="\t")
        # Final consonant features-passive conditional probabilities: output21
        tsv_writer21 = csv.writer(sink21, delimiter="\t")
        # # The following is for lemma-cons feat seq for testing purposes
        # tsv_writer22 = csv.writer(sink22, delimiter="\t")

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
            # # The following gives the lemma-cons feature sequence
            # # for testing purposes. The outputted file is in Data/5_...
            # tsv_writer22.writerow([lemma, consonant_feature_sequence])

            # PART 6
            # Final consonant features:
            final_cons_features_sequence = []
            if len(consonant_feature_sequence) >= 1:
                final_cons_features_sequence.append(
                    consonant_feature_sequence[-1]
                )
                final_cons_features[tuple(final_cons_features_sequence)] += 1
                final_cons_features_suffix[
                    (tuple(final_cons_features_sequence), suffix)
                ] += 1

            # PART 5 – Consonant Features Sequence
            # Handling the consonant feature sequence counter
            if consonant_feature_sequence:
                cons_features[tuple(consonant_feature_sequence)] += 1
                cons_features_suffix[
                    (tuple(consonant_feature_sequence), suffix)
                ] += 1
        # Writing the consonant features into a tsv file
        for c_feature, count in cons_features.most_common():
            tsv_writer16.writerow([c_feature, count])
            # print(f"{feature}:\t{count}")
        # Writing the consonant feature seq-suffix counts into a tsv file
        for (
            c_feature,
            suffix,
        ), count in cons_features_suffix.most_common():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            tsv_writer17.writerow([c_feature, suffix, count])
        # Conditional Probability: p(passive|consonant_features)
        for (c_feature, suffix), count in cons_features_suffix.items():
            # I removed the /-hia,-mia,-ria/ restriction based on
            # Kyle's suggestion
            # if suffix in ["hia", "mia", "ria"]:
            p = round(count / cons_features[c_feature], 4)
            # Outputting consontn features, suffix, cons feature-suffix
            # counts, the probabilities, cons feat counts out of 890
            tsv_writer18.writerow(
                [
                    c_feature,
                    suffix,
                    cons_features_suffix[(c_feature, suffix)],
                    p,
                    cons_features[c_feature],
                ]
            )
            # print(f"{consonant_feature}\t{suffix}:\t{count}\t{p}")

        # PART 6 – Final Consonant Features
        # Writing the final consonant features into a tsv file
        for feature, count in final_cons_features.most_common():
            tsv_writer19.writerow([feature, count])
        for (
            feature,
            suffix,
        ), count in final_cons_features_suffix.most_common():
            tsv_writer20.writerow([feature, suffix, count])
        for (feature, suffix), count in final_cons_features_suffix.items():
            p = round(count / final_cons_features[feature], 4)
            tsv_writer21.writerow(
                [
                    feature,
                    suffix,
                    final_cons_features_suffix[(feature, suffix)],
                    p,
                    final_cons_features[feature],
                ]
            )

    # PART 7 – Syllable counts and passives
    with open(args.input, "r") as source, open(
        args.output23, "w"
    ) as sink23, open(args.output24, "w") as sink24, open(
        args.output25, "w"
    ) as sink25:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Syllable counts: output23
        tsv_writer23 = csv.writer(sink23, delimiter="\t")
        # Syllable-passive counts: output24
        tsv_writer24 = csv.writer(sink24, delimiter="\t")
        # Syllable count-passive conditional probabilities: output25
        tsv_writer25 = csv.writer(sink25, delimiter="\t")

        # Counting the syllables and passives
        for lemma, suffix in tsv_reader:
            syllable_sequence = ""
            # Skipping reduplications
            if lemma in reduplications:
                continue
            for sound in vowels:
                if sound in lemma:
                    syllable_sequence += "σ"
                    print(lemma, sound)

            if syllable_sequence:
                syllable_count[syllable_sequence] += 1
                syllable_suffix_count[syllable_sequence, suffix] += 1
            
            print(lemma, syllable_sequence)

        for syllable, count in syllable_count.most_common():
            tsv_writer23.writerow([syllable, count])
        for (syllable, suffix), count in syllable_suffix_count.most_common():
            tsv_writer24.writerow([syllable, suffix, count])
        for (syllable, suffix), count in syllable_suffix_count.items():
            p = round(count / syllable_count[syllable_sequence], 4)
            tsv_writer25.writerow(
                [
                    syllable,
                    suffix,
                    syllable_suffix_count[(syllable, suffix)],
                    p,
                    syllable_count[syllable],
                ]
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        default="lemma-suffix_only.tsv",
        help="input Maori TSV file",
    )
    parser.add_argument(
        "-o1",
        "--output1",
        default="01_final-V_counts.tsv",
        help="outputs stem-final vowel counts",
    )
    parser.add_argument(
        "-o2",
        "--output2",
        default="01_final-V-suffix_counts.tsv",
        help="outputs the final vowel-suffix counts",
    )
    parser.add_argument(
        "-o3",
        "--output3",
        default="01_final-V-suffix_prob.tsv",
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
    parser.add_argument(
        "-o19",
        "--output19",
        default="6_final-C-feat_counts.tsv",
        help="outputs final consonant feature counts",
    )
    parser.add_argument(
        "-o20",
        "--output20",
        default="6_final-C-feat-suffix_counts.tsv",
        help="outputs the final vowel feature-suffix counts",
    )
    parser.add_argument(
        "-o21",
        "--output21",
        default="6_final-C-feat-suffix_prob.tsv",
        help="outputs p(passive|final_vowel_feature)",
    )
    # # -o22 gives all lemma-cons feature sequences for testing
    # # purposes
    # parser.add_argument(
    #     "-o22",
    #     "--output22",
    #     default="7_lemma-C-feat-.tsv",
    #     help="outputs p(passive|final_vowel_feature)",
    # )
    parser.add_argument(
        "-o23",
        "--output23",
        default="7_syllable_counts.tsv",
        help="outputs final consonant feature counts",
    )
    parser.add_argument(
        "-o24",
        "--output24",
        default="7_syllable-suffix_counts.tsv",
        help="outputs the final vowel feature-suffix counts",
    )
    parser.add_argument(
        "-o25",
        "--output25",
        default="7_syllable-suffix_prob.tsv",
        help="outputs p(passive|syllable-counts)",
    )
    main(parser.parse_args())
