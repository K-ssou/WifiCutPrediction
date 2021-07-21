from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split
import sys
import torch
import pandas as pd
import numpy as np
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor, Lambda, Compose
import matplotlib.pyplot as plt
from torch.utils.data import Dataset
import random
import math
from sklearn.tree import DecisionTreeClassifier

# Parse the cut file in tensor for the network


def Parser(filename):
    X = []
    y = []
    f = open(filename, "r")
    text = f.readlines()
    l = len(text)
    for i in range(l - 1):
        line = text[i]
        line = line.replace("\n", "")
        result = text[i + 1]
        result = result.replace("\n", "")
        bouts_line = line.split(" ")
        bouts_res = result.split(" ")
        y.append(int(bouts_res[0]))
        data = []
        for i in range(len(bouts_line) - 1):
            if i == 4:
                for j in range(7):
                    data.append(0)
                data[int(i+float(bouts_line[i]))] = 1
            else:
                data.append(float(bouts_line[i]))
        X.append(data)
    return (X, y)


#IMEI = "46bd"
#IMEI = "203a"
#IMEI = "936f"
#IMEI = "4517"
#IMEI = "bacd"
#IMEI = "e6d2"
#IMEI = "f1d9"
IMEI = "63cd"
#IMEI = "677a"
#IMEI = "bd0d04ef821fa7df8de5a4f1b0d2633d704809f1acd6b3faf780e560c5af4278"
#slot = "15mn"
slot = "1h"
filename = "/home/cgilet/AdaBoost/Data/ADA_cuts_{}_{}.txt".format(
    IMEI[:4], slot)

X, Y = Parser(filename)

nb_1 = sum(Y)
print(f"Pourcentage de 1 : {nb_1/len(Y)*100}")


################################ ADABOOST ##############################################
train_x, test_x, train_y, test_y = train_test_split(
    X, Y, random_state=101, stratify=Y)

print("AdaBoost")

clf = AdaBoostClassifier(random_state=96)
clf.fit(train_x, train_y)
print(f"TrainAcc = {clf.score(train_x, train_y)*100}%")
print(f"TestAcc = {clf.score(test_x, test_y)*100}%")

TP = 0
TN = 0
FP = 0
FN = 0
predictions = clf.predict(X)
true = (predictions == Y)
TP = sum(true*Y)
TN = sum(true)-TP
false = (predictions != Y)
FN = sum(false*Y)
FP = sum(false)-FN

print(f"TP = {TP}")
print(f"TN = {TN}")
print(f"FP = {FP}")
print(f"FN = {FN}")

############################## RandomForestClassifier ###########################################

print("RandomForest")

clf = AdaBoostClassifier(random_state=96, base_estimator=DecisionTreeClassifier(
    random_state=101), n_estimators=200, learning_rate=0.5)
clf.fit(train_x, train_y)
print(f"TestAcc = {clf.score(test_x, test_y)*100}%")

TP = 0
TN = 0
FP = 0
FN = 0
predictions = clf.predict(X)
true = (predictions == Y)
TP = sum(true*Y)
TN = sum(true)-TP
false = (predictions != Y)
FN = sum(false*Y)
FP = sum(false)-FN

print(f"nombre de mesures : {len(Y)}")
print(f"nombre de cuts : {sum(Y)}")
print(f"nombre de mesures sans cut : {len(Y)-sum(Y)}")
print(f"TP = {TP}")
print(f"TN = {TN}")
print(f"FP = {FP}")
print(f"FN = {FN}")
print(f"Sensitivity : {TP/(FN+TP)}")
print(f"Specificity : {TN/(FP+TN)}")

################################## RESULTS #################################################
"""clf = AdaBoostClassifier(random_state=96, base_estimator=RandomForestClassifier(random_state=101), n_estimators=100, learning_rate=0.01)
TP = 260
TN = 9424
FP = 35
FN = 115
"""

