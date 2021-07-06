#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import MySQLdb
import sys
import copy
from fractions import Fraction
from datetime import timedelta
from datetime import date
from datetime import datetime
import random
import operator
from operator import itemgetter

def ts2string(ts):
	dt = datetime.utcfromtimestamp(ts/1000)
	return dt.isoformat()

def SameDay(date1,date2):
	dt1 = ts2string(date1)
	dt2 = ts2string(date2)
	dt1 = datetime.strptime(dt1, '%Y-%m-%dT%H:%M:%S')
	dt2 = datetime.strptime(dt2, '%Y-%m-%dT%H:%M:%S')
	if dt1.day == dt2.day and dt1.month == dt2.month and dt1.year==dt2.year:
		return True
	else:
		return False
#fonction qui vérifie si les deux dates sont égaux( sert à savoir que c'est la méme mesure qui est envoyé mais pour differentes applications)
def SameMesure(date1,date2):
	dt1 = ts2string(date1)
	dt2 = ts2string(date2)
	dt1 = datetime.strptime(dt1, '%Y-%m-%dT%H:%M:%S')
	dt2 = datetime.strptime(dt2, '%Y-%m-%dT%H:%M:%S')
	if dt1 == dt2:
		return True
	else:
		return False

#fonction qui vérifie si un jour(date sans heure exacte) existe dans un tableau
def Date_existe(date,tab):
	for tuples in tab:
		if SameDay(date,tuples[0]):
			return True
	return False

#fonction qui vérifie si une date (avec heure exacte) existe dans tab, puis retourne l'indexe de la date dans tab
def Exact_Date_existe(date,tab,index_debut):
	dt1 = ts2string(date)
	dt1 = datetime.strptime(dt1, '%Y-%m-%dT%H:%M:%S')
	for i in range(index_debut, len(tab)):
		if SameMesure(date,tab[i][0]):
			return i
		elif datetime.strptime(ts2string(tab[i][0]), '%Y-%m-%dT%H:%M:%S')>dt1:
			return -1
	#for tuples in tab:
	#	if SameMesure(date,tuples[0]):
	#		return True
	#return False

#ajouter une nouvelle application dans l'histogramme1 ( qui cumule le trafic global de chaque application durant la training period)
def ajouter_appli_hist1(tab,AppName):
	tab.append([0]*2)
	tab[len(tab)-1][0]= AppName

#ajouter une nouvelle application dans l'histogramme2 ( qui compte le nombre d'utilisation de chaque application au réseau durant la training period)
def ajouter_appli_hist2(tab,AppName, Nb_Slot):
	tab.append([int(0)]*(Nb_Slot+1))
	tab[-1][0]= AppName



#fonction qui cherche le uid de l'appli dans un tableau et renvoie son index s'il le trouve
def Appli_existe(name,tab):
	if len(tab)==0:
		return False,-1
	if tab.count(name)>0:
		return True,tab.index(name)
	else:
		return False,-1


def SameSlot(dt1,dt2):
	if dt1.day == dt2.day and dt1.month == dt2.month and dt1.year==dt2.year and dt1.hour==dt2.hour:
		return True
	else:
		return False

#fonction qui cherche le ssid wifi dans un tableau et renvoie son index s'il le trouve, -1 sinon
def get_wifi_id(name,tab):
	if len(tab) != 0:
		i=0
		for tuples in tab:
			if name == tuples:
				break
			else:
				i +=1
		if i>=len(tab):
			return -1
		else:
			return i		
	else :
		return -1			

#fonction qui cherche le ssid wifi dans un tableau et renvoie True s'il le trouve
def wifi_existe(name,tab):
        if len(tab)==0:
                return False
        for tuples in tab:
                if name==tuples:
                        return True
        return False

#fontion qui rejoute a listAPslot tous les AP qui ont ete enregistres avec le timeslot ts.  
def ajouterAPs(listAPslot, All_Wifi, ts):
	for tuples in All_Wifi :
		if tuples[0] == ts :
			if tuples[1] not in listAPslot :
				listAPslot.append(tuples[1])
					


