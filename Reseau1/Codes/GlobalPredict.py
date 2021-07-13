# /usr/bin/python2 /home/cgilet/Codes/Reseau1/GlobalPredict.py /home/cgilet/Codes/Reseau1/2phones.txt ADA

# script that launches a prediction algorithm for all phones

# start script :
# python GlobalPredict.py LIST_PHONES ALGO

# listPhones that gives all IMEI values to test
# ALGO = {RND, AVERAGE, ADA}
# 	RND : Prediction_Wifi_RND.py is launched
# 	AVG : Prediction_Wifi_AVG.py

# Creates 1 files
# ALGO-X-Stat.csv lists for all phones the TP, FP, TN, FN, avg sensitivity, avg specificity
# X : duration of the prediction horizen (given in minutes)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import readPhones

# import Prediction_Wifi_AVG
import Prediction_Wifi_ADA

# import Prediction_Wifi_ADA2
# import Prediction_Wifi_HW
from fractions import Fraction

if len(sys.argv) < 3:
    print(
        "------- python GlobalPredict.py ListPhonesFile ALGO={RND, AVG, ADA} ---------"
    )
    sys.exit(0)

# read list of phones
filename = sys.argv[1]
phones = readPhones.readPhones(filename)

# algorithm
algo = sys.argv[2]

# number of 15 minutes slots that defines the horizon of prediction.
# horizons = [Fraction(1,3)]
horizons = [4]  # 1-hour slot
# horizons = [1]  # 15 min slot
# horizons = [1,4]

# AVG parameters
NbRand = [10000]
# NbRand = [1000, 10000]
# NbRand = [1000, 5000, 10000]
# NbRand = [5000]
window = [0.1, 0.2]

# ADA parameters
# List of wifi network names that are shared by a Telco - not related to a location
sharedWifiList = ["FreeWifi_secure", "SFR WiFi FON", "FreeWifi", "Livebox"]
# maximum number of days where we predict
maxPredictDays = 10000

for h in horizons:
    # if (algo=='RND'):
    # 	stat_file.write("IMEI, Sensitivity_cuts, Specificity_cuts, Sensitivity_resumes, Specificity_resumes \n")
    if algo == "AVG":
        # write column headers to files
        stat_filename = "{}-{}-Stats.csv".format(algo, h * 15)
        stat_file = open(stat_filename, "a")
        stat_file.write(
            "\nIMEI, NbRand, window, Sensitivity_cuts, Specificity_cuts, Sensitivity_resumes, Specificity_resumes \n"
        )
        stat_file.close()
        cuts_filename = "{}-{}-Stats_cuts.csv".format(algo, h * 15)
        cuts_file = open(cuts_filename, "a")
        cuts_file.write("\nIMEI, Real, TP, FP, TN, FN\n")
        cuts_file.close()
        resumes_filename = "{}-{}-Stats_resumes.csv".format(algo, h * 15)
        resumes_file = open(resumes_filename, "a")
        resumes_file.write("\nIMEI, Real, TP, FP, TN, FN\n")
        resumes_file.close()
    if algo == "HW":
        hw_filename = "Home_Work.txt"
        hw_file = open(hw_filename, "w")
        hw_file.close()
    # if (algo=='ADA' or algo=='ADA2'):
    if algo == "ADA":
        README_filename = "ADA_README.txt"
        README_file = open(README_filename, "w")
        README_file.write(
            "\nIMEI, nbTrainingSlots, nbPredictionSlots,  SlotSize(minutes) \n"
        )
        README_file.close()

    # launch algo for all phones
    for imei in phones:
        # training period in weeks : adjusted to the number of measurements stored in imei[1]
        if int(imei[1]) >= 10000:
            training = 1
        else:
            training = Fraction(int(1), int(2))

        print(
            "Compute wifi prediction for ALGO = {}, horizon = {}, training = {} w, phone = {}".format(
                algo, h, training, imei[0]
            )
        )
        # 		if (algo=='RND'):
        # 		 	Prediction_Wifi_RND.predict(imei[0], h, training, stat_filename, cuts_filename, resumes_filename)
        # if (algo=='AVG'):
        # for nbR in NbRand:
        # for w in window:
        # print('\n nbRand = ',nbR, 'and window = ', w)
        # Prediction_Wifi_AVG.predict(imei[0], h, training, maxPredictDays, stat_filename, cuts_filename, resumes_filename, nbR, w)
        if algo == "ADA":
            # Get truth and features
            Prediction_Wifi_ADA.predict(
                imei[0], h, training, maxPredictDays, README_filename, sharedWifiList
            )
            # Create tree from training set
            # Run prediction
    # 	elif (algo=='ADA2'):
    # Get truth and 2 new features (time)
    # 		Prediction_Wifi_ADA2.predict(imei[0], h, training, maxPredictDays, README_filename, sharedWifiList)
    # Create tree from training set
    # Run prediction
    # elif (algo=='HW'):
    # Prediction_Wifi_HW.predict(imei[0], h, training, hw_filename, sharedWifiList)
