#!/usr/bin/env python
#encoding: utf-8

__author__ = 'Keisuke SAKAGUCHI'
__descripstion__ = "extract plain texts (document by document) from gigaword files"
__prerequisite__ = ""
# 1. Download lxml from http://lxml.de/
# 2. Before running this script, gigaword files should be modified by the commands: 
#    gunzip *.gz
#    find . -name "nyt*" |xargs -i% ksh -c '(echo "<ROOT>"; cat %; echo "</ROOT>") > %.xml'
__usage__ = "python xml2text.py xmlFilename"

import sys
import os
from lxml import etree

# For arguments information
#
argvs = sys.argv       #argument values
argc = len(argvs)      #argument length

# For checking the number of arguments
# If it's not correct, print out an error message.

if (argc != 2):
    print "Argument error. Usage: " + __usage__
    sys.exit()

# extract text from xml file
def extractTxt(filepath):
    f = open(filepath, 'rb')
    xmltree = etree.fromstring(f.read())

    # get documents from xml file
    documents = xmltree.xpath('//DOC')
    for doc in documents:
        # filename is copied from docID
        docID = doc.attrib['id']
        out_f = open('docs/' + docID, 'wb')
        
        # get texts in each paragraph
        paragraphs = doc.findall('.//P')
        for p in paragraphs:
            #print p.text,
            out_f.writelines(p.text.encode('utf-8'))

        out_f.close()

    f.close()

if __name__ == '__main__':
    extractTxt(argvs[1])
