import torch
from torch import nn
import numpy as np

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


IMEI = "63cdb165eda519857699323789e720c662592e869104383a4523c15198b5f510"
filename = "/home/cgilet/Reseau1/Data/ADA_cuts_{}.txt".format(IMEI[:4])

# Creating lists that will hold our input and target sequences
input_seq, target_seq = Parser(filename)

"""
for i in range(len(text)):
    # Remove last character for input sequence
    input_seq.append(text[i][:-1])

    # Remove first character for target sequence
    target_seq.append(text[i][1:])
    print("Input Sequence: {}\nTarget Sequence: {}".format(input_seq[i], target_seq[i]))
"""


def one_hot_encode(sequence, dict_size, seq_len, batch_size):
    # Creating a multi-dimensional array of zeros with the desired output shape
    features = np.zeros((batch_size, seq_len, dict_size), dtype=np.float32)

    # Replacing the 0 at the relevant character index with a 1 to represent that character
    for i in range(batch_size):
        for u in range(seq_len):
            features[i, u, sequence[i][u]] = 1
    return features


# Input shape --> (Batch Size, Sequence Length, One-Hot Encoding Size)
#input_seq = one_hot_encode(input_seq, dict_size, seq_len, batch_size)
input_seq = np.array(input_seq)
input_seq = torch.from_numpy(input_seq)
target_seq = torch.Tensor(target_seq)

# torch.cuda.is_available() checks and returns a Boolean True if a GPU is available, else it'll return False
is_cuda = torch.cuda.is_available()

# If we have a GPU available, we'll set our device to GPU. We'll use this device variable later in our code.
if is_cuda:
    device = torch.device("cuda")
    print("GPU is available")
else:
    device = torch.device("cpu")
    print("GPU not available, CPU used")


class Model(nn.Module):
    def __init__(self, input_size, output_size, hidden_dim, n_layers):
        super(Model, self).__init__()

        # Defining some parameters
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers

        # Defining the layers
        # RNN Layer
        self.rnn = nn.RNN(input_size, hidden_dim, n_layers, batch_first=True)
        # Fully connected layer
        self.fc = nn.Linear(hidden_dim, output_size)

    def forward(self, x):

        batch_size = x.size(0)

        # Initializing hidden state for first input using method defined below
        hidden = self.init_hidden(batch_size)

        # Passing in the input and hidden state into the model and obtaining outputs
        out, hidden = self.rnn(x, hidden)

        # Reshaping the outputs such that it can be fit into the fully connected layer
        out = out.contiguous().view(-1, self.hidden_dim)
        out = self.fc(out)

        return out, hidden

    def init_hidden(self, batch_size):
        # This method generates the first hidden state of zeros which we'll use in the forward pass
        # We'll send the tensor holding the hidden state to the device we specified earlier as well
        hidden = torch.zeros(self.n_layers, batch_size, self.hidden_dim)
        return hidden


# Instantiate the model with hyperparameters
model = Model(input_size=len(input_seq[0]),
              output_size=1, hidden_dim=12, n_layers=1)
# We'll also set the model to the device that we defined earlier (default is CPU)
model.to(device)

# Define hyperparameters
n_epochs = 100
lr = 0.01

# Define Loss, Optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=lr)

# Training Run
for epoch in range(1, n_epochs + 1):
    optimizer.zero_grad()  # Clears existing gradients from previous epoch
    # input_seq.to(device)
    output, hidden = model(input_seq)
    loss = criterion(output, target_seq.view(-1).long())
    loss.backward()  # Does backpropagation and calculates gradients
    optimizer.step()  # Updates the weights accordingly

    if epoch % 10 == 0:
        print("Epoch: {}/{}.............".format(epoch, n_epochs), end=" ")
        print("Loss: {:.4f}".format(loss.item()))

# This function takes in the model and character as arguments and returns the next character prediction and hidden state
"""
def predict(model, character):
    # One-hot encoding our input to fit into the model
    character = np.array([[char2int[c] for c in character]])
    character = one_hot_encode(character, dict_size, character.shape[1], 1)
    character = torch.from_numpy(character)
    character.to(device)

    out, hidden = model(character)

    prob = nn.functional.softmax(out[-1], dim=0).data
    # Taking the class with the highest probability score from the output
    char_ind = torch.max(prob, dim=0)[1].item()

    return int2char[char_ind], hidden

"""
"""
# This function takes the desired output length and input characters as arguments, returning the produced sentence
def sample(model, out_len, start="hey"):
    model.eval()  # eval mode
    start = start.lower()
    # First off, run through the starting characters
    chars = [ch for ch in start]
    size = out_len - len(chars)
    # Now pass in the previous characters and get a new one
    for ii in range(size):
        char, h = predict(model, chars)
        chars.append(char)

    return "".join(chars)


sample(model, 15, "good")
"""
