#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

# Universal Dependency
FIELDS = ['id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head', 'deprel', 'deps', 'misc']

if __name__ == "__main__":
    # put all the sentences into nested list
    file = open(sys.argv[1], 'r')
    line = file.readline()
    sentences = []
    current_sent = []
    while line:
        if line == '\n':
            sentences.append(current_sent)
            current_sent = []
        else:
            current_sent.append(line.strip().split('\t'))
        line = file.readline()

    print len(sentences)

