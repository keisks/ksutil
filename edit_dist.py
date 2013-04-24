#!/usr/bin/env python
#encoding: utf-8

__author__ = 'Keisuke Sakaguchi'
__version__ = "0.1"
__descripstion__ = "calculate edit distance for given two words "
__usage__ = "python editDist.py WORD1 WORD2"#

import os
import sys

#Constant Values
ins_cost = 1 # insertion cost
del_cost = 1 #deletion cost
sub_cost = 1 #substitution cost
#edThreshold = 3 # edit distance threshold 


def getEditDist(str1, str2):

    #check if both arguments are strings
    if type(str1) != str or type(str2) != str:
        raise TypeError('arguments are not string')

    else:
        str1 = '#' + str1 #add initial (special) character
        str2 = '#' + str2 #add initial (special) character
        
        #make a matrix with the size of str1 * str2 length
        dist_matrix = [[0 for j in range(len(str1))] for i in range(len(str2))]
        for i in range(len(str1)):
            dist_matrix[0][i] = i
        for j in range(len(str2)):
            dist_matrix[j][0] = j
        
        #calculate edit distance using DP
        for j in range(1, len(str1)):
            for i in range(1, len(str2)):
                cost1 = dist_matrix[i][j-1] + ins_cost
                cost2 = dist_matrix[i-1][j] + del_cost
                if str1[j] == str2[i]:
                    cost3 = dist_matrix[i-1][j-1]
                else:
                    cost3 = dist_matrix[i-1][j-1] + sub_cost
                
                if cost3 <= cost2 and cost3 <= cost1:
                    dist_matrix[i][j] = cost3
                elif cost2 <= cost3 and cost2 <= cost1:
                    dist_matrix[i][j] = cost2
                else:
                    dist_matrix[i][j] = cost1
        
        return dist_matrix[-1][-1]

if __name__ == '__main__':
    # unit test
    #print getEditDist('dog', 'bag')     # replace*2
    #print getEditDist('dog', 'cat')     # replace*3
    #print getEditDist('dog', 'doing')   # replace*1 + insert*1
    #print getEditDist('dog', 'do')      # delete*1

    print getEditDist(sys.argv[1], sys.argv[2])
