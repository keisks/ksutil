#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import csv

tabin = csv.reader(sys.stdin, delimiter='\t')
commaout = csv.writer(sys.stdout, dialect=csv.excel)
#commaout = csv.writer(sys.stdout, delimiter=',')

for row in tabin:
      commaout.writerow(row)

