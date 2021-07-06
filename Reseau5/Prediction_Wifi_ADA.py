#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ourAPI import testWeekOrWE
from ourAPI import testHomeWork
from ourAPI import ajouterAPs
from ourAPI import getHomeWorkWifi
from ourAPI import ts2string
from ourAPI import isRegularWifi
from ourAPI import predictMajority
from ourAPI import getConnectionTypeFromList
from ourAPI import getListUsedWifi
from ourAPI import getListSeenWifi
from ourAPI import getListConnectivity
from ourAPI import printTS
from datetime import timedelta
from datetime import datetime
from fractions import Fraction
import MySQLdb

IMEI = "63cdb165eda519857699323789e720c662592e869104383a4523c15198b5f510"

# Connexion to the DB
db = MySQLdb.connect(
    host="localhost", user="macacouser", passwd="rt9Ce68F", db="macacodb"
)
if db is None:
    print("No db access !!")
cursor = db.cursor()

# Request
cursor.execute(
    """select timestamp, lat, lon from location l left join measurements m on m.id=l.measurement_id where m.device_id='{}'""".format(
        (IMEI))
)

# Has the request returned something?
if cursor.rowcount > 0:
    print(
        "la requete Measurements a retourne 	{} mesures 	pour imei {}".format(
            cursor.rowcount, IMEI[0:4]
        )
    )
else:
    print("la requete sur Measurments n'a rien renvoyé !!")

row = cursor.fetchone()
print(row)
