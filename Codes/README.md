- test.py is just a training to remember how to create a neural network

- Reseau1 is a folder containing all data and script to make the first neural network. This network uses for each measurment of a phone the following features : 
    -There is a cut during this slot? (0/1)
    -Wich type of connection (Wifi/3G) (0/1)
    -Are we connected to the home API? (0/1)
    -Are we connected to the work API? (0/1)
    -Day of the week (0-6)
    -Number of API around us
    -Is the top1 Wifi in the API list? (0/1)
    -Is the top2 Wifi in the API list? (0/1)
    -Is the top3 Wifi in the API list? (0/1)
    -Slot time of the day (0-95)
 We give all this features for 1 measurment and the network try to predict if there is a cut during the next slot.

 - Reseau2 is the same folder but network change.
 We give him 2 consecutives measurment and it try to define if there is a cut during the third slot.

 - Reseau3 : In this network, we tried to simplify the features. We keep only features about date (day and slot), cuts and type of connection

 - RNN : We want totry with a RNN to improve the prediction. There is only a test of words prediction. Nothing to do with our project.