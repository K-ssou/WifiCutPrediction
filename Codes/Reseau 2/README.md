We used the script GlobalPredict to recover features. All the features are calculated and collected with the Prediction_Wifi_ADA.py script.
readPhones.y and our API.py are functions used by the previous script.
ParserXy.py take a cut file in Data and transform it to the right format for the neural network.


Results : 
We tried many values of penalisation and epsilon but prediction is not efficient. To improve prediction we will try to change features. We simplify the features to only used date and connexion type. We change the training set too.