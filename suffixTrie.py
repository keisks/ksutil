#!/usr/bin/env python
#encoding: utf-8

# This is originally from http://nbviewer.ipython.org/gist/anonymous/6603756
# Slightly modified by KS for allowing to add new entries to the suffix trie.

import sys
import os

class SuffixTrie():
    
    def __init__(self, t, st):
        """ Make suffix trie from t """
        t += '$' # special terminator symbol
        self.root = st 
        for i in xrange(len(t)): # for each suffix
            cur = self.root
            for c in t[i:]: # for each character in i'th suffix
                if c not in cur:
                    cur[c] = {} # add outgoing edge if necessary
                cur = cur[c]
    
    def followPath(self, s):
        """ Follow path given by characters of s.  Return node at
            end of path, or None if we fall off. """
        cur = self.root
        for c in s:
            if c not in cur:
                return None
            cur = cur[c]
        return cur
    
    def hasSubstring(self, s):
        """ Return true iff s appears as a substring of t """
        return self.followPath(s) is not None
    
    def hasSuffix(self, s):
        """ Return true iff s is a suffix of t """
        node = self.followPath(s)
        return node is not None and '$' in node


if __name__ == '__main__':
    #Example to use (and unit test)
    strie = SuffixTrie('aab', {}) # First Trie
    strie = SuffixTrie('cab', strie.root) # Add to the Trie
    print strie.root
    print strie.hasSuffix('ca') # False
    print strie.hasSubstring('ca') # True

