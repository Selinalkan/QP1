#!/usr/bin/env python

"""
This program only focuses on /-hia, -mia, -ria/ probabilities.

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
It calculates the stem-final vowel-suffix probabilities
for /-hia, -mia, -ria/.
It collects the features of stem-final vowels and counts their occurrences.
It counts the occurrences of vowel feature-suffix combinations.
It calculates the vowel feature-suffix probabilities for
/-hia, -mia, -ria/.

PART 2 - Vowel sequences and passives:
It counts the occurrences of vowel sequences.
It counts the occurrences of vowel sequences-suffix combinations.
It calculates the vowel sequence-suffix probabilities
for /-hia, -mia, -ria/.

PART 3 - Consonant sequences and passives:
It counts the occurrences of consonant sequences.
It counts the occurrences of consonant sequence-suffix combinations.
It calculates the consonant sequence-suffix probabilities
for /-hia, -mia, -ria/.

PART 4 - Vowel features and passives:
It counts the occurrences of vowel features.
It counts the occurrences of vowel feature-suffix combinations.
It calculates the vowel feature-suffix probabilities
for /-hia, -mia, -ria/.

PART 5 - Consonant features and passives:
It counts the occurrences of consonant features.
It counts the occurrences of consonant feature-suffix combinations.
It calculates the consonant feature-suffix probabilities
for /-hia, -mia, -ria/.

PART 6 - Final consonant features and passives:
It counts the occurrences of final consonant features.
It counts the occurrences of final consonant feature-suffix combinations.
It calculates the final consonant feature-suffix probabilities
for /-hia, -mia, -ria/.

PART 7 - Syllable counts and passives:
It counts the occurrences of syllables.
It counts the occurrences of syllable-suffix combinations.
It calculates the syllable count-suffix probabilities
for /-hia, -mia, -ria/.

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
    "a": "[low, back, -round, short]",
    "ā": "[low, back, -round, long]",
    "e": "[mid, front, -round, short]",
    "ē": "[mid, front, -round, long]",
    "i": "[high, front, -round, short]",
    "ī": "[high, front, -round, long]",
    "o": "[mid, back, +round, short]",
    "ō": "[mid, back, +round, long]",
    "u": "[high, central, +round, short]",
    "ū": "[high, central, +round, long]",
}

consonant_features_dict = {
    "h": "[-cons, -son, -nas, dors, +cont, +SG, -voi]",
    "k": "[+cons, -son, -nas, dors, -cont, -SG, -voi]",
    "m": "[+cons, +son, +nas, lab, -cont, -SG, +voi]",
    "n": "[+cons, +son, +nas, cor, -cont, -SG, +voi]",
    "ng": "[+cons, +son, +nas, dors, -cont, -SG, +voi]",
    "p": "[+cons, -son, -nas, lab, -cont, -SG, -voi]",
    "r": "[+cons, +son, -nas, cor, +cont, -SG, +voi]",
    "t": "[+cons, -son, -nas, cor, -cont, -SG, -voi]",
    "w": "[-cons, +son, -nas, lab, +cont, -SG, +voi]",
    "wh": "[+cons, -son, -nas, lab, +cont, -SG, -voi]",
}

# PART9: [+/-nasal]
# Used to check oral vs nasal feature in consonant sequences
nasality_dict = {
    "h": "-nas",
    "k": "-nas",
    "m": "+nas",
    "n": "+nas",
    "ng": "+nas",
    "p": "-nas",
    "r": "-nas",
    "t": "-nas",
    "w": "-nas",
    "wh": "-nas",
}

# PART10: place of articulation
# Used to check the place of articulation in consonant sequences
place_dict = {
    # Harlow 2007:63 – Kearns (1990) [h] --> [+high]
    # Blevins: all [+high] are [dorsal] by definition.
    "h": "dors",
    "k": "dors",
    "m": "lab",
    "n": "cor",
    "ng": "dors",
    "p": "lab",
    "r": "cor",
    "t": "cor",
    "w": "lab",
    "wh": "lab",
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
    # Stem-final vowels and suffixes counter
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
    nasality_suffix: Counter[Tuple[Any, ...]] = collections.Counter()

    # PART 10 – [labial], [coronal], [dorsal]
    # PoA of consonant sequences counter
    place: Counter[Tuple[str, ...]] = collections.Counter()
    # # PoA of consonant sequences-passive counter
    place_suffix: Counter[Tuple[Any, ...]] = collections.Counter()

    # PART 11 – Sequential [+/-consonantal]
    # phoneme feature counter
    consonantal: Counter[Tuple[str, ...]] = collections.Counter()
    # phoneme feature-suffix counter
    consonantal_suffix: Counter[Tuple[Any, ...]] = collections.Counter()

    # PART 12 – Sequential [+/-sonorant]
    # phoneme feature counter
    sonorant: Counter[Tuple[str, ...]] = collections.Counter()
    # phoneme feature-suffix counter
    sonorant_suffix: Counter[Tuple[Any, ...]] = collections.Counter()

    # PART 13 – Sequential [+/-continuant]
    # phoneme feature counter
    continuant: Counter[Tuple[str, ...]] = collections.Counter()
    # phoneme feature-suffix counter
    continuant_suffix: Counter[Tuple[Any, ...]] = collections.Counter()

    # PART 14 – Sequential [+/-voiced]
    # phoneme feature counter
    voicing: Counter[Tuple[str, ...]] = collections.Counter()
    # phoneme feature-suffix counter
    voicing_suffix: Counter[Tuple[Any, ...]] = collections.Counter()

    # PART 15 – Sequential [spread glottis]
    # phoneme feature counter
    spread_g: Counter[Tuple[str, ...]] = collections.Counter()
    # phoneme feature-suffix counter
    spread_g_suffix: Counter[Tuple[Any, ...]] = collections.Counter()

    ########################################################################
    # PART 0 & 1 – Stem-final vowels (0), stem-final vowel features (1)
    # and passives
    with open(args.input, "r") as source, open(
        args.output3, "w"
    ) as sink3, open(args.output6, "w") as sink6:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # PART 0
        tsv_writer3 = csv.writer(sink3, delimiter="\t")
        # PART 1 - Stem-final vowel features
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
        # # Writing the final vowel counts into a tsv file
        for (vowel, suffix), count in final_vowel_suffix.items():
            # ONLY /-HIA, -MIA, -RIA/
            if suffix in ["hia", "mia", "ria"]:
                p = round(count / final_vowel[vowel], 4)
                # Outputting vowel, suffix, total final vowel count per suffix,
                # the probabilities, and total final vowel count out of 886
                tsv_writer3.writerow(
                    [
                        suffix,
                        vowel,
                        p,
                        final_vowel_suffix[(vowel, suffix)],
                        final_vowel[vowel],
                    ]
                )

        # PART 1 - Stem-final vowel features
        # Conditional Probability: p(passive|final_vowel_features)
        for (feature, suffix), count in final_vowel_features_suffix.items():
            # ONLY /-HIA, -MIA, -RIA/
            if suffix in ["hia", "mia", "ria"]:
                p = round(count / final_vowel_features[feature], 4)
                # Outputting vowel features, suffix, total vowel
                # feature sequence-suffix counts, the probabilities,
                # and total vowel feature counts out of 886
                tsv_writer6.writerow(
                    [
                        suffix,                        
                        feature,
                        p,
                        final_vowel_features_suffix[(feature, suffix)],
                        final_vowel_features[feature],
                    ]
                )

    # PART 2 – Vowel sequences and passives
    with open(args.input, "r") as source, open(args.output9, "w") as sink9:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # # Vowel sequence: output7
        # tsv_writer7 = csv.writer(sink7, delimiter="\t")
        # # Vowel seq-passive: output8
        # tsv_writer8 = csv.writer(sink8, delimiter="\t")
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

        # # Writing the vowel sequences into a tsv file
        # for seq, count in vowel_seq.most_common():
        #     tsv_writer7.writerow([seq, count])
        # # Writing the vowel seq-suffix counts into a tsv file
        # for (
        #     sequence,
        #     suffix,
        # ), count in vowel_seq_suffix.most_common():
        #     # if suffix in ["hia", "mia", "ria"]:
        #     tsv_writer8.writerow([sequence, suffix, count])
        # Conditional Probability: p(passive|vowel_sequence)
        for (sequence, suffix), count in vowel_seq_suffix.items():
            # ONLY /-HIA, -MIA, -RIA/
            if suffix in ["hia", "mia", "ria"]:
                p = round(count / vowel_seq[sequence], 4)
                # Outputting vowel sequence, suffix, vowel seq-suffix counts,
                # the probabilities, and total vowel seq counts out of 886
                tsv_writer9.writerow(
                    [
                        suffix,                        
                        sequence,
                        p,
                        vowel_seq_suffix[(sequence, suffix)],
                        vowel_seq[sequence],
                    ]
                )

    # PART 3 & 4 – Consonant sequences (3) and final consonants (4)
    with open(args.input, "r") as source, open(
        args.output12, "w"
    ) as sink12, open(args.output34, "w") as sink34:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # # Consonant sequence: output10
        # tsv_writer10 = csv.writer(sink10, delimiter="\t")
        # # Consonant seq-passive: output11
        # tsv_writer11 = csv.writer(sink11, delimiter="\t")
        # Consonant seq-passive conditional probabilities: output12
        tsv_writer12 = csv.writer(sink12, delimiter="\t")
        # PART 4 - Final consonants
        # Output files
        # # Final consonant counts: output32
        # tsv_writer32 = csv.writer(sink32, delimiter="\t")
        # # Final consonant-suffix combination counts: output33
        # tsv_writer33 = csv.writer(sink33, delimiter="\t")
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
                if current_sequence[-2:] == "ng" or current_sequence[-2:] == "wh":
                    final_cons = current_sequence[-2:]
                else:
                    final_cons = current_sequence[-1:]
                final_consonant[final_cons] += 1
                final_consonant_suffix[(final_cons, suffix)] += 1

        # # Writing the consonant sequences into a tsv file
        # for seq, count in cons_seq.most_common():
        #     tsv_writer10.writerow([seq, count])
        # # Writing the consonant seq-suffix counts into a tsv file
        # for (
        #     sequence,
        #     suffix,
        # ), count in cons_seq_suffix.most_common():
        #     # if suffix in ["hia", "mia", "ria"]:
        #     tsv_writer11.writerow([sequence, suffix, count])
        # Conditional Probability: p(passive|vowel_sequence)
        for (sequence, suffix), count in cons_seq_suffix.items():
            # ONLY /-HIA, -MIA, -RIA/
            if suffix in ["hia", "mia", "ria"]:
                p = round(count / cons_seq[sequence], 4)
                # Outputting consonant sequence, suffix, consonant seq-suffix
                # counts, the probabilities, and cons seq-suffix counts
                # out of 886
                tsv_writer12.writerow(
                    [
                        suffix,                        
                        sequence,
                        p,
                        cons_seq_suffix[(sequence, suffix)],
                        cons_seq[sequence],
                    ]
                )

        # PART 4
        # # Writing the final consonants into a tsv file
        # for cons, count in final_consonant.most_common():
        #     tsv_writer32.writerow([cons, count])
        # # Writing the consonant seq-suffix counts into a tsv file
        # for (
        #     consonant,
        #     suffix,
        # ), count in final_consonant_suffix.most_common():
        #     tsv_writer33.writerow([consonant, suffix, count])
        # Conditional Probability: p(passive|vowel_sequence)
        for (consonant, suffix), count in final_consonant_suffix.items():
            # ONLY /-HIA, -MIA, -RIA/
            if suffix in ["hia", "mia", "ria"]:
                p = round(count / final_consonant[consonant], 4)
                # Outputting consonant sequence, suffix, consonant
                # seq-suffix
                # counts, the probabilities, and cons seq-suffix
                # counts out of 886
                tsv_writer34.writerow(
                    [
                        suffix,                        
                        consonant,
                        p,
                        final_consonant_suffix[(consonant, suffix)],
                        final_consonant[consonant],
                    ]
                )

    # PART 5 – Vowel features and passives
    with open(args.input, "r") as source, open(args.output15, "w") as sink15:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # # Vowel features: output112
        # tsv_writer13 = csv.writer(sink13, delimiter="\t")
        # # Vowel features-passive: output14
        # tsv_writer14 = csv.writer(sink14, delimiter="\t")
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
        # for v_feature, count in vowel_features.most_common():
        #     tsv_writer13.writerow([v_feature, count])
        # # Writing the vowel feature-suffix counts into a tsv file
        # for (
        #     v_feature,
        #     suffix,
        # ), count in vowel_features_suffix.most_common():
        #     # if suffix in ["hia", "mia", "ria"]:
        #     tsv_writer14.writerow([v_feature, suffix, count])
        # Conditional Probability: p(passive|vowel_features)
        for (v_feature, suffix), count in vowel_features_suffix.items():
            # ONLY /-HIA, -MIA, -RIA/
            if suffix in ["hia", "mia", "ria"]:
                p = round(count / vowel_features[v_feature], 4)
                # Outputting vowel features, suffix, vowel feat-suffix counts,
                # the probabilities, and vowel feat counts out of 886
                tsv_writer15.writerow(
                    [
                        suffix,                        
                        v_feature,
                        p,
                        vowel_features_suffix[(v_feature, suffix)],
                        vowel_features[v_feature],
                    ]
                )

    # PART 6 & 7 – Consonant features (6), final consonant features (7)
    # and suffixes
    with open(args.input, "r") as source, open(
        args.output18, "w"
    ) as sink18, open(args.output21, "w") as sink21:
        # open(args.output22, "w") as sink22:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # # Consonant features: output16
        # tsv_writer16 = csv.writer(sink16, delimiter="\t")
        # # Consonant features-passive: output17
        # tsv_writer17 = csv.writer(sink17, delimiter="\t")
        # Consonant features-passive conditional probabilities: output18
        tsv_writer18 = csv.writer(sink18, delimiter="\t")

        # PART 6 – Final consonant features
        # # Final consonant feature counts: output19
        # tsv_writer19 = csv.writer(sink19, delimiter="\t")
        # # Final consonant feature-suffix counts: output20
        # tsv_writer20 = csv.writer(sink20, delimiter="\t")
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

            # PART 5 – Consonant Features Sequence
            # Handling the consonant feature sequence counter
            if consonant_feature_sequence:
                cons_features[tuple(consonant_feature_sequence)] += 1
                cons_features_suffix[
                    (tuple(consonant_feature_sequence), suffix)
                ] += 1
        # # Writing the consonant features into a tsv file
        # for c_feature, count in cons_features.most_common():
        #     tsv_writer16.writerow([c_feature, count])
        #     # print(f"{c_feature}:\t{count}")
        # # Writing the consonant feature seq-suffix counts into a tsv file
        # for (
        #     c_feature,
        #     suffix,
        # ), count in cons_features_suffix.most_common():
        #     # if suffix in ["hia", "mia", "ria"]:
        #     tsv_writer17.writerow([c_feature, suffix, count])
        # Conditional Probability: p(passive|consonant_features)
        for (c_feature, suffix), count in cons_features_suffix.items():
            # ONLY /-HIA, -MIA, -RIA/
            if suffix in ["hia", "mia", "ria"]:
                p = round(count / cons_features[c_feature], 4)
                # Outputting cons features, suffix, cons feature-suffix
                # counts, the probabilities, cons feat counts out of 886
                tsv_writer18.writerow(
                    [
                        suffix,                        
                        c_feature,
                        p,
                        cons_features_suffix[(c_feature, suffix)],
                        cons_features[c_feature],
                    ]
                )
                # print(f"{consonant_feature}\t{suffix}:\t{count}\t{p}")

        # PART 7 – Final Consonant Features
        # # Writing the final consonant features into a tsv file
        # for feature, count in final_cons_features.most_common():
        #     tsv_writer19.writerow([feature, count])
        # # Writing the final consonant features-suffix pair counts
        # # into a tsv file
        # for (
        #     feature,
        #     suffix,
        # ), count in final_cons_features_suffix.most_common():
        #     tsv_writer20.writerow([feature, suffix, count])
        # Conditional Probability: p(passive|final_cons_features)
        for (feature, suffix), count in final_cons_features_suffix.items():
            # ONLY /-HIA, -MIA, -RIA/
            if suffix in ["hia", "mia", "ria"]:
                p = round(count / final_cons_features[feature], 4)
                tsv_writer21.writerow(
                    [
                        suffix,                        
                        feature,
                        p,
                        final_cons_features_suffix[(feature, suffix)],
                        final_cons_features[feature],
                    ]
                )

    # PART 8 – Syllable counts and passives
    with open(args.input, "r") as source, open(args.output25, "w") as sink25:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # # Syllable counts: output23
        # tsv_writer23 = csv.writer(sink23, delimiter="\t")
        # # Syllable-passive counts: output24
        # tsv_writer24 = csv.writer(sink24, delimiter="\t")
        # Syllable count-passive conditional probabilities: output25
        tsv_writer25 = csv.writer(sink25, delimiter="\t")

        # Counting the diphthong and monophthongs
        for lemma, suffix in tsv_reader:
            diphthong_count = 0
            vowel_count = 0
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
            # print(lemma, syllable_sequence)

            if syllable_sequence:
                syllable_count[syllable_sequence] += 1
                syllable_suffix_count[syllable_sequence, suffix] += 1
            # print(lemma, syllable_sequence, syllable_count[syllable_sequence])

        # # Writing the syllable counts into a tsv file
        # for syllable, count in syllable_count.most_common():
        #     tsv_writer23.writerow([syllable, count])
        # # Writing the syllable-suffix pair counts into a tsv file
        # for (syllable, suffix), count in syllable_suffix_count.most_common():
        #     tsv_writer24.writerow([syllable, suffix, count])
        # Conditional probability: p(suffix|syllable_count)
        for (syllable, suffix), count in syllable_suffix_count.items():
            # ONLY /-HIA, -MIA, -RIA/
            if suffix in ["hia", "mia", "ria"]:
                p = round(count / syllable_count[syllable], 4)
                # Outputting syllable representation, suffix, syllable-suffix
                # counts, the probabilities, and syllable counts out of 886 -
                # reduplications
                tsv_writer25.writerow(
                    [
                        suffix,                        
                        syllable,
                        p,
                        syllable_suffix_count[(syllable, suffix)],
                        syllable_count[syllable],
                    ]
                )

    # PART 9 – Oral vs nasal consonant features
    # and suffixes
    with open(args.input, "r") as source, open(args.output28, "w") as sink28:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # # Consonant features: output16
        # tsv_writer26 = csv.writer(sink26, delimiter="\t")
        # # Consonant features-passive: output17
        # tsv_writer27 = csv.writer(sink27, delimiter="\t")
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
        # # Writing the consonant features into a tsv file
        # for c_feature, count in cons_features_nasality.most_common():
        #     tsv_writer26.writerow([c_feature, count])
        #     # print(f"{c_feature}:\t{count}")
        # # Writing the consonant feature seq-suffix counts into a tsv file
        # for (
        #     c_feature,
        #     suffix,
        # ), count in cons_features_nasality_suffix.most_common():
        #     tsv_writer27.writerow([c_feature, suffix, count])
        # Conditional Probability: p(passive|consonant_features)
        for (
            c_feature,
            suffix,
        ), count in nasality_suffix.items():
            # ONLY /-HIA, -MIA, -RIA/
            if suffix in ["hia", "mia", "ria"]:
                p = round(count / nasality[c_feature], 4)
                # Outputting cons features, suffix, cons feature-suffix
                # counts, the probabilities, cons feat counts out of 886
                tsv_writer28.writerow(
                    [
                        suffix,                        
                        c_feature,
                        p,
                        nasality_suffix[(c_feature, suffix)],
                        nasality[c_feature],
                    ]
                )

    # PART 10 – Place of articulation of consonant sequences
    with open(args.input, "r") as source, open(args.output31, "w") as sink31:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # # Consonant features: output16
        # tsv_writer29 = csv.writer(sink29, delimiter="\t")
        # # Consonant features-passive: output17
        # tsv_writer30 = csv.writer(sink30, delimiter="\t")
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
        # # Writing the consonant features into a tsv file
        # for c_feature, count in cons_features_place.most_common():
        #     tsv_writer29.writerow([c_feature, count])
        #     # print(f"{c_feature}:\t{count}")
        # # Writing the consonant feature seq-suffix counts into a tsv file
        # for (
        #     c_feature,
        #     suffix,
        # ), count in cons_features_place_suffix.most_common():
        #     tsv_writer30.writerow([c_feature, suffix, count])
        # Conditional Probability: p(passive|consonant_features)
        for (c_feature, suffix), count in place_suffix.items():
            # ONLY /-HIA, -MIA, -RIA/
            if suffix in ["hia", "mia", "ria"]:
                p = round(count / place[c_feature], 4)
                # Outputting cons features, suffix, cons feature-suffix
                # counts, the probabilities, cons feat counts out of 886
                tsv_writer31.writerow(
                    [
                        suffix,                        
                        c_feature,
                        p,
                        place_suffix[(c_feature, suffix)],
                        place[c_feature],
                    ]
                )

    # JULY 29 MODIFICATION
    # PART 11 – Sequential [+/-consonantal]
    with open(args.input, "r") as source, open(args.output37, "w") as sink37:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
        # Consonant features-passive conditional probabilities: output37
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
                    consonant_feature_sequence.append(consonantal_dict["ng"])
                    i += 2
                    continue
                # Checking for <wh> digraph
                if char == "w" and i + 1 < len(lemma) and lemma[i + 1] == "h":
                    consonant_feature_sequence.append(consonantal_dict["wh"])
                    i += 2
                    continue
                # Checking for other consonantal segments
                if char in consonantal_dict:
                    consonant_feature_sequence.append(consonantal_dict[char])
                i += 1

            # Handling the consonant feature sequence counter
            if consonant_feature_sequence:
                consonantal[tuple(consonant_feature_sequence)] += 1
                consonantal_suffix[
                    (tuple(consonant_feature_sequence), suffix)
                ] += 1
        # Writing the consonant features into a tsv file
        # Conditional Probability: p(passive|consonant_features)
        for (c_feature, suffix), count in consonantal_suffix.items():
            # Only /-mia, -ria, -hia/
            if suffix in ["mia", "ria", "hia"]:
                p = round(count / consonantal[c_feature], 4)
                # Outputting cons features, suffix, cons feature-suffix
                # counts, the probabilities, cons feat counts out of 886
                tsv_writer37.writerow(
                    [
                        suffix,
                        c_feature,
                        p,
                        consonantal_suffix[(c_feature, suffix)],
                        consonantal[c_feature],
                    ]
            )

    # PART 12 – Sequential [+/-sonorant]
    with open(args.input, "r") as source, open(args.output40, "w") as sink40:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
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
                    consonant_feature_sequence.append(sonorant_dict["ng"])
                    i += 2
                    continue
                # Checking for <wh> digraph
                if char == "w" and i + 1 < len(lemma) and lemma[i + 1] == "h":
                    consonant_feature_sequence.append(sonorant_dict["wh"])
                    i += 2
                    continue
                # Checking for other consonantal segments
                if char in sonorant_dict:
                    consonant_feature_sequence.append(sonorant_dict[char])
                i += 1

            # Handling the consonant feature sequence counter
            if consonant_feature_sequence:
                sonorant[tuple(consonant_feature_sequence)] += 1
                sonorant_suffix[
                    (tuple(consonant_feature_sequence), suffix)
                ] += 1
        # Writing the consonant features into a tsv file
        for (c_feature, suffix), count in sonorant_suffix.items():
            # Only [-mia, -ria, -hia]
            if suffix in ["mia", "ria", "hia"]:
                p = round(count / sonorant[c_feature], 4)
                # Outputting cons features, suffix, cons feature-suffix
                # counts, the probabilities, cons feat counts out of 886
                tsv_writer40.writerow(
                    [
                        suffix,
                        c_feature,
                        p,
                        sonorant_suffix[(c_feature, suffix)],
                        sonorant[c_feature],
                    ]
            )

   # PART 13 – Sequential [+/-continuant]
    with open(args.input, "r") as source, open(args.output43, "w") as sink43:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
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
                    consonant_feature_sequence.append(continuant_dict["ng"])
                    i += 2
                    continue
                # Checking for <wh> digraph
                if char == "w" and i + 1 < len(lemma) and lemma[i + 1] == "h":
                    consonant_feature_sequence.append(continuant_dict["wh"])
                    i += 2
                    continue
                # Checking for other consonantal segments
                if char in continuant_dict:
                    consonant_feature_sequence.append(continuant_dict[char])
                i += 1

            # Handling the consonant feature sequence counter
            if consonant_feature_sequence:
                continuant[tuple(consonant_feature_sequence)] += 1
                continuant_suffix[
                    (tuple(consonant_feature_sequence), suffix)
                ] += 1
        # Writing the consonant features into a tsv file
        # Conditional Probability: p(passive|consonant_features)
        for (c_feature, suffix), count in continuant_suffix.items():
            # Only [-mia, -ria, -hia]
            if suffix in ["mia", "ria", "hia"]:
                p = round(count / continuant[c_feature], 4)
                # Outputting cons features, suffix, cons feature-suffix
                # counts, the probabilities, cons feat counts out of 886
                tsv_writer43.writerow(
                    [
                        suffix,
                        c_feature,
                        p,
                        continuant_suffix[(c_feature, suffix)],
                        continuant[c_feature],
                    ]
            )

    # PART 14 – Sequential [+/-voiced]
    with open(args.input, "r") as source, open(args.output46, "w") as sink46:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
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
                    consonant_feature_sequence.append(voicing_dict["ng"])
                    i += 2
                    continue
                # Checking for <wh> digraph
                if char == "w" and i + 1 < len(lemma) and lemma[i + 1] == "h":
                    consonant_feature_sequence.append(voicing_dict["wh"])
                    i += 2
                    continue
                # Checking for other consonantal segments
                if char in voicing_dict:
                    consonant_feature_sequence.append(voicing_dict[char])
                i += 1

            # Handling the consonant feature sequence counter
            if consonant_feature_sequence:
                voicing[tuple(consonant_feature_sequence)] += 1
                voicing_suffix[
                    (tuple(consonant_feature_sequence), suffix)
                ] += 1
        # Writing the consonant features into a tsv file
        # Conditional Probability: p(passive|consonant_features)
        for (c_feature, suffix), count in voicing_suffix.items():
            # Only [-mia, -ria, -hia]
            if suffix in ["mia", "ria", "hia"]:    
                p = round(count / voicing[c_feature], 4)
                # Outputting cons features, suffix, cons feature-suffix
                # counts, the probabilities, cons feat counts out of 886
                tsv_writer46.writerow(
                    [
                        suffix,
                        c_feature,
                        p,
                        voicing_suffix[(c_feature, suffix)],
                        voicing[c_feature],
                    ]
            )

    # PART 15 – Sequential [spread glottis]
    with open(args.input, "r") as source, open(args.output49, "w") as sink49:
        # Input file
        tsv_reader = csv.reader(source, delimiter="\t")
        # Output files
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
                    consonant_feature_sequence.append(spread_g_dict["ng"])
                    i += 2
                    continue
                # Checking for <wh> digraph
                if char == "w" and i + 1 < len(lemma) and lemma[i + 1] == "h":
                    consonant_feature_sequence.append(spread_g_dict["wh"])
                    i += 2
                    continue
                # Checking for other consonantal segments
                if char in spread_g_dict:
                    consonant_feature_sequence.append(spread_g_dict[char])
                i += 1

            # Handling the consonant feature sequence counter
            if consonant_feature_sequence:
                spread_g[tuple(consonant_feature_sequence)] += 1
                spread_g_suffix[
                    (tuple(consonant_feature_sequence), suffix)
                ] += 1
        # Writing the consonant features into a tsv file
        # Conditional Probability: p(passive|consonant_features)
        for (c_feature, suffix), count in spread_g_suffix.items():
            # Only [-mia, -ria, -hia]
            if suffix in ["mia", "ria", "hia"]: 
                p = round(count / spread_g[c_feature], 4)
                # Outputting cons features, suffix, cons feature-suffix
                # counts, the probabilities, cons feat counts out of 886
                tsv_writer49.writerow(
                    [
                        suffix,
                        c_feature,
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
        default="mri-lemma-suffix.tsv",
        help="input Maori TSV file",
    )
    # PART0
    parser.add_argument(
        "-o3",
        "--output3",
        default="00_HMR_final-V-suffix_prob.tsv",
        help="outputs p(passive|final_vowel)",
    )
    # PART1
    parser.add_argument(
        "-o6",
        "--output6",
        default="01_HMR_final-V-feat-suffix_prob.tsv",
        help="outputs p(passive|final_vowel_feature)",
    )
    # PART2
    parser.add_argument(
        "-o9",
        "--output9",
        default="02_HMR_V-seq-suffix_prob.tsv",
        help="outputs p(passive|vowel_sequence)",
    )
    # PART3
    parser.add_argument(
        "-o12",
        "--output12",
        default="03_HMR_C-seq-suffix_prob.tsv",
        help="outputs p(passive|consonant_sequence)",
    )
    # PART4
    parser.add_argument(
        "-o34",
        "--output34",
        default="04_HMR_final-C-suffix_prob.tsv",
        help="outputs p(passive|final_consonant)",
    )
    # PART5
    parser.add_argument(
        "-o15",
        "--output15",
        default="05_HMR_V-feat-suffix_prob.tsv",
        help="outputs p(passive|vowel_feature)",
    )
    # PART6
    parser.add_argument(
        "-o18",
        "--output18",
        default="06_HMR_C-feat-suffix_prob.tsv",
        help="outputs p(passive|consonant_feature)",
    )
    # PART7
    parser.add_argument(
        "-o21",
        "--output21",
        default="07_HMR_final-C-feat-suffix_prob.tsv",
        help="outputs p(passive|final_vowel_feature)",
    )
    # PART8
    parser.add_argument(
        "-o25",
        "--output25",
        default="08_HMR_syllable-suffix_prob.tsv",
        help="outputs p(passive|syllable-counts)",
    )
    # PART9
    parser.add_argument(
        "-o28",
        "--output28",
        default="09_HMR_C-nasality-suffix_prob.tsv",
        help="outputs p(passive|consonant_feature_nasality)",
    )
    # PART10
    parser.add_argument(
        "-o31",
        "--output31",
        default="10_HMR_C-place-suffix_prob.tsv",
        help="outputs p(passive|consonant_place)",
    )
    # PART11 [+/-consonantal]
    parser.add_argument(
        "-o37",
        "--output37",
        default="11_HMR_C-consonantal-suffix_prob.tsv",
        help="outputs p(passive|consonant_place)",
    )
    # PART12 [+/-sonorant]
    parser.add_argument(
        "-o40",
        "--output40",
        default="12_HMR_C-sonorant-suffix_prob.tsv",
        help="outputs p(passive|consonant_place)",
    )
    # PART13 [+/-continuant]
    parser.add_argument(
        "-o43",
        "--output43",
        default="13_HMR_C-continuant-suffix_prob.tsv",
        help="outputs p(passive|consonant_place)",
    )
    # PART14 [+/-voiced]
    parser.add_argument(
        "-o46",
        "--output46",
        default="14_HMR_C-voicing-suffix_prob.tsv",
        help="outputs p(passive|consonant_place)",
    )
    # PART15 [spread glottis]
    parser.add_argument(
        "-o49",
        "--output49",
        default="15_HMR_C-spread-g-suffix_prob.tsv",
        help="outputs p(passive|consonant_place)",
    )
    main(parser.parse_args())
