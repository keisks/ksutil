#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import enchant

d = enchant.Dict("en_US")
for line in open(sys.argv[1], 'r'):
    new_line = []
    for t in line.rstrip().split():
        if not t.isalpha():
            new_line.append(t)
        elif d.check(t):
            new_line.append(t)
        else:
            try:
                new_line.append(d.suggest(t)[0])
            except IndexError:
                new_line.append(t)

    print(" ".join(new_line))

