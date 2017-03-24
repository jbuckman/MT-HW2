import sys, math, numpy
from collections import defaultdict

source_fname = sys.argv[1]
target_fname = sys.argv[2]
out_fname = sys.argv[3]

with open(source_fname, "r") as infile: source_corpus = [line.strip().split() for line in infile]
# with open(target_fname, "r") as infile: target_corpus = [line.strip().split() for line in infile]
with open(target_fname, "r") as infile: target_corpus = [["<null>"] + line.strip().split() for line in infile]

default_prob = 1./len(set.union(*[set(target) for target in target_corpus]))
alignments = defaultdict(lambda :default_prob)

ITERATIONS = 8
for iter in xrange(ITERATIONS):
    # E STEP
    total_align_prob = defaultdict(float)
    source_denom = defaultdict(float)
    target_denom = defaultdict(float)
    for source, target in zip(source_corpus, target_corpus):
        for s in source:
            for t in target:
                target_denom[t] += alignments[(t, s)]
        for s in source:
            for t in target:
                local_align_prob = alignments[(t, s)] / target_denom[t]
                total_align_prob[(t, s)] += local_align_prob
                source_denom[s] += local_align_prob

    # M STEP
    for t,s in total_align_prob:
        alignments[(t, s)] = total_align_prob[(t, s)] / source_denom[s]

    # CALCULATE & WRITE BEST ALIGNMENTS
    aligned_sents = []
    total_nlp = words = 0.0
    for source, target in zip(source_corpus, target_corpus):
        a = [numpy.argmax([alignments[(t, s)] for t in target]) for s in source]
        total_nlp += -sum([math.log(alignments[target[i], s]) for s, i in zip(source, a)])
        words += len(target)
        # aligned_sents.append(' '.join([str(i) for i in a]))
        aligned_sents.append(' '.join([str(i-1) for i in a]))
    with open(out_fname, "w") as f: f.write('\n'.join(aligned_sents))
    print iter, "|", total_nlp / words

