#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import csv

tabin = csv.reader(sys.stdin, delimiter='\t')
commaout = csv.writer(sys.stdout, dialect=csv.excel)

for row in tabin:
      commaout.writerow(row)

