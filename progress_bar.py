#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import progressbar # pip install progressbar2

# Setup progressbar$
bar = progressbar.ProgressBar(widgets=[
    ' [', progressbar.Timer(), '] ',
    progressbar.Bar(),
    ' (', progressbar.ETA(), ') ',])

iterations = 10000000
last = 0
for i in bar(range(iterations)):
    last = i
print(last)

