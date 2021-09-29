import os 
import sys
import csv
import random
random.seed(42)

def cross_validation_split(dataset, folds=5, shuffle=False):
    if shuffle:
        random.shuffle(dataset)

    fold_size = int(len(dataset)/folds)

    fold_data = []

    idx = 0
    for i in range(folds):
        fold_i = []
        while len(fold_i) < fold_size:
            fold_i.append(dataset[idx])
            idx += 1

        fold_data.append(fold_i) 

    # If we want to use all the data points, add the remaining
    #if idx<len(dataset):
    #    fold_data.append(dataset[idx:])

    return fold_data


r = cross_validation_split(list(range(101)), 5)
print(r)
