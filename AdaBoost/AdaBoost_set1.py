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
            data.append(float(bouts_line[i]))
        X.append(data)
    return (X, y)


IMEI = "63cdb165eda519857699323789e720c662592e869104383a4523c15198b5f510"
filename = "/home/cgilet/Reseau1/Data/ADA_cuts_{}.txt".format(IMEI[:4])

X, Y = Parser(filename)

nb_1 = sum(Y)
print(f"Pourcentage de 1 : {nb_1/len(Y)*100}")


################################ ADABOOST ##############################################
train_x, test_x, train_y, test_y = train_test_split(
    X, Y, random_state=101, stratify=Y)

print("AdaBoost")

clf = AdaBoostClassifier(random_state=96)
print(clf.fit(train_x, train_y))
print(f"TrainAcc = {clf.score(train_x, train_y)*100}%")
print(f"TestAcc = {clf.score(test_x, test_y)*100}%")


############################## RandomForestClassifier ###########################################

print("RandomForest")

clf = AdaBoostClassifier(random_state=96, base_estimator=RandomForestClassifier(
    random_state=101), n_estimators=100, learning_rate=0.01)
clf.fit(train_x, train_y)
print(f"TestAcc = {clf.score(test_x, test_y)}%")


# Slot d'1h ?
# Calcul TP/TN/FP/FN -> pour 1 / pour 0

# Lundi ou le 15, aprem sinon semaine suivante lundi avant 16H (10H) ou le mardi ou mecredi
