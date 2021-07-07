In this file, you will find the codes to make a prediction using ADaBoost and Random Forest.

In AdaBoost_set1.py we use the following features:
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
We give as input a set of features corresponding to a slot to predict a cut in the next slot.

In AdaBoost_set2.py, we use the same measurements but give as input two sets of consecutive measurements (slot i and i + 1) to pre-irrigate the cut at slot i + 2.

In both cases, we obtain an accuracy of around 96%. Despite this high result, we cannot make sure that the cuts are correctly predicted since overall there is less than 4% of cuts to predict.

SET1:
AdaBoost
TrainAcc = 96.31186440677966%
TestAcc = 96.1366409109394%
RandomForest
TestAcc = 0.9516063440422936%

SET2:
AdaBoost
TrainAcc = 96.25711960943858%
TestAcc = 96.1366409109394%
RandomForest
TestAcc = 0.9605530703538023%