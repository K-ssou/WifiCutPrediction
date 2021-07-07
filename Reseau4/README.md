In the Codes folder, you will find the different scripts that were used to retrieve our data from the database.

In the Data folder, we have grouped together all the files containing our data, and in particular the ADA_cuts_IMEI.txt file which, after processing, serves as input and validation for our neural network.
This file contains the following features:
-Number of slots since the last cut?
-Type of connexion (0=3G/1=Wifi)
-Connected to the HomeWifi? (0/1)
-Connected to the WorkWifi? (0/1)
-Day (0-6)
-Number of Apslots
-Top 1 Wifi in list of Apslots? (0/1)
-Top 2 Wifi in list of Apslots? (0/1)
-Top 3 Wifi in list of Apslots? (0/1)
-Number of the Slot
We are trying to predict in how many slots there will be a new cut.

reseau2.py is the code that parses our data, builds a neural network and trains it.

This time, we do not use custom loss but the L1loss which corresponds to the absolute value of the difference between the prediction and the reality.

Then, the Parser allows from our text data file, to obtain the inputs and outputs of our neural network.
Here, the inputs are the features during one slot and the output indicates in how many slots there will be a cut. We can also do the same with more slots but it doesn't influence the results.

Next, we divide our data set into training set and test set and normalize all the inputs.

For the structure of the network, we use layers of neurons with a linear activation function. Between each layer we add a ReLU layer. We tested many network structures (number of layers and number of neurons per layer).

For the training of our network we use the following parameters:
- optimizer: Adam
- learning rate: 1e-4
- number of epochs: 20
- batch size: 1

Results : 
Accuracy oscillates throughout the learning process and we fail to reach sufficiently low values.
Even by changing the network architecture or the parameter values, we fail to achieve satisfactory accuracy.