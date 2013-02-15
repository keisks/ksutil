#!/usr/bin/env python
#encoding: utf-8

__author__ = 'Keisuke SAKAGUCHI'
__version__ = "0.1"
__license__ = "GPL v3"
__descripstion__ = "Parsing stanfordCoreNLP-parsed xml file."
__usage__ = "python stanfordXmlParser.py FILE(*.xml)"

import sys
import os
from lxml import etree

def parseXml(xmlPath):
    
    parsedSentenceList = []
    
    # Open the file with lxml
    f = open(xmlPath, 'r')
    xmltree = etree.fromstring(f.read())
    sentences = xmltree.xpath('//sentences')
    document = xmltree.xpath('//document')

    # extracting tokens, parse-tree, dependencies, and coreferences

    for sent in sentences[0].findall('.//sentence'):
        # sentence information is stored in a dictionary
        sentDict = {}
        wordList = []
        lemmaList = []
        posList = []
        nerList = []
        cobList = []        # CharacterOffsetBegin
        coeList = []        # CharacterOffsetEnd

        basDepList = []     # basic dependency
        colDepList = []     # collapsed dependency
        ccpDepList = []     # collapsed-ccprocessed dependency

        # get id
        sentDict['id'] = sent.attrib['id']
        sentDict['tree'] = sent.find('.//parse').text

        # get token information: word, lemma, pos, ner, and offsets
        for token in sent.findall('.//token'):
            if token.find('.//word').text is not None:
                wordList.append(token.find('.//word').text)
            else:
                pass

            if token.find('.//lemma').text is not None:
                lemmaList.append(token.find('.//lemma').text)
            else:
                pass

            if token.find('.//POS').text is not None:
                posList.append(token.find('.//POS').text)
            else:
                pass

            if token.find('.//NER').text is not None:
                nerList.append(token.find('.//NER').text)
            else:
                pass

            if token.find('.//CharacterOffsetBegin').text is not None:
                cobList.append(token.find('.//CharacterOffsetBegin').text)
            else:
                pass

            if token.find('.//CharacterOffsetEnd').text is not None:
                coeList.append(token.find('.//CharacterOffsetEnd').text)
            else:
                pass

        # append each list into sentence dictionary
        sentDict['word'] = wordList
        sentDict['lemma'] = lemmaList
        sentDict['pos'] = posList
        sentDict['ner'] = nerList
        sentDict['cob'] = cobList
        sentDict['coe'] = coeList

        # get (basic) dependency
        if sent.find('.//basic-dependencies') is not None:
            basDep = sent.find('.//basic-dependencies')
            for dep in basDep.findall('.//dep'):
                depType = dep.attrib['type']
                depGov = dep.find('.//governor').text
                depDep = dep.find('.//dependent').text
                
                basDepList.append((depType, depGov, depDep))
        else:
            pass
        
        sentDict['basdep'] = basDepList

        # get (collapsed) dependency
        if sent.find('.//collapsed-dependencies') is not None:
            colDep = sent.find('.//collapsed-dependencies')
            for dep in colDep.findall('.//dep'):
                depType = dep.attrib['type']
                depGov = dep.find('.//governor').text
                depDep = dep.find('.//dependent').text
                
                colDepList.append((depType, depGov, depDep))
        else:
            pass

        sentDict['coldep'] = colDepList

        # get (collapsed-ccprocessed) dependency
        if sent.find('.//collapsed-ccprocessed-dependencies') is not None:
            ccpDep = sent.find('.//collapsed-ccprocessed-dependencies')
            for dep in ccpDep.findall('.//dep'):
                depType = dep.attrib['type']
                depGov = dep.find('.//governor').text
                depDep = dep.find('.//dependent').text
                
                ccpDepList.append((depType, depGov, depDep))
        else:
            pass

        sentDict['coldep'] = colDepList

        # get coreference information (not yet implemented)
        # coming soon...
        # 

        parsedSentenceList.append(sentDict)

    return parsedSentenceList

if __name__ == '__main__':
    
    # For module tests, write code here.
    print parseXml(sys.argv[1])
    
