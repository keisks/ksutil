#!/usr/bin/env python
#encoding: utf-8

__author__ = "Keisuke SAKAGUCHI"
__version__ = "0.1"
__descripstion__ = "get synonyms (in WordNet) for input word with pos"
__usage__ = "python wnSynonyms.py WORD POS"

import sys
import os
from nltk.corpus import wordnet as wn

def get_synonyms(word, pos):
    word_synsets = wn.synsets(word, pos)
    
    synonymList = []
    for synset in word_synsets:
        for synonym in synset.lemmas:
            if ((synonym.name.isalpha())
                and (word != synonym.name)):
                synonymList.append(synonym.name)
    synonymSet = set(synonymList)
    return list(synonymSet)

if __name__ == '__main__':
    # unit test
    # pos: {verb:v, noun:n, adj:a|s, adv:r}
    #print get_synonyms('look', 'v')

    print get_synonyms(sys.argv[1], sys.argv[2])

