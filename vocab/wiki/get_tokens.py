import os
import sys
import re
from collections import Counter

for line in open("./frequency_lists_PG_200604.txt", 'r'):
    line = line.strip()
    tokens = line.split()
    if len(tokens) > 3:
        m = re.search(r"\[\[(\w+)\]\]", line)
        if m is None:
            pass
        else:
            #print(m.group(1))
            print(m.group(1).lower())

for line in open("./contemporary_fiction.txt", 'r'):
    line = line.strip()
    if line.startswith("#"):
        m = re.search(r"\[\[(\w+)\]\]", line)
        if m is None:
            pass
        else:
            #print(m.group(1))
            print(m.group(1).lower())
 

for line in open("./contemporary_fiction_60_categories.txt", 'r'):
    line = line.strip()
    if line.startswith("*"):
        m = re.search(r"\[\[(\w+)\]\]", line)
        if m is None:
            pass
        else:
            #print(m.group(1))
            print(m.group(1).lower())
 
