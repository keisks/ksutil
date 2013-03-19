#!/usr/bin/env python
#encoding: utf-8

__author__ = 'Keisuke SAKAGUCHI'
__version__ = "0.1"
__descripstion__ = "very simple word regularizer"
__usage__ = "python word_regularize.py WORD"

import sys
import os
import re

numWordList = [
        'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
        'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
        'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen',
        'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy',
        'eighty', 'ninety', 'hundred', 'thousand', 'million', 'billion'
        ]

persPronList = [
        'i', 'me', 'my', 'mine', 'myself',
        'we', 'us', 'our', 'ours', 'ourselves',
        'you', 'your', 'yours', 'yourself', 'yourselves',
        'he', 'him', 'his', 'himself',
        'she', 'her', 'hers', 'herself',
        'they', 'them', 'their', 'theirs', 'themselves',
        'it', 'its', 'itself'
        ]

dateList = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
        'January', 'February', 'March', 'April', 
        'May' 'June', 'July', 'August', 'September', 
        'October', 'November', 'December'
        'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun',
        'Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday'
        ]

def regularize(word):

    # check if the word is DATE
    # if true, return word"#DATE#"
    p = re.compile(r'[12]\d{3}/(?:0?[1-9]|1[0-2])/(?:0?[1-9]|[12][0-9]|3[01])') 
    if p.search(word) or word in dateList:
        return "#DATE#"

    # check if the word is TIME
    # if true, return word"#TIME#"
    p = re.compile(r'(?:[01]?[0-9]|2[0-4]):[0-5][0-9]')
    if p.search(word):
        return "#TIME#"

    # check if the word is NUMBER
    # if true, return word "#NUMBER#"
    p = re.compile(r'[+-]?(?:0|[1-9]\d*)(?:\.\d*[1-9])?')
    if p.search(word) or word.lower() in numWordList:
        return "#NUMBER#"

    # check if the word is a personal pronoun
    # if true, return word "#PRP#"
    if word.lower() in persPronList:
        return "#PRP#"

    # check if the word contains non-ascii characters
    # if true, return word "#NonAscii#"
    p = re.compile(r'^[\x20-\x7E]+$')
    if p.search(word) is None:
        return "#NonAscii#"

    # check if the word is e-mail address
    # if true, return word "#EMail#"
    p = re.compile(r'[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+')
    if p.search(word):
        return "#EMail#"

    # check if the word is URL
    # if true, return word "#URL#"
    p = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    if p.search(word):
        return "#URL#"

    else:
        return word

if __name__ == '__main__':
    print regularize(sys.argv[1])

    ''' unit test
    print regularize('dog')                 # dog
    print regularize('1234')                # #NUMBER#
    print regularize('12.34')               # #NUMBER#
    print regularize('0.1234')              # #NUMBER#
    print regularize('fifty')               # #NUMBER#
    print regularize('myself')              # #PRP#
    print regularize('ほげ')                # #NonAscii#
    print regularize('hoge@email.com')      # #EMail#
    print regularize('https://test.org')    # #URL#
    print regularize('2014/1/1')            # #DATE#
    print regularize('23:59:59')            # #TIME#
    '''