def getListUsedWifi(db, device_id, DEBUG=False):
#retourne un tableau qui liste les ssid des wifis auxquels l'utilisateur s'est connecté  
	
	#execute la requete sur la table connectivity
	cursor_scan = db.cursor()
	cursor_scan.execute("""select ssid from connectivity c, measurements m where c.measurement_id=m.id and m.device_id='{}' and type=1""".format((device_id)))
	if cursor_scan.rowcount > 0:
		print("la requête pour UsedWifi a renvoyé quelque chose")
	else:
		print("la requête pour UsedWifi n\'a rien renvoyé")
	
	UsedWifi =[]#Pour stocker les ssid des wifi auquel l'utilisateur s'est connecté 
	wifiname=None
	cpt=0
	while True:
		row = cursor_scan.fetchone()
		if row is None:
			if cpt==0:
				if DEBUG:
					print('Aucune mesure envoyé pour wifi ou ID mobile non existant dans MACACO SERVER')
			break
		cpt=cpt+1
		wifiname=row[0].replace('"','')
		if not wifi_existe(wifiname,UsedWifi) and wifiname is not None:
			UsedWifi.append((wifiname))
	print('nombre de UsedWifi : {}'.format(len(UsedWifi)))
	print ('[%s]' % ', '.join(map(str, UsedWifi)))
	print ('\n')
	cursor_scan.close()
	return UsedWifi



def getHomeWorkWifi(db, device_id, UsedWifi, hw_filename, sharedWifiList, DEBUG=False):
	#retourne les index du Wifi le plus souvent utilise le jour et la nuit parmi les wifi 
	#sur lequel l'utilisateur s'est connnecte
	##retourne aussi top - la liste des UsedWifi triee par ordre decroissant de frequence 

	#lance la requete sur la table wifi
	cursor_scan = db.cursor()
	cursor_scan.execute("""select timestamp_fire, w.name from wifi w, measurements m where m.id=w.measurement_id and m.device_id='{}'""".format((device_id)))
	if cursor_scan.rowcount > 0:
		print('la requête Scan WIFI a renvoyé quelque chose')
	else:
		print('la requête Scan WIFI n\'a rien renvoyé')

	
	#Autant de cases que de preferred WiFi (UsedWiFi) et enregistre dans chaque case le nombre de fois
	#ce WiFi a ete vu entre 8am et 8pm
	dayWiFi=[]
	#idem entre 8pm et 8am
	nightWiFi=[]
	for i in range(len(UsedWifi)):
		dayWiFi.append(int(0))
		nightWiFi.append(int(0))

	cpt=0
	while True:
		row = cursor_scan.fetchone()
		if row is None:
			if cpt==0:
				if DEBUG:
					print('Aucune mesure envoyé pour 3G ou ID mobile non existant dans MACACO SERVER')
			break
		date_init = datetime.strptime('2015-05-22T00:00:00', '%Y-%m-%dT%H:%M:%S')
		ts = row[0] #timeslot
		date_ts = datetime.strptime(ts2string(ts), '%Y-%m-%dT%H:%M:%S')
		if  date_ts > date_init:
			#on recupère les mesures depuis la date création de la table connectivity
			cpt=cpt+1
			wifi = row[1]
			wifi_id = get_wifi_id(wifi, UsedWifi)
			if wifi_id >=0:
				#recherche de l'id du wifi dans la table UsedWifi 
				#wifi_id vaut -1 si pas trouve
				eightAM = date_ts.replace(hour=8, minute=0, second=0, microsecond=0)
				eightPM = date_ts.replace(hour=20, minute=0, second=0, microsecond=0)
				if (date_ts >= eightAM and date_ts < eightPM):
					#Jour ! On compte le nb de fois on a vu le wifi a l'id wifi_id de jour
					dayWiFi[wifi_id] += 1
				else : 
					#Nuit !
					nightWiFi[wifi_id] += 1

	#Recherche du wifi le plus frequent qui soit different des wifi partages
	maxD = 0
	maxN = 0
	idMaxD = 0
	idMaxN = 0
	allDayWiFi = []
	toSort=[]
	for i in range(len(dayWiFi)):
		if (maxD < dayWiFi[i]) and (UsedWifi[i] not in sharedWifiList):
			print('Wifi id ', i,' and name ', UsedWifi[i])
			maxD = dayWiFi[i]
			idMaxD = i
		if (maxN < nightWiFi[i]) and (UsedWifi[i] not in sharedWifiList):
			maxN = nightWiFi[i]
			idMaxN = i
		#create histogram of all day
		toSort.append([dayWiFi[i]+nightWiFi[i], UsedWifi[i]])

	#Sort wifi by decreasing frequency for  all Day.
	res = sorted(toSort, key=itemgetter(0), reverse=True)
	print('Top AP sorted [%s]' % ', '.join(map(str, res)))
	#Remove from res the AP in sharedWifiList
	top = []
	for item in res:
		if item[1] not in sharedWifiList:
			#all element to top
			top.append(item)
	print('Top AP sorted [%s]' % ', '.join(map(str, top)))


	hw_file = open(hw_filename, 'a');
	hw_file.write("\n \n IMEI {} Home Work diff = {}".format(device_id, (idMaxN!=idMaxD))) 
	hw_file.write("\n Wifi [%s]" % ", ".join(map(str, UsedWifi))) 
	hw_file.write("\n Work [%s]" % ", ".join(map(str, dayWiFi))) 
	hw_file.write("\n Home [%s]" % ", ".join(map(str, nightWiFi))) 
	hw_file.write("\n Work {} and Home {} ".format(UsedWifi[idMaxD], UsedWifi[idMaxN]))
	hw_file.close() 

	print('dayWiFi [%s]' % ', '.join(map(str, dayWiFi)))
	print('nightWiFi [%s]' % ', '.join(map(str, nightWiFi)))
	print('max DayWiFi id = ', idMaxD, ' nom = ',UsedWifi[idMaxD])
	print('max NightWiFi id = ', idMaxN, ' nom = ',UsedWifi[idMaxN])
	print('\n')

	cursor_scan.close()

	#ATTENTION je retourne pas top - je pense qu'il ne faut pas enleve les wifi partages ici
	return [idMaxD, idMaxN, res]



