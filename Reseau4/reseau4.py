# /usr/bin/python /home/cgilet/Codes/Reseau1/reseau1.py

import sys
import torch
import numpy as np
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor, Lambda, Compose
import matplotlib.pyplot as plt
from torch.utils.data import Dataset
import random
import math

# Define our own loss to weight the loss
# Give a higher weight to penalize the non-detection of a cut


class customloss(torch.nn.Module):
    def __init__(self):
        super(customloss, self).__init__()

    def forward(self, pred, tensor_y):
        eps = 0.4  # Accept the prediction if |pred - real|<eps
        diff = abs(pred - tensor_y)
        mask_diff = (diff >= eps).float()
        mask_cut = (tensor_y == 1).float()

        loss_val = (
            (200 * mask_cut + 10) * mask_diff * diff
        )  # Change the values of weight
        return torch.sum(loss_val)


# Parse the cut file in tensor for the network
def Parser(filename):
    X = []
    y = []
    f = open(filename, 'r')
    text = f.readlines()
    l = len(text)
    for i in range(l):
        line = text[i]
        line = line.replace('\n', "")
        bouts_line = line.split(' ')
        y.append(int(bouts_line[0]))
        data = []
        for i in range(len(bouts_line)-1):
            data.append(float(bouts_line[i]))
        X.append(data)
    cut = y.copy()
    for i in range(l):  # Changement de features
        prev = 1
        nex = 1
        while (i - prev) >= 0 and cut[i - prev] != 1:
            prev += 1
        while (i + nex) <= (l-1) and cut[i + nex] != 1:
            nex += 1
        X[i][0] = prev
        y[i] = nex
    return (X, y)


# File to open
# IMEI = "bd0d04ef821fa7df8de5a4f1b0d2633d704809f1acd6b3faf780e560c5af4278"
# IMEI = "677aba9f4c7375c0ac5443d680b6114cd0d36983342aca01e84e8afd907396ec"
IMEI = "63cdb165eda519857699323789e720c662592e869104383a4523c15198b5f510"
filename = "/home/cgilet/Codes/Reseau1/Data/ADA_cuts_{}.txt".format(IMEI[:4])

X, Y = Parser(filename)

# Divide all the data in test set (20%) and train set (80%)
idx_test = math.floor(80 * len(X) / 100)
X_train = X[:idx_test]
X_test = X[idx_test:]
Y_train = Y[:idx_test]
Y_test = Y[idx_test:]

nbelt = len(X[0])

# Normalize data
moy_X = np.mean(X_train, 0)
sigma_X = np.std(X_train, 0)
X_train = (X_train - moy_X) / sigma_X
X_test = (X_test - moy_X) / sigma_X


# Get cpu or gpu device for training.
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using {} device".format(device))

# Define model


class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.l1 = nn.Linear(nbelt, 128)
        self.r1 = nn.ReLU()
        self.l2 = nn.Linear(128, 64)
        self.r2 = nn.ReLU()
        self.l3 = nn.Linear(64, 32)
        self.r3 = nn.ReLU()
        self.l4 = nn.Linear(32, 1)

    def forward(self, x):
        x = self.l1(x)
        x = self.r1(x)
        x = self.l2(x)
        x = self.r2(x)
        x = self.l3(x)
        x = self.r3(x)
        x = self.l4(x)
        return x


model = NeuralNetwork().to(device)
print(model)
loss_fn = nn.L1Loss()
#loss_fn = customloss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
y_t = torch.tensor(Y_test).float()

nb_epoch = 20
for epoch_num in range(nb_epoch):
    good_pred = 0
    print(f"Epoch : {epoch_num}")
    print("Train")
    for idx in range(len(X_train)):
        tensor_x = torch.tensor([X_train[idx]]).float()
        tensor_y = torch.tensor([[Y_train[idx]]]).float()

        pred = model(tensor_x)
        loss = loss_fn(pred, tensor_y)
        # loss = customloss(pred, tensor_y)
        if idx % 100 == 0:
            print(f"loss: {loss.item():>7f}")

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print("Test")

    bonne_pred_0 = 0
    bonne_pred_1 = 0
    for idx in range(len(X_test)):
        tensor_x = torch.tensor([X_test[idx]]).float()
        tensor_y = torch.tensor([[Y_test[idx]]]).float()

        pred = model(tensor_x)
        loss = loss_fn(pred, tensor_y)
        if loss.item() < 2:
            good_pred += 1
        if idx % 100 == 0:
            print(f"loss: {loss.item():>7f}")
    print(f"acc: {good_pred/len(X_test)*100}%")


####################### TEST ###########################################
# test = [[0.0, 1.0, 0.0, 1.0, 4.0, 3.0, 0.0, 0.0, 1.0, 35.0]] #OK
# test = [[0.0, 1.0, 0.0, 0.0, 3.0, 11.0, 1.0, 0.0, 0.0, 60.0]] #OK
# test = [[1.0, 1.0, 0.0, 0.0, 3.0, 1.0, 0.0, 0.0, 0.0, 61.0]] #Pas OK
# test = [[1.0, 0.0, 0.0, 0.0, 4.0, 11.0, 0.0, 0.0, 0.0, 40.0]] #OK
# test = [[1.0, 0.0, 0.0, 0.0, 4.0, 12.0, 0.0, 0.0, 0.0, 41.0]]
# test = (test - moy_X) / sigma_X
# test = torch.tensor(test).float()
# print(model(test).item())
#######################################################################
