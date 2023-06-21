#!/usr/bin/env python

"""This script counts the numbers of passive suffixes attached to verbs in
     Maori.The verbs going through various internal changes are not accounted
     for in this script."""

import argparse
import csv
import logging
import pynini
import collections


from pynini.lib import pynutil
from pynini.lib import rewrite
from collections import Counter

# logging.basicConfig(filename="info.log", level=logging.DEBUG)

# The alphabet: https://teara.govt.nz/en/interactive/41063/the-maori-alphabet
# <ng> and <wh> are diagraphs, but we treat them as separete characters 
# while including their corresponding phonemes.
v = pynini.union(
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
)

c = pynini.union(
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
        # Consonantal phonemes that correspond to the two diagraphs, <ng> and <wh>
        "ŋ",
        "ɸ",
)

sigma_star = pynini.union(v, c).closure().optimize()

# Rules for each of the 12 passive suffixes
tia_rule = pynini.concat(sigma_star, pynutil.insert("tia"))
a_rule = pynini.concat(sigma_star, pynutil.insert("a"))
hia_rule = pynini.concat(sigma_star, pynutil.insert("hia"))
ia_rule = pynini.concat(sigma_star, pynutil.insert("ia"))
ina_rule = pynini.concat(sigma_star, pynutil.insert("ina"))
kia_rule = pynini.concat(sigma_star, pynutil.insert("kia"))
mia_rule = pynini.concat(sigma_star, pynutil.insert("mia"))
na_rule = pynini.concat(sigma_star, pynutil.insert("na"))
nga_rule = pynini.concat(sigma_star, pynutil.insert("nga"))
ngia_rule = pynini.concat(sigma_star, pynutil.insert("ngia"))
ria_rule = pynini.concat(sigma_star, pynutil.insert("ria"))
kina_rule = pynini.concat(sigma_star, pynutil.insert("kina"))

# "tia" rule
assert rewrite.matches("hohou", "hohoutia", tia_rule)
assert not rewrite.matches("arahi", "arahina", tia_rule)
# "a" rule
assert rewrite.matches("ehu", "ehua", a_rule)
assert rewrite.matches("hī", "hīa", a_rule) # an example to test the macrons
assert not rewrite.matches("ato", "atohia", a_rule)
# "hia" rule
assert rewrite.matches("ara", "arahia", hia_rule)
assert not rewrite.matches("arahi", "arahina", hia_rule)
# "ia" rule
assert rewrite.matches("hiko", "hikoia", ia_rule)
assert not rewrite.matches("hirihiri", "hirihiria", ia_rule)
# "ina" rule
assert rewrite.matches("kata", "kataina", ina_rule)
assert not rewrite.matches("kari", "karia", ina_rule)
# "kia" rule
assert rewrite.matches("momoto", "momotokia", kia_rule)
assert not rewrite.matches("momotu", "momotuhia", kia_rule)
# "mia" rule
assert rewrite.matches("nanao", "nanaomia", mia_rule)
assert not rewrite.matches("nati", "natia", mia_rule)
# "na" rule
assert rewrite.matches("ruaki", "ruakina", na_rule)
assert not rewrite.matches("runa", "runaa", na_rule)
# "nga" rule
assert rewrite.matches("kai", "kainga", nga_rule)
assert not rewrite.matches("kanga", "kangaa", nga_rule)
# "ngia" rule
assert rewrite.matches("waikeri", "waikeringia", ngia_rule)
assert not rewrite.matches("hongi", "hongia", ngia_rule)
# "ria" rule
assert rewrite.matches("takapau", "takapauria", ria_rule)
assert not rewrite.matches("tari", "taria", ria_rule)
# "kina" rule
assert rewrite.matches("hopu", "hopukina", kina_rule)
assert not rewrite.matches("rumaki", "rumakina", kina_rule)

# "tanga" rule
# Raises a Composition Failure error
# assert rewrite.matches("hūpana", "hūpanatanga", tanga_rule)
# assert not rewrite.matches("ihiihi", "ihiihia", tanga_rule)

# Pairing suffixes with their corresponding rules to loop over.
rule_dict = {
    "tia": tia_rule,
    "a": a_rule,
    "hia": hia_rule,
    "ia": ia_rule,
    "ina": ina_rule,
    "kia": kia_rule,
    "mia": mia_rule,
    "na": na_rule,
    "nga": nga_rule,
    "ngia": ngia_rule,
    "ria": ria_rule,
    "kina": kina_rule,
}

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

def main(args: argparse.Namespace) -> None:
    final_vowel_counts = collections.Counter()
    with open(args.input, "r") as source, open(args.output, "w") as sink:
        tsv_reader = csv.reader(source, delimiter="\t")
        tsv_writer = csv.writer(sink, delimiter="\t")
        for lemma, passive in tsv_reader:
            for vowel in vowel_dict:
                if lemma.endswith(vowel):
                    final_vowel_counts[vowel] += 1
    # with open(args.output, "w") as sink:
        for vowel, count in final_vowel_counts.most_common():
            # tsv_writer = csv.writer(sink, delimiter="\t")
            tsv_writer.writerow([vowel, count]) # need to give a list argument
            print(f"{vowel}:\t{count}")


    

# def main(args: argparse.Namespace) -> None:
#     final_vowel_counts = Counter()
#     with open(args.input, "r") as source:
#         tsv_reader = csv.reader(source, delimiter="\t")
#         for lemma, passive in tsv_reader:
#             for vowel in v:
#                 for rule_name, rule in rule_dict.items():
#                     rule_found = False  # Using a Boolean expression in the loop
#                     try:
#                         if rewrite.matches(lemma, passive, rule):
#                             if lemma.endswith(vowel):
#                                 final_vowel_counts[vowel] += 1
#                             rule_found = True
#                             # "If some condition is true, I'll take this branch
#                             # down my code."
#                             logging.info("Rule found: %s\t\t%s", lemma, passive)
#                             break
#                     except rewrite.Error:
#                         logging.warning("Composition Failure: %s\t\t%s", lemma, passive)
#                 if not rule_found:
#                     logging.info("No Rules Found: %s\t\t%s", lemma, passive)
#                     print(f"No rules found for {lemma} -> {passive}")
#                     final_vowel_counts["<Irregular>"] += 1
#     for vowel, count in final_vowel_counts.most_common():
#         print(f"{vowel}:\t{count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="input Maori TSV file")
    parser.add_argument(
        "--output", required=True, help="output stem-final vowels with counts"
    )
    main(parser.parse_args())
    # Do I need an output argument?

    # parser.add_argument(
    #     "--output", required=True, help="output Maori file as lemmas"
    # )