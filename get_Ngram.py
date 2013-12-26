#!/usr/bin/env python
#encoding: utf-8

__author__ = "Keisuke Sakaguchi"
__version__ = "0.1"
__descripstion__ = "INPUT: Segmented words, # of N, OUTPUT: N-gram list"
__usage__ = "python get_Ngram.py N"

import sys
import os

def ngram(wordList, N):
    BOS = ['<s>']
    EOS = ['</s>']

    wordList = BOS + wordList + EOS
    ngramList = []
    for j in range(len(wordList)):
        for i in range(j):
            if j-i == N:    # set '<=' instead of '==' when extracting 1..N gram 
                ngramList.append(" ".join(wordList[i:j]))

    return ngramList

if __name__ == '__main__':

    #Test 
    n = 3
    words = ['This', 'is', 'a', 'test', 'sentence', '.']
    print ngram(words, n)
    
    """ Result
    ['<s> This is', 'This is a', 'is a test', 'a test sentence', 'test sentence .']
    """




