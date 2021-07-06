Launch : /usr/bin/python2 /home/cgilet/Codes/Reseau2/GlobalPredict.py /home/cgilet/Codes/Reseau2/2phones.txt ADA
Copy results in Data
/usr/bin/python /home/cgilet/Codes/Reseau2/reseau2.py

We used the script GlobalPredict to recover features. All the features are calculated and collected with the Prediction_Wifi_ADA.py script.
readPhones.py and ourAPI.py are functions used by the previous script.
ParserXy.py take a cut file in Data and transform it to the right format for the neural network.


Results : 
We tried many values of penalisation and epsilon but prediction is not efficient. To improve prediction we will try to change features. We simplify the features to use only date and connexion type. We change the training set too.