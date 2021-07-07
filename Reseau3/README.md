In the Codes folder, you will find the different scripts that were used to retrieve our data from the database.

In the Data folder, we have grouped together all the files containing our data, and in particular the ADA_cuts_IMEI.txt file which, after processing, serves as input and validation for our neural network.
This file contains the following features:
-Cut during this slot? (0/1)
-Type of connexion (0=3G/1=Wifi)
-Day (0-6)
-Number of the Slot

reseau2.py is the code that parses our data, builds a neural network and trains it.

first, we define a custom loss, which allows us to penalize the non detection of a cut, because it is a very rare event in our database (~ 3%). There are two parameters to vary:
eps which corresponds to the accepted difference between a predicted value and the value to be predicted to assume them to be equal
rate which decides to what extent we penalize the non detection of cuts compared to the detection of a false cut.

Then, the Parser allows from our text data file, to obtain the inputs and outputs of our neural network.
Here, the inputs are the features during one slot and the output indicates whether or not there is a cut in the next slot.

Next, we divide our data set into training set and test set and normalize all the inputs.We tried to change the test set (take it at the start of the data and not at the end). This had no impact on the results.

For the structure of the network, we use layers of neurons with a linear activation function. Between each layer we add a ReLU layer. We tested many network structures (number of layers and number of neurons per layer).

For the training of our network we use the following parameters:
- optimizer: Adam
- learning rate: 1e-4
- number of epochs: 10
- batch size: 1

Results : 
You will find in the file accuracy.xsls the numerical values of the accuracy for different values of eps and rate.
Even by changing the network architecture or the parameter values, we fail to achieve satisfactory accuracy.