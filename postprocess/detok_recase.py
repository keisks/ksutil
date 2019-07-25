#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
from nltk.tokenize.treebank import TreebankWordTokenizer, TreebankWordDetokenizer # nltk 3.3
from truecaser.Truecaser import *
import _pickle as cPickle

def convert(tokens, wordCasingLookup, uniDist, backwardBiDist, forwardBiDist, trigramDist):
    return getTrueCase(tokens, 'as-is', wordCasingLookup, uniDist, backwardBiDist, forwardBiDist, trigramDist)

# load a truecase model
print("load truecaser", file=sys.stderr)
f = open("truecaser/distributions.obj", 'rb')
uniDist = cPickle.load(f)
backwardBiDist = cPickle.load(f)
forwardBiDist = cPickle.load(f)
trigramDist = cPickle.load(f)
wordCasingLookup = cPickle.load(f)
f.close()

if __name__ == "__main__":
    sent = "Tom and Jerry are n't going today , but I 'll watch TV ."
    tokens = [x.lower() for x in sent.split()]
    print(tokens)
    truecase_tokens = convert(tokens, wordCasingLookup, uniDist, backwardBiDist, forwardBiDist, trigramDist)
    detokenizer = TreebankWordDetokenizer()
    sent = detokenizer.detokenize(truecase_tokens)
    print(sent)

