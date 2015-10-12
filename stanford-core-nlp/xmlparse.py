#!/usr/bin/env python
#encoding: utf-8

__author__ = "Keisuke Sakaguchi"
__usage__ = ""

import os
import sys
import xml.etree.ElementTree as ET

def parseXML(xmlPath):
    parsedSentenceList = []
    
    elem = ET.parse(xmlPath).getroot()
    sentences = elem.findall(".//sentences")

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

        # dependency diectionaries (key is ID)
        # note that ID starts from 1 in the stanfordCoreNLP
        basDepDict = {}
        colDepDict = {}
        ccpDepDict = {}


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

        # get dependencies

        #sent.findall('.//dependencies')[0].attrib['type'] == 'basic-dependencies':
        for dependency in sent.findall('.//dependencies'):
            if dependency.attrib['type'] == "basic-dependencies":
                for dep in dependency:
                    depType = dep.attrib['type']
                    depGov = int(dep.find('.//governor').attrib['idx'])-1
                    depDep = int(dep.find('.//dependent').attrib['idx'])-1
                    basDepList.append((depType, depGov, depDep))

                    # dependency dictionary (the key is word ID)
                    if basDepDict.has_key(depGov):
                        basDepDict[depGov].append((depType, depDep))
                    else:
                        basDepDict[depGov] = [(depType, depDep)]
                sentDict['basDep'] = basDepList
                sentDict['basDepID'] = basDepDict

            elif dependency.attrib['type'] == "collapsed-dependencies":
                for dep in dependency:
                    depType = dep.attrib['type']
                    depGov = int(dep.find('.//governor').attrib['idx'])-1
                    depDep = int(dep.find('.//dependent').attrib['idx'])-1
                    colDepList.append((depType, depGov, depDep))

                    # dependency dictionary (the key is word ID)
                    if colDepDict.has_key(depGov):
                        colDepDict[depGov].append((depType, depDep))
                    else:
                        colDepDict[depGov] = [(depType, depDep)]

                sentDict['colDep'] = colDepList
                sentDict['colDepID'] = colDepDict

            elif dependency.attrib['type'] == "collapsed-ccprocessed-dependencies":
                for dep in dependency:
                    depType = dep.attrib['type']
                    depGov = int(dep.find('.//governor').attrib['idx'])-1
                    depDep = int(dep.find('.//dependent').attrib['idx'])-1
                    ccpDepList.append((depType, depGov, depDep))

                    # dependency dictionary (the key is word ID)
                    if ccpDepDict.has_key(depGov):
                        ccpDepDict[depGov].append((depType, depDep))
                    else:
                        ccpDepDict[depGov] = [(depType, depDep)]

                sentDict['ccpDep'] = ccpDepList
                sentDict['ccpDepID'] = ccpDepDict

            else:
                pass

        # get coreference information (not yet implemented)
        # coming soon...?
        # 

        parsedSentenceList.append(sentDict)

    return parsedSentenceList


if __name__ == "__main__":
    print parseXML(sys.argv[1])
