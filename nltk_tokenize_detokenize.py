#!/usr/bin/python
# -*- coding: utf-8 -*-
import nltk

data = ["Hi", ",", "my", "name", "is", "Bob", "!"]
if nltk.__version__ == "3.2.2":
    from nltk.tokenize.moses import MosesDetokenizer # nltk 3.2.2
    detokenizer = MosesDetokenizer()
    sent = detokenizer.detokenize(data, return_str=True)

elif nltk.__version__ == "3.3":
    from nltk.tokenize.treebank import TreebankWordTokenizer, TreebankWordDetokenizer # nltk 3.3
    detokenizer = TreebankWordDetokenizer()
    sent = detokenizer.detokenize(data)

else:
    exit()

print(sent)
