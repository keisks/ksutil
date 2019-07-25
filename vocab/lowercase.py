import os, sys

for w in open(sys.argv[1], 'r'):
    w = w.strip()
    print('"' + w.lower() + '",')

