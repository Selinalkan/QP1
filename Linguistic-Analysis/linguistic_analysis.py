#!/usr/bin/env python

"""
This program analyzes 886 Māori verb-passive suffix pairs in a TSV file and
performs various computations and counts related to 7 linguistic features. It
focuses on stem-final vowels and passives, vowel sequences and passives,
consonant sequences and passives, vowel features and passives, consonant
features and passives, final consonant features and passives, and syllable
counts and passives.

The program performs the following steps:

PART 0 & 1 - Stem-final vowels and passives:
It counts the occurrences of stem-final vowels.
It counts the occurrences of vowel-suffix combinations.
It calculates the stem-final vowel-suffix probabilities.
It collects the features of stem-final vowels and counts their occurrences.
It counts the occurrences of vowel feature-suffix combinations.
It calculates the vowel feature-suffix probabilities.

PART 2 - Vowel sequences and passives:
It counts the occurrences of vowel sequences.
It counts the occurrences of vowel sequences-suffix combinations.
It calculates the vowel sequence-suffix probabilities.

PART 3 - Consonant sequences and passives:
It counts the occurrences of consonant sequences.
It counts the occurrences of consonant sequence-suffix combinations.
It calculates the consonant sequence-suffix probabilities.

PART 5 - Vowel features and passives:
It counts the occurrences of vowel features.
It counts the occurrences of vowel feature-suffix combinations.
It calculates the vowel feature-suffix probabilities.

PART 6 - Consonant features and passives:
It counts the occurrences of consonant features.
It counts the occurrences of consonant feature-suffix combinations.
It calculates the consonant feature-suffix probabilities.

PART 7 - Final consonant features and passives:
It counts the occurrences of final consonant features.
It counts the occurrences of final consonant feature-suffix combinations.
It calculates the final consonant feature-suffix probabilities.

PART 8 - Syllable counts and passives:
It counts the occurrences of syllables.
It counts the occurrences of syllable-suffix combinations.
It calculates the syllable count-suffix probabilities.

PART 9

PART 10

The program uses several counters from the collections module to keep track
of the counts. The vowel, consonant, diphthong, reduplication, and suffix sets
define the language-specific elements used for counting and analysis.

Note: The program assumes the existence of input and output files specified in
the command-line arguments and writes the results of its analysis to the
respective output files.
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
diphthongs = {
    "ae",
    "āe",
    "ai",
    "āi",
    "ao",
    "āo",
    "au",
    "āu",
    "ou",
    "ōu",
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
    "io",
}

reduplications = {
    "ahuahu",
    "akiaki",
    "ākirikiri",
    "amuamu",
    "apoapo",
    "aruaru",
    "ātete",
    "haehae",
    "hahau",
    "hāhau",
    "hakuhaku",
    "haupapa",
    "herehere",
    "heuheu",
    "hiahia",
    "hihira",
    "hihiri",
    "hirihiri",
    "hohou",
    "hokohoko",
    "hongihongi",
    "houhou",
    "huhu",
    "huihui",
    "hukihuki",
    "hunuhunu",
    "iheuheu",
    "ihiihi",
    "kākahu",
    "kakaro",
    "kakau",
    "kaukau",
    "ketuketu",
    "kiki",
    "kikini",
    "kohikohi",
    "koko",
    "kōpenupenu",
    "kuku",
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
    "onioni",
    "pākarukaru",
    "panipani",
    "pehipehi",
    "piupiu",
    "pōhēhē",
    "poipoi",
    "popo",
    "pōpopo",
    "poroporo",
    "purupuru",
    "rahoraho",
    "rangirangi",
    "rara",
    "rārangi",
    "rarapi",
    "rarawhi",
    "rere",
    "riri",
    "riringi",
    "rurerure",
    "rūrū",
    "ruruku",
    "tāhawahawa",
    "tahitahi",
    "taitai",
    "takapapa",
    "takitaki",
    "tāmuimui",
    "tamumu",
    "tāpapa",
    "tāpāpā",
    "tapatapa",
    "tapatapahi",
    "tātāmi",
    "tātari",
    "tatau",
    "tātāwhi",
    "tautohetohe",
    "tīkoko",
    "titi",
    "tītokotoko",
    "tohatoha",
    "tokotoko",
    "toutou",
    "tuhituhi",
    "tuitui",
    "tuketuke",
    "tukutuku",
    "tunutunu",
    "uiui",
    "uwhiuwhi",
    "wāwāhi",
    "wareware",
    "wawae",
    "wawata",
    "wehewehe",
    "wetewete",
    "whāwhā",
    "whaiwhai",
    "whakahohori",
    "whakahohoro",
    "whakahorohoro",
    "whakaipoipo",
    "whakakakara",
    "whakakopakopa",
    "whakakorokoro",
    "whakamākūkū",
    "whakamāmā",
    "whakamamae",
    "whakamārōrō",
    "whakamātaotao",
    "whakamātautau",
    "whakapaipai",
    "whakapakeke",
    "whakapakoko",
    "whakapapa",
    "whakapōhēhē",
    "whakarāpopoto",
    "whakarere",
    "whakaririki",
    "whakataetae",
    "whakatakitaki",
    "whakatākotokoto",
    "whakatangitangi",
    "whakataratara",
    "whakatata",
    "whakatikatika",
    "whakawāwā",
    "whakawhiwhi",
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

# PART9: [+/-nasal]
# Used to check oral vs nasal feature in consonant sequences
nasality_dict = {
    "h": "o",
    "k": "o",
    "m": "n",
    "n": "n",
    "ng": "n",
    "p": "o",
    "r": "o",
    "t": "o",
    "w": "o",
    "wh": "o",
}

# PART10: place of articulation
# Used to check the place of articulation in consonant sequences
place_dict = {
    # Harlow 2007:63 – Kearns (1990) [h] --> [+high]
    # Blevins: all [+high] are [dorsal] by definition.
    "h": "dorsal",
    "k": "dorsal",
    "m": "labial",
    "n": "coronal",
    "ng": "dorsal",
    "p": "labial",
    "r": "coronal",
    "t": "coronal",
    "w": "labial",
    "wh": "labial",
}

# JULY 29, 2023
# Adding more features upon Prof. Blevins's suggestion:
# [+/-consonantal], [+/- sonorant], [+/-nasal], [coronal],
# [labial], [dorsal], [+/-cont], [+/-voiced], [spread glottis],
# and possible combinations of these.

# PART11: [+/-consonantal]
consonantal_dict = {
    "h": "-cons",
    "k": "+cons",
    "m": "+cons",
    "n": "+cons",
    "ng": "+cons",
    "p": "+cons",
    "r": "+cons",
    "t": "+cons",
    "w": "-cons",
    "wh": "+cons",
}

# PART12: [+/-sonorant]
sonorant_dict = {
    "h": "-son",
    "k": "-son",
    "m": "+son",
    "n": "+son",
    "ng": "+son",
    "p": "-son",
    # r is considered a flap, hence sonorant.
    # Harlod 2007:77
    "r": "+son",
    "t": "-son",
    "w": "+son",
    "wh": "-son",
}

# PART13: [+/-cont]
continuant_dict = {
    "h": "+cont",
    "k": "-cont",
    "m": "-cont",
    "n": "-cont",
    "ng": "-cont",
    "p": "-cont",
    "r": "+cont",
    "t": "-cont",
    "w": "+cont",
    "wh": "+cont",
}

# PART14: [+/-voiced]
# Harlow 1996
voicing_dict = {
    "h": "-voi",
    "k": "-voi",
    "m": "+voi",
    "n": "+voi",
    "ng": "+voi",
    "p": "-voi",
    "r": "+voi",
    "t": "-voi",
    "w": "+voi",
    "wh": "-voi",
}

# PART15: [spread glottis]
spread_g_dict = {
    "h": "+SG",
    "k": "-SG",
    "m": "-SG",
    "n": "-SG",
    "ng": "-SG",
    "p": "-SG",
    "r": "-SG",
    "t": "-SG",
    "w": "-SG",
    "wh": "-SG",
}

def main(args: argparse.Namespace) -> None:
    # PART 0 - Stem-final vowels and passives
    # Stem-final vowels counter
    final_vowel: Counter[str] = collections.Counter()
    # Stem-final vowels-suffix combinations counter
    final_vowel_suffix: Counter[Tuple[str, str]] = collections.Counter()

    # PART 1 - Stem-Final vowel features
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

    # PART 4 - Final consonants
    # Final consonants counter
    final_consonant: Counter[str] = collections.Counter()
    # Final consonants-suffix combinations counter
    final_consonant_suffix: Counter[Tuple[str, str]] = collections.Counter()

    # PART 5 – Vowel features and passives
    # Vowel features
    vowel_features: Counter[Tuple[str, ...]] = collections.Counter()
    # Vowel feature-passive counter
    vowel_features_suffix: Counter[Tuple[Any, ...]] = collections.Counter()

    # PART 6 – Consonant features and passives
    # Consonant features
    cons_features: Counter[Tuple[str, ...]] = collections.Counter()
    # Consonant feature-passive counter
    cons_features_suffix: Counter[Tuple[Any, ...]] = collections.Counter()

    # PART 7 – Final consonant features and passives
    # Final consonant features counter
    final_cons_features: Counter[Tuple[str, ...]] = collections.Counter()
    # Final consonant feature-passive counter
    final_cons_features_suffix: Counter[
        Tuple[Any, ...]
    ] = collections.Counter()

    # PART 8 – Syllable counts and passives
    # Syllable counter
    syllable_count: Counter[str] = collections.Counter()
    # Syllable-passive counter
    syllable_suffix_count: Counter[Tuple[str, str]] = collections.Counter()

    # PART 9 – [+/-nasal]
    # Oral vs nasal consonant sequence
    nasality: Counter[Tuple[str, ...]] = collections.Counter()
    # Oral vs nasal consonant sequence-passive counter
    nasality_suffix: Counter[
        Tuple[Any, ...]
    ] = collections.Counter()

    # PART 10 – [labial], [coronal], [dorsal]
    # PoA of consonant sequences counter
    place: Counter[Tuple[str, ...]] = collections.Counter()
    # # PoA of consonant sequences-passive counter
    place_suffix: Counter[
        Tuple[Any, ...]
    ] = collections.Counter()

    # PART 11 – Sequential [+/-consonantal]
    # phoneme feature counter
    consonantal: Counter[Tuple[str, ...]] = collections.Counter()
    # phoneme feature-suffix counter
    consonantal_suffix: Counter[
        Tuple[Any, ...]
    ] = collections.Counter()

    # PART 12 – Sequential [+/-sonorant]
    # phoneme feature counter
    sonorant: Counter[Tuple[str, ...]] = collections.Counter()
    # phoneme feature-suffix counter
    sonorant_suffix: Counter[
        Tuple[Any, ...]
    ] = collections.Counter()

    # PART 13 – Sequential [+/-continuant]
    # phoneme feature counter
    continuant: Counter[Tuple[str, ...]] = collections.Counter()
    # phoneme feature-suffix counter
    continuant_suffix: Counter[
        Tuple[Any, ...]
    ] = collections.Counter()

    # PART 14 – Sequential [+/-voiced]
    # phoneme feature counter
    voicing: Counter[Tuple[str, ...]] = collections.Counter()
    # phoneme feature-suffix counter
    voicing_suffix: Counter[
        Tuple[Any, ...]
    ] = collections.Counter()

    # PART 15 – Sequential [spread glottis]
    # phoneme feature counter
    spread_g: Counter[Tuple[str, ...]] = collections.Counter()
    # phoneme feature-suffix counter
    spread_g_suffix: Counter[
        Tuple[Any, ...]
    ] = collections.Counter()

########################################################################
    # PART 0 & 1 – Stem-final vowels (0), stem-final vowel features (1)
    # and passives
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
        # PART 0
        # Vowel-count output file: output1
        tsv_writer1 = csv.writer(sink1, delimiter="\t")
        # Vowel-suffix count output file: output2
        tsv_writer2 = csv.writer(sink2, delimiter="\t")
        # Stem-final vowel-suffix probability output file: output3
        tsv_writer3 = csv.writer(sink3, delimiter="\t")
        # PART 1 - Stem-final vowel features
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

            # PART 1 - Stem-final vowel features
            # Checking if the final_vowel_features_seq is non-empty
            if final_vowel_feature_sequence:
                final_vowel_features[tuple(final_vowel_feature_sequence)] += 1
                final_vowel_features_suffix[
                    (tuple(final_vowel_feature_sequence), suffix)
                ] += 1

        # PART 0
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
            # the probabilities, and total final vowel count out of 886
            tsv_writer3.writerow(
                [
                    vowel,
                    suffix,
                    p,
                    final_vowel_suffix[(vowel, suffix)],
                    final_vowel[vowel],
                ]
            )

        # PART 1 - Stem-final vowel features
        # Writing the final vowel feature counts into a tsv file
        for feature, count in final_vowel_features.most_common():
            tsv_writer4.writerow([feature, count])
        # Writing the final vowel feature-suffix counts into a tsv file
        for (
            feature,
            suffix,
        ), count in final_vowel_features_suffix.most_common():
            tsv_writer5.writerow([feature, suffix, count])
        # Conditional Probability: p(passive|final_vowel_features)
        for (feature, suffix), count in final_vowel_features_suffix.items():
            p = round(count / final_vowel_features[feature], 4)
            # Outputting vowel features, suffix, total vowel
            # feature sequence-suffix counts, the probabilities,
            # and total vowel feature counts out of 886
            tsv_writer6.writerow(
                [
                    feature,
                    suffix,
                    p,
                    final_vowel_features_suffix[(feature, suffix)],
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
            tsv_writer8.writerow([sequence, suffix, count])
        # Conditional Probability: p(passive|vowel_sequence)
        for (sequence, suffix), count in vowel_seq_suffix.items():
            p = round(count / vowel_seq[sequence], 4)
            # Outputting vowel sequence, suffix, vowel seq-suffix counts,
            # the probabilities, and total vowel seq counts out of 886
            tsv_writer9.writerow(
                [
                    sequence,
                    suffix,
                    p,
                    vowel_seq_suffix[(sequence, suffix)],
                    vowel_seq[sequence],
                ]
            )

    # PART 3 & 4 – Consonant sequences (3) and final consonants (4)
    with open(args.input, "r") as source, open(
        args.output10, "w"
    ) as sink10, open(args.output11, "w") as sink11, open(
        args.output12, "w"
    ) as sink12, open(
        args.output32, "w"
    ) as sink32, open(
        args.output33, "w"
    ) as sink33, open(
        args.output34, "w"
    ) as sink34:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Consonant sequence: output10
        tsv_writer10 = csv.writer(sink10, delimiter="\t")
        # Consonant seq-passive: output11
        tsv_writer11 = csv.writer(sink11, delimiter="\t")
        # Consonant seq-passive conditional probabilities: output12
        tsv_writer12 = csv.writer(sink12, delimiter="\t")
        # PART 4 - Final consonants
        # Output files
        # Final consonant counts: output32
        tsv_writer32 = csv.writer(sink32, delimiter="\t")
        # Final consonant-suffix combination counts: output33
        tsv_writer33 = csv.writer(sink33, delimiter="\t")
        # Final cons-passive conditional probabilities: output34
        tsv_writer34 = csv.writer(sink34, delimiter="\t")

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

                # PART 4
                if (
                    current_sequence[-2:] == "ng"
                    or current_sequence[-2:] == "wh"
                ):
                    final_cons = current_sequence[-2:]
                else:
                    final_cons = current_sequence[-1:]
                final_consonant[final_cons] += 1
                final_consonant_suffix[(final_cons, suffix)] += 1

        # Writing the consonant sequences into a tsv file
        for seq, count in cons_seq.most_common():
            tsv_writer10.writerow([seq, count])
        # Writing the consonant seq-suffix counts into a tsv file
        for (
            sequence,
            suffix,
        ), count in cons_seq_suffix.most_common():
            tsv_writer11.writerow([sequence, suffix, count])
        # Conditional Probability: p(passive|vowel_sequence)
        for (sequence, suffix), count in cons_seq_suffix.items():
            p = round(count / cons_seq[sequence], 4)
            # Outputting consonant sequence, suffix, consonant seq-suffix
            # counts, the probabilities, and cons seq-suffix counts out of 886
            tsv_writer12.writerow(
                [
                    sequence,
                    suffix,
                    p,
                    cons_seq_suffix[(sequence, suffix)],
                    cons_seq[sequence],
                ]
            )

        # PART 4
        # Writing the final consonants into a tsv file
        for cons, count in final_consonant.most_common():
            tsv_writer32.writerow([cons, count])
        # Writing the consonant seq-suffix counts into a tsv file
        for (
            consonant,
            suffix,
        ), count in final_consonant_suffix.most_common():
            tsv_writer33.writerow([consonant, suffix, count])
        # Conditional Probability: p(passive|vowel_sequence)
        for (consonant, suffix), count in final_consonant_suffix.items():
            p = round(count / final_consonant[consonant], 4)
            # Outputting consonant sequence, suffix, consonant seq-suffix
            # counts, the probabilities, and cons seq-suffix counts out of 886
            tsv_writer34.writerow(
                [
                    consonant,
                    suffix,
                    p,
                    final_consonant_suffix[(consonant, suffix)],
                    final_consonant[consonant],
                ]
            )

    # PART 5 – Vowel features and passives
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
            tsv_writer14.writerow([v_feature, suffix, count])
        # Conditional Probability: p(passive|vowel_features)
        for (v_feature, suffix), count in vowel_features_suffix.items():
            p = round(count / vowel_features[v_feature], 4)
            # Outputting vowel features, suffix, vowel feat-suffix counts,
            # the probabilities, and vowel feat counts out of 886
            tsv_writer15.writerow(
                [
                    v_feature,
                    suffix,
                    p,
                    vowel_features_suffix[(v_feature, suffix)],
                    vowel_features[v_feature],
                ]
            )

    # PART 6 & 7 – Consonant features (6), final consonant features (7)
    # and suffixes
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

        # PART 7 – Final consonant features
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

            # PART 7
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

            # PART 6 – Consonant Features Sequence
            # Handling the consonant feature sequence counter
            if consonant_feature_sequence:
                cons_features[tuple(consonant_feature_sequence)] += 1
                cons_features_suffix[
                    (tuple(consonant_feature_sequence), suffix)
                ] += 1
        # Writing the consonant features into a tsv file
        for c_feature, count in cons_features.most_common():
            tsv_writer16.writerow([c_feature, count])
            # print(f"{c_feature}:\t{count}")
        # Writing the consonant feature seq-suffix counts into a tsv file
        for (
            c_feature,
            suffix,
        ), count in cons_features_suffix.most_common():
            tsv_writer17.writerow([c_feature, suffix, count])
        # Conditional Probability: p(passive|consonant_features)
        for (c_feature, suffix), count in cons_features_suffix.items():
            p = round(count / cons_features[c_feature], 4)
            # Outputting cons features, suffix, cons feature-suffix
            # counts, the probabilities, cons feat counts out of 886
            tsv_writer18.writerow(
                [
                    c_feature,
                    suffix,
                    p,
                    cons_features_suffix[(c_feature, suffix)],
                    cons_features[c_feature],
                ]
            )
            # print(f"{consonant_feature}\t{suffix}:\t{count}\t{p}")

        # PART 7 – Final Consonant Features
        # Writing the final consonant features into a tsv file
        for feature, count in final_cons_features.most_common():
            tsv_writer19.writerow([feature, count])
        # Writing the final consonant features-suffix pair counts
        # into a tsv file
        for (
            feature,
            suffix,
        ), count in final_cons_features_suffix.most_common():
            tsv_writer20.writerow([feature, suffix, count])
        # Conditional Probability: p(passive|final_cons_features)
        for (feature, suffix), count in final_cons_features_suffix.items():
            p = round(count / final_cons_features[feature], 4)
            tsv_writer21.writerow(
                [
                    feature,
                    suffix,
                    p,
                    final_cons_features_suffix[(feature, suffix)],
                    final_cons_features[feature],
                ]
            )

    # PART 8 – Syllable counts and passives
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


        # # The following counts the suffixes
        # suffix_counts = {}
        # Counting the diphthong and monophthongs
        for lemma, suffix in tsv_reader:
            diphthong_count = 0
            vowel_count = 0

        #     # Counting the suffixes
        #     suffix_counts[suffix] = suffix_counts.get(suffix, 0) + 1

        # for suffix, count in suffix_counts.items():
        #     print(f"{suffix}: {count}")
        
            # Skipping reduplications
            if lemma in reduplications:
                continue
            # Diphthong counts
            for diphthong in diphthongs:
                diphthong_count += lemma.count(diphthong)
            # Monophthong counts
            for vowel in vowels:
                vowel_count += lemma.count(vowel)
            # Syllable count per lemma
            lemma_syllable_count = (
                diphthong_count + vowel_count - (2 * diphthong_count)
            )
            # print(lemma, lemma_syllable_count, diphthong_count)

            # Indicating syllable counts by sigma
            syllable_sequence = "σ" * lemma_syllable_count

            if syllable_sequence:
                syllable_count[syllable_sequence] += 1
                syllable_suffix_count[syllable_sequence, suffix] += 1
            # print(lemma, syllable_sequence,
            # syllable_count[syllable_sequence])

        # Writing the syllable counts into a tsv file
        for syllable, count in syllable_count.most_common():
            tsv_writer23.writerow([syllable, count])
        # Writing the syllable-suffix pair counts into a tsv file
        for (syllable, suffix), count in syllable_suffix_count.most_common():
            tsv_writer24.writerow([syllable, suffix, count])
        # Conditional probability: p(suffix|syllable_count)
        for (syllable, suffix), count in syllable_suffix_count.items():
            p = round(count / syllable_count[syllable], 4)
            # Outputting syllable representation, suffix, syllable-suffix
            # counts, the probabilities, and syllable counts out of 886 -
            # reduplications
            tsv_writer25.writerow(
                [
                    syllable,
                    suffix,
                    p,
                    syllable_suffix_count[(syllable, suffix)],
                    syllable_count[syllable],
                ]
            )
            # print(syllable, suffix, p,
            # syllable_suffix_count[(syllable, suffix)],
            # syllable_count[syllable])

    # PART 9 – Oral vs nasal consonant features
    # and suffixes
    with open(args.input, "r") as source, open(
        args.output26, "w"
    ) as sink26, open(args.output27, "w") as sink27, open(
        args.output28, "w"
    ) as sink28:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Consonant features: output16
        tsv_writer26 = csv.writer(sink26, delimiter="\t")
        # Consonant features-passive: output17
        tsv_writer27 = csv.writer(sink27, delimiter="\t")
        # Consonant features-passive conditional probabilities: output18
        tsv_writer28 = csv.writer(sink28, delimiter="\t")

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
                        nasality_dict["ng"]
                    )
                    i += 2
                    continue
                # Checking for <wh> digraph
                if char == "w" and i + 1 < len(lemma) and lemma[i + 1] == "h":
                    consonant_feature_sequence.append(
                        nasality_dict["wh"]
                    )
                    i += 2
                    continue
                # Checking for other consonantal segments
                if char in nasality_dict:
                    consonant_feature_sequence.append(
                        nasality_dict[char]
                    )
                i += 1

            # Handling the consonant feature sequence counter
            if consonant_feature_sequence:
                nasality[tuple(consonant_feature_sequence)] += 1
                nasality_suffix[
                    (tuple(consonant_feature_sequence), suffix)
                ] += 1
        # Writing the consonant features into a tsv file
        for c_feature, count in nasality.most_common():
            tsv_writer26.writerow([c_feature, count])
            # print(f"{c_feature}:\t{count}")
        # Writing the consonant feature seq-suffix counts into a tsv file
        for (
            c_feature,
            suffix,
        ), count in nasality_suffix.most_common():
            tsv_writer27.writerow([c_feature, suffix, count])
        # Conditional Probability: p(passive|consonant_features)
        for (
            c_feature,
            suffix,
        ), count in nasality_suffix.items():
            p = round(count / nasality[c_feature], 4)
            # Outputting cons features, suffix, cons feature-suffix
            # counts, the probabilities, cons feat counts out of 886
            tsv_writer28.writerow(
                [
                    c_feature,
                    suffix,
                    p,
                    nasality_suffix[(c_feature, suffix)],
                    nasality[c_feature],
                ]
            )

    # PART 10 – Place of articulation of consonant sequences
    with open(args.input, "r") as source, open(
        args.output29, "w"
    ) as sink29, open(args.output30, "w") as sink30, open(
        args.output31, "w"
    ) as sink31:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Consonant features: output16
        tsv_writer29 = csv.writer(sink29, delimiter="\t")
        # Consonant features-passive: output17
        tsv_writer30 = csv.writer(sink30, delimiter="\t")
        # Consonant features-passive conditional probabilities: output18
        tsv_writer31 = csv.writer(sink31, delimiter="\t")

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
                        place_dict["ng"]
                    )
                    i += 2
                    continue
                # Checking for <wh> digraph
                if char == "w" and i + 1 < len(lemma) and lemma[i + 1] == "h":
                    consonant_feature_sequence.append(
                        place_dict["wh"]
                    )
                    i += 2
                    continue
                # Checking for other consonantal segments
                if char in place_dict:
                    consonant_feature_sequence.append(
                        place_dict[char]
                    )
                i += 1

            # Handling the consonant feature sequence counter
            if consonant_feature_sequence:
                place[tuple(consonant_feature_sequence)] += 1
                place_suffix[
                    (tuple(consonant_feature_sequence), suffix)
                ] += 1
        # Writing the consonant features into a tsv file
        for c_feature, count in place.most_common():
            tsv_writer29.writerow([c_feature, count])
            # print(f"{c_feature}:\t{count}")
        # Writing the consonant feature seq-suffix counts into a tsv file
        for (
            c_feature,
            suffix,
        ), count in place_suffix.most_common():
            tsv_writer30.writerow([c_feature, suffix, count])
        # Conditional Probability: p(passive|consonant_features)
        for (c_feature, suffix), count in place_suffix.items():
            p = round(count / place[c_feature], 4)
            # Outputting cons features, suffix, cons feature-suffix
            # counts, the probabilities, cons feat counts out of 886
            tsv_writer31.writerow(
                [
                    c_feature,
                    suffix,
                    p,
                    place_suffix[(c_feature, suffix)],
                    place[c_feature],
                ]
            )

    # JULY 29 MODIFICATION
    # PART 11 – Sequential [+/-consonantal]
    with open(args.input, "r") as source, open(
        args.output35, "w"
    ) as sink35, open(args.output36, "w") as sink36, open(
        args.output37, "w"
    ) as sink37:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Consonant features: output16
        tsv_writer35 = csv.writer(sink35, delimiter="\t")
        # Consonant features-passive: output17
        tsv_writer36 = csv.writer(sink36, delimiter="\t")
        # Consonant features-passive conditional probabilities: output18
        tsv_writer37 = csv.writer(sink37, delimiter="\t")

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
                        consonantal_dict["ng"]
                    )
                    i += 2
                    continue
                # Checking for <wh> digraph
                if char == "w" and i + 1 < len(lemma) and lemma[i + 1] == "h":
                    consonant_feature_sequence.append(
                        consonantal_dict["wh"]
                    )
                    i += 2
                    continue
                # Checking for other consonantal segments
                if char in consonantal_dict:
                    consonant_feature_sequence.append(
                        consonantal_dict[char]
                    )
                i += 1

            # Handling the consonant feature sequence counter
            if consonant_feature_sequence:
                consonantal[tuple(consonant_feature_sequence)] += 1
                consonantal_suffix[
                    (tuple(consonant_feature_sequence), suffix)
                ] += 1
        # Writing the consonant features into a tsv file
        for c_feature, count in consonantal.most_common():
            tsv_writer35.writerow([c_feature, count])
            # print(f"{c_feature}:\t{count}")
        # Writing the consonant feature seq-suffix counts into a tsv file
        for (
            c_feature,
            suffix,
        ), count in consonantal_suffix.most_common():
            tsv_writer36.writerow([c_feature, suffix, count])
        # Conditional Probability: p(passive|consonant_features)
        for (c_feature, suffix), count in consonantal_suffix.items():
            p = round(count / consonantal[c_feature], 4)
            # Outputting cons features, suffix, cons feature-suffix
            # counts, the probabilities, cons feat counts out of 886
            tsv_writer37.writerow(
                [
                    c_feature,
                    suffix,
                    p,
                    consonantal_suffix[(c_feature, suffix)],
                    consonantal[c_feature],
                ]
            )

    # PART 12 – Sequential [+/-sonorant]
    with open(args.input, "r") as source, open(
        args.output38, "w"
    ) as sink38, open(args.output39, "w") as sink39, open(
        args.output40, "w"
    ) as sink40:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Consonant features: output16
        tsv_writer38 = csv.writer(sink38, delimiter="\t")
        # Consonant features-passive: output17
        tsv_writer39 = csv.writer(sink39, delimiter="\t")
        # Consonant features-passive conditional probabilities: output18
        tsv_writer40 = csv.writer(sink40, delimiter="\t")

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
                        sonorant_dict["ng"]
                    )
                    i += 2
                    continue
                # Checking for <wh> digraph
                if char == "w" and i + 1 < len(lemma) and lemma[i + 1] == "h":
                    consonant_feature_sequence.append(
                        sonorant_dict["wh"]
                    )
                    i += 2
                    continue
                # Checking for other consonantal segments
                if char in sonorant_dict:
                    consonant_feature_sequence.append(
                        sonorant_dict[char]
                    )
                i += 1

            # Handling the consonant feature sequence counter
            if consonant_feature_sequence:
                sonorant[tuple(consonant_feature_sequence)] += 1
                sonorant_suffix[
                    (tuple(consonant_feature_sequence), suffix)
                ] += 1
        # Writing the consonant features into a tsv file
        for c_feature, count in sonorant.most_common():
            tsv_writer38.writerow([c_feature, count])
            # print(f"{c_feature}:\t{count}")
        # Writing the consonant feature seq-suffix counts into a tsv file
        for (
            c_feature,
            suffix,
        ), count in sonorant_suffix.most_common():
            tsv_writer39.writerow([c_feature, suffix, count])
        # Conditional Probability: p(passive|consonant_features)
        for (c_feature, suffix), count in sonorant_suffix.items():
            p = round(count / sonorant[c_feature], 4)
            # Outputting cons features, suffix, cons feature-suffix
            # counts, the probabilities, cons feat counts out of 886
            tsv_writer40.writerow(
                [
                    c_feature,
                    suffix,
                    p,
                    sonorant_suffix[(c_feature, suffix)],
                    sonorant[c_feature],
                ]
            )

    # PART 13 – Sequential [+/-continuant]
    with open(args.input, "r") as source, open(
        args.output41, "w"
    ) as sink41, open(args.output42, "w") as sink42, open(
        args.output43, "w"
    ) as sink43:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Consonant features: output16
        tsv_writer41 = csv.writer(sink41, delimiter="\t")
        # Consonant features-passive: output17
        tsv_writer42 = csv.writer(sink42, delimiter="\t")
        # Consonant features-passive conditional probabilities: output18
        tsv_writer43 = csv.writer(sink43, delimiter="\t")

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
                        continuant_dict["ng"]
                    )
                    i += 2
                    continue
                # Checking for <wh> digraph
                if char == "w" and i + 1 < len(lemma) and lemma[i + 1] == "h":
                    consonant_feature_sequence.append(
                        continuant_dict["wh"]
                    )
                    i += 2
                    continue
                # Checking for other consonantal segments
                if char in continuant_dict:
                    consonant_feature_sequence.append(
                        continuant_dict[char]
                    )
                i += 1

            # Handling the consonant feature sequence counter
            if consonant_feature_sequence:
                continuant[tuple(consonant_feature_sequence)] += 1
                continuant_suffix[
                    (tuple(consonant_feature_sequence), suffix)
                ] += 1
        # Writing the consonant features into a tsv file
        for c_feature, count in continuant.most_common():
            tsv_writer41.writerow([c_feature, count])
            # print(f"{c_feature}:\t{count}")
        # Writing the consonant feature seq-suffix counts into a tsv file
        for (
            c_feature,
            suffix,
        ), count in continuant_suffix.most_common():
            tsv_writer42.writerow([c_feature, suffix, count])
        # Conditional Probability: p(passive|consonant_features)
        for (c_feature, suffix), count in continuant_suffix.items():
            p = round(count / continuant[c_feature], 4)
            # Outputting cons features, suffix, cons feature-suffix
            # counts, the probabilities, cons feat counts out of 886
            tsv_writer43.writerow(
                [
                    c_feature,
                    suffix,
                    p,
                    continuant_suffix[(c_feature, suffix)],
                    continuant[c_feature],
                ]
            )

    # PART 14 – Sequential [+/-voiced]
    with open(args.input, "r") as source, open(
        args.output44, "w"
    ) as sink44, open(args.output45, "w") as sink45, open(
        args.output46, "w"
    ) as sink46:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Consonant features: output16
        tsv_writer44 = csv.writer(sink44, delimiter="\t")
        # Consonant features-passive: output17
        tsv_writer45 = csv.writer(sink45, delimiter="\t")
        # Consonant features-passive conditional probabilities: output18
        tsv_writer46 = csv.writer(sink46, delimiter="\t")

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
                        voicing_dict["ng"]
                    )
                    i += 2
                    continue
                # Checking for <wh> digraph
                if char == "w" and i + 1 < len(lemma) and lemma[i + 1] == "h":
                    consonant_feature_sequence.append(
                        voicing_dict["wh"]
                    )
                    i += 2
                    continue
                # Checking for other consonantal segments
                if char in voicing_dict:
                    consonant_feature_sequence.append(
                        voicing_dict[char]
                    )
                i += 1

            # Handling the consonant feature sequence counter
            if consonant_feature_sequence:
                voicing[tuple(consonant_feature_sequence)] += 1
                voicing_suffix[
                    (tuple(consonant_feature_sequence), suffix)
                ] += 1
        # Writing the consonant features into a tsv file
        for c_feature, count in voicing.most_common():
            tsv_writer44.writerow([c_feature, count])
            # print(f"{c_feature}:\t{count}")
        # Writing the consonant feature seq-suffix counts into a tsv file
        for (
            c_feature,
            suffix,
        ), count in voicing_suffix.most_common():
            tsv_writer45.writerow([c_feature, suffix, count])
        # Conditional Probability: p(passive|consonant_features)
        for (c_feature, suffix), count in voicing_suffix.items():
            p = round(count / voicing[c_feature], 4)
            # Outputting cons features, suffix, cons feature-suffix
            # counts, the probabilities, cons feat counts out of 886
            tsv_writer46.writerow(
                [
                    c_feature,
                    suffix,
                    p,
                    voicing_suffix[(c_feature, suffix)],
                    voicing[c_feature],
                ]
            )

    # PART 15 – Sequential [spread glottis]
    with open(args.input, "r") as source, open(
        args.output47, "w"
    ) as sink47, open(args.output48, "w") as sink48, open(
        args.output49, "w"
    ) as sink49:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Consonant features: output16
        tsv_writer47 = csv.writer(sink47, delimiter="\t")
        # Consonant features-passive: output17
        tsv_writer48 = csv.writer(sink48, delimiter="\t")
        # Consonant features-passive conditional probabilities: output18
        tsv_writer49 = csv.writer(sink49, delimiter="\t")

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
                        spread_g_dict["ng"]
                    )
                    i += 2
                    continue
                # Checking for <wh> digraph
                if char == "w" and i + 1 < len(lemma) and lemma[i + 1] == "h":
                    consonant_feature_sequence.append(
                        spread_g_dict["wh"]
                    )
                    i += 2
                    continue
                # Checking for other consonantal segments
                if char in spread_g_dict:
                    consonant_feature_sequence.append(
                        spread_g_dict[char]
                    )
                i += 1

            # Handling the consonant feature sequence counter
            if consonant_feature_sequence:
                spread_g[tuple(consonant_feature_sequence)] += 1
                spread_g_suffix[
                    (tuple(consonant_feature_sequence), suffix)
                ] += 1
        # Writing the consonant features into a tsv file
        for c_feature, count in spread_g.most_common():
            tsv_writer47.writerow([c_feature, count])
            # print(f"{c_feature}:\t{count}")
        # Writing the consonant feature seq-suffix counts into a tsv file
        for (
            c_feature,
            suffix,
        ), count in spread_g_suffix.most_common():
            tsv_writer48.writerow([c_feature, suffix, count])
        # Conditional Probability: p(passive|consonant_features)
        for (c_feature, suffix), count in spread_g_suffix.items():
            p = round(count / spread_g[c_feature], 4)
            # Outputting cons features, suffix, cons feature-suffix
            # counts, the probabilities, cons feat counts out of 886
            tsv_writer49.writerow(
                [
                    c_feature,
                    suffix,
                    p,
                    spread_g_suffix[(c_feature, suffix)],
                    spread_g[c_feature],
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
        default="00_final-V_counts.tsv",
        help="outputs stem-final vowel counts",
    )
    parser.add_argument(
        "-o2",
        "--output2",
        default="00_final-V-suffix_counts.tsv",
        help="outputs the final vowel-suffix counts",
    )
    parser.add_argument(
        "-o3",
        "--output3",
        default="00_final-V-suffix_prob.tsv",
        help="outputs p(passive|final_vowel)",
    )
    parser.add_argument(
        "-o4",
        "--output4",
        default="01_final-V-feat_counts.tsv",
        help="outputs stem-final vowel feature counts",
    )
    parser.add_argument(
        "-o5",
        "--output5",
        default="01_final-V-feat-suffix_counts.tsv",
        help="outputs the final vowel feature-suffix counts",
    )
    parser.add_argument(
        "-o6",
        "--output6",
        default="01_final-V-feat-suffix_prob.tsv",
        help="outputs p(passive|final_vowel_feature)",
    )
    parser.add_argument(
        "-o7",
        "--output7",
        default="02_V-seq_counts.tsv",
        help="outputs vowel sequence counts",
    )
    parser.add_argument(
        "-o8",
        "--output8",
        default="02_V-seq-suffix_counts.tsv",
        help="outputs vowel sequence-passive counts",
    )
    parser.add_argument(
        "-o9",
        "--output9",
        default="02_V-seq-suffix_prob.tsv",
        help="outputs p(passive|vowel_sequence)",
    )
    parser.add_argument(
        "-o10",
        "--output10",
        default="03_C-seq_counts.tsv",
        help="outputs consonant sequence counts",
    )
    parser.add_argument(
        "-o11",
        "--output11",
        default="03_C-seq-suffix_counts.tsv",
        help="outputs consonant sequence-passive counts",
    )
    parser.add_argument(
        "-o12",
        "--output12",
        default="03_C-seq-suffix_prob.tsv",
        help="outputs p(passive|consonant_sequence)",
    )
    parser.add_argument(
        "-o32",
        "--output32",
        default="04_final-C_counts.tsv",
        help="outputs final consonant counts",
    )
    parser.add_argument(
        "-o33",
        "--output33",
        default="04_final-C-suffix_counts.tsv",
        help="outputs final consonant-passive counts",
    )
    parser.add_argument(
        "-o34",
        "--output34",
        default="04_final-C-suffix_prob.tsv",
        help="outputs p(passive|final_consonant)",
    )
    parser.add_argument(
        "-o13",
        "--output13",
        default="05_V-feat_counts.tsv",
        help="outputs vowel feature counts",
    )
    parser.add_argument(
        "-o14",
        "--output14",
        default="05_V-feat-suffix_counts.tsv",
        help="outputs vowel feature-passive counts",
    )
    parser.add_argument(
        "-o15",
        "--output15",
        default="05_V-feat-suffix_prob.tsv",
        help="outputs p(passive|vowel_feature)",
    )
    parser.add_argument(
        "-o16",
        "--output16",
        default="06_C-feat_counts.tsv",
        help="outputs consonant feature counts",
    )
    parser.add_argument(
        "-o17",
        "--output17",
        default="06_C-feat-suffix_counts.tsv",
        help="outputs consonant feature-passive counts",
    )
    parser.add_argument(
        "-o18",
        "--output18",
        default="06_C-feat-suffix_prob.tsv",
        help="outputs p(passive|consonant_feature)",
    )
    parser.add_argument(
        "-o19",
        "--output19",
        default="07_final-C-feat_counts.tsv",
        help="outputs final consonant feature counts",
    )
    parser.add_argument(
        "-o20",
        "--output20",
        default="07_final-C-feat-suffix_counts.tsv",
        help="outputs the final vowel feature-suffix counts",
    )
    parser.add_argument(
        "-o21",
        "--output21",
        default="07_final-C-feat-suffix_prob.tsv",
        help="outputs p(passive|final_vowel_feature)",
    )
    # # -o22 gives all lemma-cons feature sequences for testing
    # # purposes
    # parser.add_argument(
    #     "-o22",
    #     "--output22",
    #     default="7_lemma-C-feat-.tsv",
    #     help="outputs p(passive|cons_feature)",
    # )
    parser.add_argument(
        "-o23",
        "--output23",
        default="08_syllable_counts.tsv",
        help="outputs final consonant feature counts",
    )
    parser.add_argument(
        "-o24",
        "--output24",
        default="08_syllable-suffix_counts.tsv",
        help="outputs the final vowel feature-suffix counts",
    )
    parser.add_argument(
        "-o25",
        "--output25",
        default="08_syllable-suffix_prob.tsv",
        help="outputs p(passive|syllable-counts)",
    )
    parser.add_argument(
        "-o26",
        "--output26",
        default="09_C-nasality_counts.tsv",
        help="outputs oral vs nasal consonant feature counts",
    )
    parser.add_argument(
        "-o27",
        "--output27",
        default="09_C-nasality-suffix_counts.tsv",
        help="outputs oral vs nasal consonant feature-passive counts",
    )
    parser.add_argument(
        "-o28",
        "--output28",
        default="09_C-nasality-suffix_prob.tsv",
        help="outputs p(passive|consonant_feature_nasality)",
    )
    parser.add_argument(
        "-o29",
        "--output29",
        default="10_C-place_counts.tsv",
        help="outputs consonant place counts",
    )
    parser.add_argument(
        "-o30",
        "--output30",
        default="10_C-place-suffix_counts.tsv",
        help="outputs consonant place-passive counts",
    )
    parser.add_argument(
        "-o31",
        "--output31",
        default="10_C-place-suffix_prob.tsv",
        help="outputs p(passive|consonant_place)",
    )
    # [+/-consonantal]
    parser.add_argument(
        "-o35",
        "--output35",
        default="11_C-consonantal_counts.tsv",
        help="outputs consonant place counts",
    )
    parser.add_argument(
        "-o36",
        "--output36",
        default="11_C-consonantal-suffix_counts.tsv",
        help="outputs consonant place-passive counts",
    )
    parser.add_argument(
        "-o37",
        "--output37",
        default="11_C-consonantal-suffix_prob.tsv",
        help="outputs p(passive|consonant_place)",
    )
    # [+/-sonorant]
    parser.add_argument(
        "-o38",
        "--output38",
        default="12_C-sonorant_counts.tsv",
        help="outputs consonant place counts",
    )
    parser.add_argument(
        "-o39",
        "--output39",
        default="12_C-sonorant-suffix_counts.tsv",
        help="outputs consonant place-passive counts",
    )
    parser.add_argument(
        "-o40",
        "--output40",
        default="12_C-sonorant-suffix_prob.tsv",
        help="outputs p(passive|consonant_place)",
    )
    # [+/-continuant]
    parser.add_argument(
        "-o41",
        "--output41",
        default="13_C-continuant_counts.tsv",
        help="outputs consonant place counts",
    )
    parser.add_argument(
        "-o42",
        "--output42",
        default="13_C-continuant-suffix_counts.tsv",
        help="outputs consonant place-passive counts",
    )
    parser.add_argument(
        "-o43",
        "--output43",
        default="13_C-continuant-suffix_prob.tsv",
        help="outputs p(passive|consonant_place)",
    )
    # [+/-voiced]
    parser.add_argument(
        "-o44",
        "--output44",
        default="14_C-voicing_counts.tsv",
        help="outputs consonant place counts",
    )
    parser.add_argument(
        "-o45",
        "--output45",
        default="14_C-voicing-suffix_counts.tsv",
        help="outputs consonant place-passive counts",
    )
    parser.add_argument(
        "-o46",
        "--output46",
        default="14_C-voicing-suffix_prob.tsv",
        help="outputs p(passive|consonant_place)",
    )
    # [spread glottis]
    parser.add_argument(
        "-o47",
        "--output47",
        default="15_C-spread-g_counts.tsv",
        help="outputs consonant place counts",
    )
    parser.add_argument(
        "-o48",
        "--output48",
        default="15_C-spread-g-suffix_counts.tsv",
        help="outputs consonant place-passive counts",
    )
    parser.add_argument(
        "-o49",
        "--output49",
        default="15_C-spread-g-suffix_prob.tsv",
        help="outputs p(passive|consonant_place)",
    )
    main(parser.parse_args())
