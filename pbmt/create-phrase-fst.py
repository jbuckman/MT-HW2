from __future__ import print_function
from collections import namedtuple
import sys

INPUT_DIR = sys.argv[1]
OUTPUT_DIR = sys.argv[2]

with open(INPUT_DIR, "r") as infile:
    phrases = [line.strip().split("\t") for line in infile]

Node = namedtuple("Node", ["name", "id", "children"])

ROOT = Node("", 0, {})
count = 1
with open(OUTPUT_DIR, "w") as outfile:
    for source, target, score in phrases:
        cur = ROOT
        for word in source.split():
            if word in cur.children:
                # print("si")
                cur = cur.children[word]
            else:
                print("%d %d %s <eps>" % (cur.id, count, word), file=outfile)
                new_node = Node(word, count, {})
                cur.children[word] = new_node
                cur = new_node
                count += 1
        for word in target.split():
            if word in cur.children:
                # print("yes")
                cur = cur.children[word]
            else:
                print("%d %d <eps> %s" % (cur.id, count, word), file=outfile)
                new_node = Node(word, count, {})
                cur.children[word] = new_node
                cur = new_node
                count += 1
        print("%d %d <eps> <eps> %4f" % (cur.id, 0, float(score)), file=outfile)
        # print(source, target, count)
    print("0 0 </s> </s>", file=outfile)
    print("0 0 <unk> <unk>", file=outfile)
    print("0", file=outfile)