def getListSeenWifi(db, device_id, UsedWifi, DEBUG=False):
#Lance une requete sur la table wifi pour lister tous les wifi vus avec la date de leur mesure
	
	#lance la requete sur la table wifi
	cursor_scan = db.cursor()
	cursor_scan.execute("""select timestamp_fire, w.name from wifi w, measurements m where m.id=w.measurement_id and m.device_id='{}'""".format((device_id)))
	if cursor_scan.rowcount > 0:
		print('la requête Scan WIFI a renvoyé quelque chose')
	else:
		print('la requête Scan WIFI n\'a rien renvoyé')

	old_ts_3g = None
	cpt=0
	#Liste de tableaux a deux elements - pour chaque element, on enregistre la date et le nom du wifi prefere de l'utilisateur
	Scan_Wifi=[]
	#liste tous les wifis vus (copie de la requete) - en position 0, on a le timestamp, en position1, le nom du wifi. 
	All_Wifi=[]
   
	while True:
		row = cursor_scan.fetchone()
		if row is None:
			if cpt==0:
				if DEBUG:
					print('Aucune mesure envoyé pour 3G ou ID mobile non existant dans MACACO SERVER')
			break
		date_init = datetime.strptime('2015-05-22T00:00:00', '%Y-%m-%dT%H:%M:%S')
		if  datetime.strptime(ts2string(row[0]), '%Y-%m-%dT%H:%M:%S') > date_init:#on recupère les mesures depuis la date création de la table connectivity
			cpt=cpt+1
			ts = row[0] #timeslot
			if old_ts_3g is None:
				old_ts_3g=ts
			if SameDay(ts,old_ts_3g):
				#on enregistre tous les wifi avec leur timestamp
				All_Wifi.append((row[0],row[1]))
				if wifi_existe(row[1],UsedWifi):
					#on ajoute le nom du SSID dans Scan_Wifi s'il est present dans la mesure
					#on ne trace pas les essid familiers vus chaque jour
					Scan_Wifi.append((row[0],row[1]))
				old_ts_3g = ts
			else:
				#On change de jour
				old_ts_3g = ts
				#del WifiAccesPoints[:]
				if wifi_existe(row[1],UsedWifi):
					Scan_Wifi.append((row[0],row[1]))
	print('nombre de seen Wifi : {}'.format(len(Scan_Wifi)))
	cursor_scan.close()
	return [Scan_Wifi, All_Wifi]



