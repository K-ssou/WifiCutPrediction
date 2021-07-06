This git contains all the studies carried out as well as the associated results.

AdaBoost : 
In this file, I tried to predict Wifi cuts using AdaBoost and RandomForest.
To feed the algorithm, I used the following features:
-Cut during this slot? (0/1)
-Type of connexion (0=3G/1=Wifi)
-Connected to the HomeWifi? (0/1)
-Connected to the WorkWifi? (0/1)
-Day (0-6)
-Number of Apslots
-Top 1 Wifi in list of Apslots? (0/1)
-Top 2 Wifi in list of Apslots? (0/1)
-Top 3 Wifi in list of Apslots? (0/1)
-Number of the Slot

RNN : 
As the results obtained by the different networks (1-4) are not conclusive, I tried to implement an RNN (Recurrent neural network).
The construction of the network is underway and no results are currently available.

Reseau1 : 
This network is the first that I have built to try to predict WiFi cuts.
This network takes as input all the features of a slot and must predict the probability of a cut in the next slot.
The features are as follows:
-Cut during this slot? (0/1)
-Type of connexion (0=3G/1=Wifi)
-Connected to the HomeWifi? (0/1)
-Connected to the WorkWifi? (0/1)
-Day (0-6)
-Number of Apslots
-Top 1 Wifi in list of Apslots? (0/1)
-Top 2 Wifi in list of Apslots? (0/1)
-Top 3 Wifi in list of Apslots? (0/1)
-Number of the Slot
The network architecture changed a lot during the tests.

Reseau2 : 
For this network, I used the same network as the Reseau1 but instead of giving an input slot to predict the probability of a cut in the next slot, I tried to give several measurements as input (for example the measurements i and i + 1 so that the network predicts a cut at slot i + 2)

Reseau3 :
Since the amount of data is limited, I tried to simplify the features. So in this network, the inputs are:
-Cut during this slot? (0/1)
-Type of connexion (0=3G/1=Wifi)
-Day (0-6)
-Number of the Slot

Reseau4 : 
Since our previous networks weren't able to predict cuts, we decided to change the form of the input data. Rather than indicating if there is a cut during this slot, we indicate since how many slots there have been no cuts. The objective is therefore to predict in how many slots the next cut will take place.
Features are : 
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

Reseau5 : 
For this network, we decide to add features (notably the location).
The construction of the network is underway and no results are currently available.

Accuracy.xlsx : 
In this file, you will find some results obtained for our different networks.
The different columns correspond to the different epochs of each network.

For lines, you will find the accuracy for the detection of 0s and 1s according to the different parameters.