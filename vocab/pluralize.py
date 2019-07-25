import os, sys
from pattern.en import pluralize, singularize

for w in open(sys.argv[1], 'r'):
    w = w.strip()
    print('"' + w + '",')
    print('"'+ pluralize(w) + '",')

