import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor, Lambda, Compose
import matplotlib.pyplot as plt
from torch.utils.data import Dataset
import random

def function(x):
    return x**2

x = []
y =[]
for i in range(1000):
    val_x = random.random()*10-5
    x.append(val_x)
    y.append(function(val_x))

# Get cpu or gpu device for training.
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using {} device".format(device))

# Define model
class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.l1 = nn.Linear(1, 64)
        self.r1 = nn.ReLU()
        self.l2 = nn.Linear(64,64)
        self.r2 = nn.ReLU()
        self.l3 = nn.Linear(64,1)
        

    def forward(self, x):
        x = self.l1(x)
        x = self.r1(x)
        x = self.l2(x)
        x = self.r2(x)
        x = self.l3(x)
        return x

model = NeuralNetwork().to(device)
print(model)
loss_fn = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-4)

for epoch_num in range(1):
    for idx in range(len(x)):
        tensor_x = torch.tensor([x[idx]])
        tensor_y = torch.tensor([y[idx]])

        pred = model(tensor_x)
        loss = loss_fn(pred, tensor_y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"loss: {loss.item():>7f}")

val = float(input("Valeur ?"))
print(model(torch.tensor([val])).item())