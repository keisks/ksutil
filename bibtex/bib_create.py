#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import copy
import bibtexparser # pip install bibtexparser

with open(sys.argv[1]) as bibtex_in:
    bib_database = bibtexparser.load(bibtex_in)
    print("Original BibTeX entries are:")
    print(bib_database.entries[0])
    bib_info = copy.deepcopy(bib_database.entries[0])
    bib_info["Summary"] = "my summary"
    bib_info["Comments"] = "my comments"
    #print(bib_info)
    bib_database.entries = [bib_info]

    with open("new_"+sys.argv[1], 'w') as bibtex_out:
        bibtexparser.dump(bib_database, bibtex_out)

    print("new_" + sys.argv[1] + " is created.")

