import os
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve, auc, accuracy_score

pred_prob = []
pred_list = []
gold_list = []

for row in open(sys.argv[1], 'r'):
    prob = row.strip().split(',')[0]
    pred_prob.append(float(prob))
    if float(prob)>=0.5:
        pred_list.append(1)
    else:
        pred_list.append(0)

for row in csv.DictReader(open("./test.csv", 'r')):
    gold_list.append(int(row["label"]))


precision, recall, threshold = precision_recall_curve(gold_list, pred_prob)

auc_v =  round(auc(recall, precision), 3)
acc = accuracy_score(gold_list, pred_list)
print(f"auc: {auc_v}")
print(f"acc: {acc}")

plt.plot(recall, precision)
plt.xlabel("recall")
plt.ylabel("prec")
plt.savefig("./plot.pdf")