""" clf = AdaBoostClassifier(random_state=96, base_estimator=DecisionTreeClassifier(
    random_state=101), n_estimators=100, learning_rate=0.01)
TP = 263
TN = 9372
FP = 87
FN = 112
"""

"""clf = AdaBoostClassifier(random_state=96, base_estimator=DecisionTreeClassifier(
    random_state=101), n_estimators=100, learning_rate=0.5)
TP = 286
TN = 9380
FP = 79
FN = 89
"""

"""clf = AdaBoostClassifier(random_state=96, base_estimator=DecisionTreeClassifier(
    random_state=101), n_estimators=200, learning_rate=0.5)
TP = 288
TN = 9374
FP = 85
FN = 87
"""


##################################### With 1 feature/day #######################################
"""
def Parser(filename):
    X = []
    y = []
    f = open(filename, "r")
    text = f.readlines()
    l = len(text)
    for i in range(l - 1):
        line = text[i]
        line = line.replace("\n", "")
        result = text[i + 1]
        result = result.replace("\n", "")
        bouts_line = line.split(" ")
        bouts_res = result.split(" ")
        y.append(int(bouts_res[0]))
        data = []
        for i in range(len(bouts_line) - 1):
            if i == 4:
                for j in range(7):
                    data.append(0)
                data[int(i+float(bouts_line[i]))] = 1
            else:
                data.append(float(bouts_line[i]))
        X.append(data)
    return (X, y)
"""
"""
TestAcc = 94.63196421309476%
TP = 280
TN = 9391
FP = 68
FN = 95
Sensitivity : 0.7466666666666667
Specificity : 0.9928110793952849
"""

############## With 1 feature week + 1 feature we ##################################
"""def Parser(filename):
    X = []
    y = []
    f = open(filename, "r")
    text = f.readlines()
    l = len(text)
    for i in range(l - 1):
        line = text[i]
        line = line.replace("\n", "")
        result = text[i + 1]
        result = result.replace("\n", "")
        bouts_line = line.split(" ")
        bouts_res = result.split(" ")
        y.append(int(bouts_res[0]))
        data = []
        for i in range(len(bouts_line) - 1):
            if i == 4 and float(bouts_line[i]) < 5:
                data.append(1)
                data.append(0)
            elif i == 4 and float(bouts_line[i]) >= 5:
                data.append(0)
                data.append(1)
            else:
                data.append(float(bouts_line[i]))
        X.append(data)
    return (X, y)
"""
"""
TestAcc = 94.63196421309476%
TP = 220
TN = 9405
FP = 54
FN = 155
Sensitivity : 0.5866666666666667
Specificity : 0.994291151284491
"""


####################### Slot 15mn #####################################
"""
TestAcc = 86.5040650406504%
nombre de mesures : 2460
nombre de cuts : 286
nombre de mesures sans cut : 2174
TP = 216
TN = 2134
FP = 40
FN = 70
Sensitivity : 0.7552447552447552
Specificity : 0.9816007359705612
"""

###################### Other phone ##################################
""" 677a
TestAcc = 80.66914498141264%
nombre de mesures : 1075
nombre de cuts : 154
nombre de mesures sans cut : 921
TP = 99
TN = 892
FP = 29
FN = 55
Sensitivity : 0.6428571428571429
Specificity : 0.9685124864277959
"""

""" bd0d
TestAcc = 81.66666666666667%
nombre de mesures : 1197
nombre de cuts : 205
nombre de mesures sans cut : 992
TP = 162
TN = 958
FP = 34
FN = 43
Sensitivity : 0.7902439024390244
Specificity : 0.9657258064516129
"""

""" 63cd
TestAcc = 86.5040650406504%
nombre de mesures : 2460
nombre de cuts : 286
nombre de mesures sans cut : 2174
TP = 216
TN = 2134
FP = 40
FN = 70
Sensitivity : 0.7552447552447552
Specificity : 0.9816007359705612
"""
