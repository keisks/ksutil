#!/usr/bin/env python
#encoding: utf-8

__author__ = 'Keisuke Sakaguchi'
__version__ = "0.1"
__descripstion__ = "calculate edit distance for given two sequences (e.g. lists or strings) "
__usage__ = "python edit_dist.py seqence1 sequence2"#

import os
import sys

#Constant Values
ins_cost = 1 # insertion cost
del_cost = 1 #deletion cost
sub_cost = 1 #substitution cost
#edThreshold = 3 # edit distance threshold 


def getEditDist(seq1, seq2):
    if isinstance(seq1, str):
        seq1 = list(seq1)
    if isinstance(seq2, str):
        seq2 = list(seq2)

    seq1 = ['#'] + seq1
    seq2 = ['#'] + seq2
    
    dist_matrix = [[0 for j in range(len(seq1))] for i in range(len(seq2))]
    for i in range(len(seq1)):
        dist_matrix[0][i] = i
    for j in range(len(seq2)):
        dist_matrix[j][0] = j

    move_matrix = [[0 for j in range(len(seq1))] for i in range(len(seq2))]
    move_matrix[0][0] = '#'
    for i in range(1,len(seq1)):
        move_matrix[0][i] = "I"
    for j in range(1,len(seq2)):
        move_matrix[j][0] = "D"
   
    #calculate edit distance using DP
    for j in range(1, len(seq1)):
        for i in range(1, len(seq2)):
            # compute cost for insertion, deletion, and replace(substitution)
            cost1 = dist_matrix[i][j-1] + ins_cost
            cost2 = dist_matrix[i-1][j] + del_cost
            if seq1[j] == seq2[i]:
                cost3 = dist_matrix[i-1][j-1]
            else:
                cost3 = dist_matrix[i-1][j-1] + sub_cost

            # decide the move
            if cost3 <= cost2 and cost3 <= cost1:
                dist_matrix[i][j] = cost3
                move_matrix[i][j] = 'R'
            elif cost2 <= cost3 and cost2 <= cost1:
                dist_matrix[i][j] = cost2
                move_matrix[i][j] = "D"
            else:
                dist_matrix[i][j] = cost1
                move_matrix[i][j] = "I"
    
    # get operations
    j = len(seq1)-1
    i = len(seq2)-1
    prev_move = move_matrix[i][j]
    moves = [prev_move]
    while not (prev_move == "#"):
        if prev_move == "I": 
            prev_move = move_matrix[i][j-1]
            j -= 1
            moves.append("I")
        elif prev_move == "D":
            prev_move = move_matrix[i-1][j]
            i -= 1
            moves.append("D")
        elif prev_move == "R":
            if dist_matrix[i][j] == dist_matrix[i-1][j-1]:
                moves.append("_")
            else:
                moves.append("R")

            prev_move = move_matrix[i-1][j-1]
            j -= 1
            i -= 1

    return dist_matrix[-1][-1], moves[::-1]


if __name__ == '__main__':
    # unit test
    #print getEditDist('dog', 'bag')    # replace*2
    #print getEditDist('dog', 'cat')    # replace*3
    #print getEditDist('dog', 'doing')  # replace*1 + insert*1
    #print getEditDist('dog', 'do')     # delete*1
    #print getEditDist([1,3], [2,3])    # replace*1
    print getEditDist([1,2,3,5,6], [1,2,4,5])    # replace*1

    #print getEditDist(sys.argv[1], sys.argv[2])
