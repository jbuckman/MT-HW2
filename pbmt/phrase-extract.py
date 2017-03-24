# -*- encoding: utf-8 -*-
from __future__ import print_function
import sys, math, numpy
from collections import defaultdict


'''
Determine whether set of values is quasi-consecutive
  Examples:
    {1, 2, 3, 4, 5, 6} => True
    {4, 2, 3} => True (equivalent to {2, 3, 4})
    {3} => True
    {1, 2, 4} => True if word at position 3 is not aligned to anything, False otherwise
'''
def quasi_consec(tp, source_to_target, target_to_source):
    for j in range(min(tp), max(tp)+1):
        if j not in tp and source_to_target[j] != -1:
            return False
    return True

'''
Given an alignment, extract phrases consistent with the alignment
  Input:
    -e_aligned_words: mapping between E-side words (positions) and aligned F-side words (positions)
    -f_aligned_words: mapping between F-side words (positions) and aligned E-side words (positions)
    -e: E sentence
    -f: F sentence
  Return list of extracted phrases
'''
def phrase_extract(source_to_target, target_to_source, e, f):
    extracted_phrases = set([])
    # Loop over all substrings in the E
    for i1 in range(len(e)):
        for i2 in range(i1, len(e)):
            # Get all positions in F that correspond to the substring from i1 to i2 in E (inclusive)
            tp = set([j for i,j in target_to_source if i1 <= i and i <= i2])
            if len(tp) != 0 and len(tp) < 5 and quasi_consec(tp, source_to_target, target_to_source):
                j1 = min(tp) # min TP
                j2 = max(tp) # max TP
                # Get all positions in E that correspond to the substring from j1 to j2 in F (inclusive)
                sp = set([i for i,j in target_to_source if j1 <= j and j <= j2])
                if len(sp) != 0 and len(sp) < 5 and len([i for i in sp if i1 <= i and i <= i2]) == len(sp): # Check that all elements in sp fall between i1 and i2 (inclusive)
                    e_phrase = e[i1:i2+1]
                    f_phrase = f[j1:j2+1]
                    extracted_phrases.add((tuple(e_phrase), tuple(f_phrase)))
#                    # Extend source phrase by adding unaligned words
                    while j1 >= 0 and source_to_target[j1] == -1: # Check that j1 is unaligned
                        j_prime = j2
                        while j_prime < len(f) and source_to_target[j1] == -1: # Check that j2 is unaligned
                            f_phrase = f[j1:j_prime+1]
                            extracted_phrases.add((tuple(e_phrase), tuple(f_phrase)))
                            j_prime += 1
                        j1 -= 1

    return extracted_phrases

source_fname = sys.argv[1]
target_fname = sys.argv[2]
align_fname = sys.argv[3]
out_fname = sys.argv[4]

with open(source_fname, "r") as infile: source_corpus = [line.strip().split() for line in infile]
with open(target_fname, "r") as infile: target_corpus = [line.strip().split() for line in infile]
with open(align_fname, "r") as infile: align_corpus = [[int(a) for a in line.strip().split()] for line in infile]

phrase_pair_count = defaultdict(float)
target_phrase_count = defaultdict(float)

for source, target, align in zip(source_corpus, target_corpus, align_corpus):
    source_to_target = align
    target_to_source = zip(align, range(len(align)))
    extracted_phrases = phrase_extract(source_to_target, target_to_source, target, source)
    for pair in extracted_phrases:
        # print pair
        phrase_pair_count[pair] += 1
        target_phrase_count[pair[0]] += 1

with open(out_fname, "w") as outfile:
    for pair in phrase_pair_count:
        score = math.log(phrase_pair_count[pair] / target_phrase_count[pair[0]])
        if score < 0: score = -score
        print("%s\t%s\t%.4f" % (' '.join(pair[1]), ' '.join(pair[0]), score), file=outfile)