#returns true if the timestamp is stored in scan_wifi: it means the wifi is currently a preferred wifi
def isRegularWifi(ts, scan_wifi):
	for row in scan_wifi:
		if row[0]==ts:
			#print 'Regular Wifi found : ',row[1]	
			return True
	return False





#retourne liste des entrees dans la table de connectivite pour l'imei en parametre
#pour chaque entree, on stocke le timestamp et le Type de la table connectivite
def getListConnectivity(db, device_id):
	ConnList = []

	cursor_connectivity = db.cursor()
	cursor_connectivity.execute("""select timestamp_fire, type, ssid from connectivity c, measurements m where c.measurement_id=m.id and m.device_id='{}'""".format((device_id)))
	if cursor_connectivity.rowcount > 0:
    		print('la requete sur le Type de la table Connectivity a retourné 	{} 	lignes pour imei {}'.format(cursor_connectivity.rowcount, device_id[0:4]))
	else:
    		print('la requete sur la table Connectivity  n\'a rien renvoyé !!')
		
	while True:
		row = cursor_connectivity.fetchone()
		if row is not None:
			ConnList.append((row[0],row[1]))
		else:
			break
	return ConnList 


#Retourne le type de la connection (1/0) de la mesure de timestamp ts dans  de la liste conn en parametre
#S'il n'y a pas d'entree avec le timestamp ts, retourne None
def getConnectionTypeFromList(ts, conn):
	Type=None
	for row in conn:
		if row[0]==ts:
			#print 'Regular Wifi found : ',row[1]	
			return row[1]
	return Type



def printTS(ts):
	cur_ts= datetime.strptime(ts2string(ts),'%Y-%m-%dT%H:%M:%S')
	print('Cur ts :', cur_ts.strftime('%Y-%m-%dT%H:%M:%S'))

	return


	
#Return true if, knowing probability p, the random value is around p after nbRnd random throws
def predictMajority(p, nbRnd, window):
    res = False
    if p != 0:
        nb = 0
        for i in range(nbRnd):
            if random.random() < float(p):
                nb += int(1)
                continue
        if nb >= float(nbRnd * p * float(1 - window)) and nb <= float(nbRnd * p * float(1 + window)):
            res = True
    return res


def testHomeWork(listAPslot, homeWifi, workWifi, ts):
	h=0
	w=0
	#tests if we are during the day, if the user is at work by looking if he is covered by its work Wifi
	#if during the night, tests if covered by home wifi
	date_ts = datetime.strptime(ts2string(ts), '%Y-%m-%dT%H:%M:%S')
	eightAM = date_ts.replace(hour=8, minute=0, second=0, microsecond=0)
	eightPM = date_ts.replace(hour=20, minute=0, second=0, microsecond=0)
	if (date_ts >= eightAM and date_ts < eightPM):
		#Jour ! 
		if workWifi in listAPslot:
			w = 1 
	else : 
		#Nuit !
		if homeWifi in listAPslot:
			h = 1
	return [h,w]




#test if timestamp is week or weekday 
#returns number of day
def testWeekOrWE(ts):
	date_ts = datetime.strptime(ts2string(ts), '%Y-%m-%dT%H:%M:%S')
	return date_ts.date().weekday()





