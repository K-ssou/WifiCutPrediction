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


def printResults(cut, resume, All_Wifi, ts, top, homeWifi, workWifi, Old_Type, Type, old_index, cur_index, cuts_file, resumes_file, DEBUG, Wifi_Leaved ):
	#APPRENTISSAGE + GROUND TRUTH
	#calcul (avant apprentissage) de la probabilite de coupure du slot old_index
	#if Wifi_Leaved[2][old_index+1]==0:
		#p_cut = float(Fraction(Wifi_Leaved[0][old_index+1], 1))
		#p_resume = Fraction(Wifi_Leaved[1][old_index+1],1)
	#else:
		#p_cut = float(Fraction(Wifi_Leaved[0][old_index+1], Wifi_Leaved[2][old_index+1]))
		#p_resume = Fraction(Wifi_Leaved[1][old_index+1], Wifi_Leaved[2][old_index+1])
	#probability de reprise du slot old_index
	#on compte le nombre de fois le slot cur_index est passe
	Wifi_Leaved[2][old_index+1]+=int(1)


	#lists the name of all APs seen in the slot
	listAPslot = []

	#on stocke les APs vus dans la liste dans listAPslot
	ajouterAPs(listAPslot,All_Wifi, ts)


	if DEBUG:
		print('List Wifi of current ts [%s]' % ', '.join(map(str, listAPslot)))
	if Old_Type==1 and Type==0:
		#CUT count nb of cuts in the slot
		cut[0]+=1

		#print   'CUT - cut = ',cut[0], 'in ts=', ts
		#on compte le nombre de coupures dans l'histogramme
		Wifi_Leaved[0][old_index+1]+=int(1)
	if Old_Type==0 and Type==1:
		#RESUME count in the slot
		resume[0]+=1 
		#on compte le nombre de reprises dans l'histogramme
		Wifi_Leaved[1][old_index+1]+=int(1)
	#on vide la liste des APs que j'ai vu 
	if (old_index != cur_index):
		if DEBUG:
			print('On a change de slot')
		#PRINT results to file

		#Get Home/Work AP
		#Home 1/0 means during the night you are covered by your work AP
		#Work 1/0 means during the day you are covered by your home AP
		[h,w]=testHomeWork(listAPslot, homeWifi, workWifi, ts)
		if DEBUG==True and h==1:
			print('Covered by Home  AP ! ')

		#Test weekday/weekend - 0:6
		we=testWeekOrWE(ts)
		if DEBUG==True and w==1:
			print('Covered by Work AP ! ')

		if cut[0]>0:
			cut_line = "1 "
			#cuts_file.write('{} '.format(1))
		else:
			cut_line = "0 "
			#cuts_file.write('{} '.format(0))
		if resume[0]>0:
			res_line = "1 "
			#resumes_file.write('{} '.format(1))
		else:
			res_line = "0 "
			#resumes_file.write('{} '.format(0))

		cut_line += "{} ".format(int(Type))
		res_line += "{} ".format(int(Type))

		#add home work
		cut_line +=  "{} ".format(float(h))
		res_line += "{} ".format(float(h))
		cut_line +=  "{} ".format(float(w))
		res_line += "{} ".format(float(w))

		#cuts_file.write('1:{} '.format(float(h)))
		#resumes_file.write('1:{} '.format(float(h)))
		#cuts_file.write('2:{} '.format(float(w)))
		#resumes_file.write('2:{} '.format(float(w)))

		#weekday/weekend - 1/0
		cut_line +=  "{} ".format(float(we))
		res_line += "{} ".format(float(we))
		#cuts_file.write('3:{} '.format(float(we)))
		#resumes_file.write('3:{} '.format(float(we)))
	
		#number of AP seen in the slot
		cut_line +=  "{} ".format(float(len(listAPslot)))
		res_line += "{} ".format(float(len(listAPslot)))
		#cuts_file.write('4:{} '.format(float(len(listAPslot))))
		#resumes_file.write('4:{} '.format(float(len(listAPslot))))

		#top one, two and three present in listAPslot
		if top[0][1] in listAPslot:
			cut_line +=  "{} ".format(float(1))
			res_line += "{} ".format(float(1))
			#cuts_file.write('5:{} '.format(float(1)))
			#resumes_file.write('5:{} '.format(float(1)))
		else:
			cut_line +=  "{} ".format(float(0))
			res_line += "{} ".format(float(0))
			#cuts_file.write('5:{} '.format(float(0)))
			#resumes_file.write('5:{} '.format(float(0)))
		if top[1][1] in listAPslot:
			cut_line +=  "{} ".format(float(1))
			res_line += "{} ".format(float(1))
			#cuts_file.write('6:{} '.format(float(1)))
			#resumes_file.write('6:{} '.format(float(1)))
		else:
			cut_line +=  "{} ".format(float(0))
			res_line += "{} ".format(float(0))
			#cuts_file.write('6:{} '.format(float(0)))
			#resumes_file.write('6:{} '.format(float(0)))
		if top[2][1] in listAPslot:
			cut_line +=  "{} ".format(float(1))
			res_line += "{} ".format(float(1))
			#cuts_file.write('7:{} '.format(float(1)))
			#resumes_file.write('7:{} '.format(float(1)))
		else:
			cut_line +=  "{} ".format(float(0))
			res_line += "{} ".format(float(0))
			#cuts_file.write('7:{} '.format(float(0)))
			#resumes_file.write('7:{} '.format(float(0)))
		#Add cur_index (index of slot between 0 and 24*4 if 15min slot duration)
		cut_line +=  "{} ".format(float(cur_index))
		res_line += "{} ".format(float(cur_index))
		#cuts_file.write('8:{} '.format(float(cur_index)))
		#resumes_file.write('8:{} '.format(float(cur_index)))

		#Add p_cut or p_resumes for cur_index
		#cut_line +=  '9:{} '.format(float(p_cut))
		#res_line += '9:{} '.format(float(p_resume))

		#cut_line += '9:{} '.format(datetime(ts))
		#res_line += '9:{} '.format(datetime(ts))
		#if cut[0]>0:
			#plot cut[0] times the line if there is a cut. 
			#for i in range(cut[0]):
			#for i in range(1):
			#	print(' cut {}'.format(cut))	
				#cuts_file.write(cut_line+'\n')
		#else: 
		cuts_file.write(cut_line+'\n')
		#if resume[0]>0:
			#for j in range(resume[0]):
			#for i in range(1):
				#resumes_file.write(res_line+'\n')
		#else:
		resumes_file.write(res_line+'\n')
		#re-init cut / resume count
		cut[0]=0
		resume[0]=0
	return


#creates a file ADA_{IMEI}.txt that lists for each slot the truth and the values of the features. 
#add into the README file the nb of slots to be used for training and the nb of slots used for prediction in the AVG algorithm
def predict(device_id, horizon, TrainingPeriod, maxPredictDays, README_filename, sharedWifiList):

	#duree de horizon*15 minutes au format daytime
	Slot = timedelta(minutes=int(horizon*15))
	#daytime qui correspond a la duree d'apprentissage
	TrainingPeriodWeek=timedelta(weeks=int(TrainingPeriod))
	#Nombre de slot max pour la training period
	TrainingPeriodNbMes=float(TrainingPeriod)*7*24*60/(horizon*15) 
	#Nb max de mesures predites 
	EndNbPredictions=maxPredictDays*24*60/(horizon*15) #interval pour mesures toutes les 5 minutes
	

	#nbSlots in one day
	Nb_Slot=int(Fraction(int(60*24),int(horizon*15)))
	
	print('Nb Slots = ',Nb_Slot)
	print('Slot duration of ',horizon*15,'min')
	print('Training period of',TrainingPeriod,' weeks ',TrainingPeriodNbMes,' measurements')
	print('EndNbPredictions of ', EndNbPredictions,' measurement and in days ', maxPredictDays)

	db=MySQLdb.connect(host="localhost",user="macacouser",passwd="rt9Ce68F",db="macacodb")
	if db is None:
		print('No db access !!')


	#Pour stocker les ssid des wifi auquel l'utilisateur s'est connecté (table connectivity)
	UsedWifi=getListUsedWifi(db, device_id)

	#retourne l'indice dans UsedWifi du reseau Wifi prefere le plus utilise le jour (8am-8pm) et la nuit (8pm-8am)
	#retourne aussi top - la liste des UsedWifi triee par ordre decroissant de frequence 
	[idDayWifi, idNightWifi, top] = getHomeWorkWifi(db, device_id, UsedWifi, 'tmp_file', sharedWifiList)
	homeWifi = UsedWifi[idNightWifi]
	workWifi = UsedWifi[idDayWifi]	

	#Scan_Wifi : retourne la liste des wifi familiers auxquels on s'est connecte : pos 0 timeslot, pos 1 wifi 
	#All-Wifi : retourne la liste de tous les wifi vus avec leur timestamp : pos 0 timeslot, pos 1 wifiname
	[Scan_Wifi, All_Wifi]=getListSeenWifi(db, device_id, UsedWifi)

	#retourne liste des entrees dans la table de connectivite pour l'imei en parametre
	#pour chaque entree, on stocke le timestamp et le Type de la table connectivite
	ConnList = getListConnectivity(db, device_id)	

	#get all measurements
	cursor_wifi = db.cursor()
	cursor_wifi.execute("""select timestamp_fire from measurements m where m.device_id='{}'""".format((device_id)))
	if cursor_wifi.rowcount > 0:
    		print('la requete Measurements a retourne 	{} mesures 	pour imei {}'.format(cursor_wifi.rowcount, device_id[0:4]))
	else:
    		print('la requete sur la table Measurements  n\'a rien renvoyé !!')

	
	#file that stores the features 
	#each line concerns one measurement slot (5 minutes or more depending on slot size)
	#file where we write all columns of features and truth: 
	# 	truth 	1:feat1 	2:feat2 	3:feat3
	# truth : boolean : cut/noCut	1/0
	# feat1 : boolean : covered by home AP	1/0
	# feat2 : boolean : covered by work AP	1/0
	# feat3 : boolean : weekday/WE	1/0
	# feat4 : integer : nbSeenAP	
	# feat5 : boolean : top1_PreferredAP 1/0 (present or not)
	# feat6 : boolean : top2_PreferredAP 1/0 (present or not)
	# feat7 : boolean : top3_PreferredAP 1/0 (present or not)
	# feat8 : integer : index of slot between 0 and 24*4 if 15min slot duration
	# feat9 : float : probability of cut / resume for this specific slot computed from past history (all history)
	
	#Dump ALL to the same file
	#cuts_train_file =  open("ADA_cuts_train_{}.txt".format(device_id[0:4]),'w')
	#resumes_train_file =  open("ADA_resumes_train_{}.txt".format(device_id[0:4]),'w')
	#cuts_test_file =  open("ADA_cuts_test_{}.txt".format(device_id[0:4]),'w')
	#resumes_test_file =  open("ADA_resumes_test_{}.txt".format(device_id[0:4]),'w')
	cuts_test_file =  open("ADA_cuts_{}.txt".format(device_id[0:4]),'w')
	resumes_test_file =  open("ADA_resumes_{}.txt".format(device_id[0:4]),'w')

	#histogram of wifi cut
	#histogramme qui stocke le nombre de coupures Wifi et l enombre de passage total dans chaque Slot
	Wifi_Leaved=[]
	Wifi_Leaved.append([int(0)]*(Nb_Slot+1))
	Wifi_Leaved[-1][0]= 'wifiCuts'
	Wifi_Leaved.append([int(0)]*(Nb_Slot+1))
	Wifi_Leaved[-1][0]= 'wifiResumes'
	Wifi_Leaved.append([int(0)]*(Nb_Slot+1))
	Wifi_Leaved[-1][0]= 'NbTimesSlotMeasured'
	#print 'Wifi Leaved [0][%s]' % ', '.join(map(str, Wifi_Leaved[0]))
	#print 'Wifi Leaved [1][%s]' % ', '.join(map(str, Wifi_Leaved[1]))
	#print 'Wifi Leaved [2][%s]' % ', '.join(map(str, Wifi_Leaved[2]))
	


	#index of old time slot
	old_index=None  
	#index courant
	cur_index=None
	found= False
	
	#index of old time slot
	old_index=None  
	#index courant
	cur_index=None
	found= False

	#current measurement date
	ts=None 
	#previous measurement date
	old_ts=None

	#Type de la connection de la mesure courante: 
	#   si 1 on a du WiFi, 
	#   si 0 on est en 3G
	Type=None
	#Type de la connection de la mesure precedente	
	Old_Type=None

	First_Date=None
	#number of measurements with valid Types (not Nones)	
	cpt=0
	#Maximum time different between two meausrement timestamps to be valid for Wifi change detection
	#Interval of 10minutes in date format - 
	dixminutes = datetime.strptime('1970-01-01T00:10:00', '%Y-%m-%dT%H:%M:%S')

	#number of predictions
	NbPredictions=0

	#nb of cuts in the current slot (set to 0 everytime there is a slot change)
	cut=[]
	resume=[]
	cut.append(0)
	resume.append(0)

	DEBUG=False

	while True:
		#print 'Measurement Nb ',cpt,'\n'
		row = cursor_wifi.fetchone()

		if First_Date is None:
			First_Date = datetime.strptime( ts2string(row[0]), '%Y-%m-%dT%H:%M:%S')
			if DEBUG:
				print('First Date : ',First_Date.strftime('%Y-%m-%dT%H:%M:%S'))
		if row is None:
			#On a lu toutes les requetes, on sort du while true
			break
		else :
			ts = row[0]
			

			#GET CONNECTION TYPE
			#verifier si le timestamp correspond a une entree dans la liste Scan_Wifi: 
			#dans ce cas, il faut mettre le type a 1 (meme s'il valait 0) 
			#car on est couvert par un WiFi habituel
			if isRegularWifi(ts, Scan_Wifi):
				Type=1
			else:
				#on cherche dans la table connection 
				#attention Type peut etre nul - dans ce cas on ne le traite pas. 
				Type=getConnectionTypeFromList(ts, ConnList)
			#time slot au format datetime
			date = ts2string(ts)
			date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
			if ((Type is not None) and (cpt>TrainingPeriodNbMes) and (date-First_Date > TrainingPeriodWeek) and (NbPredictions <= EndNbPredictions)):
				#printTS(ts)
				#Ici on est en mode prediction - 
				#print 'PREDICTION'

				for i in range(Nb_Slot):
					# on cherche le slot de la mesure en cours parmi les 4*24 slots d'une journee
					SlotInf = date.replace(hour=0, minute=0, second=0, microsecond=0)
					
					if date >= SlotInf+Slot*i and date<SlotInf+Slot*i+Slot: 
						#Avoir l'index i du slot auquel correspond la date
						cur_index = i
						
						diff = ts2string(ts-old_ts)
						diffts = datetime.strptime(diff,'%Y-%m-%dT%H:%M:%S')
						#on verifie qu'on a deux slots consecutifs 
						if diffts < dixminutes:
							NbPredictions+=int(1)
							printResults(cut, resume, All_Wifi, ts, top, homeWifi, workWifi, Old_Type, Type, old_index, cur_index, cuts_test_file, resumes_test_file, DEBUG, Wifi_Leaved )
						break #du for in range(nb_slot)


        	        	#on passe au slot suivant en se souvenant de l'ancien slot
				old_index=cur_index
				#on se souvient de l'ancien type
				Old_Type=Type	    	
				#et de l'ancien timestamp
				old_ts=ts
	
			else:
	
				if Type is not None:
					if DEBUG:
						print('APPRENTISSAGE PUR')
					#APPRENTISSAGE PUR
					# row date < training period
					if DEBUG:
						printTS(ts)


					#on trate les mesures depuis la date création de la table connectivity
					date_init = datetime.strptime('2015-05-22T00:00:00', '%Y-%m-%dT%H:%M:%S')
					if  datetime.strptime(ts2string(row[0]), '%Y-%m-%dT%H:%M:%S') > date_init:
				
						if Old_Type is None:
							Old_Type=Type
						for i in range(Nb_Slot):
							date = ts2string(ts)
							date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
							SlotInf = date.replace(hour=0, minute=0, second=0, microsecond=0)
					
							if date >= SlotInf+Slot*i and date<SlotInf+Slot*i+Slot: 
								#Avoir l'index i du slot auquel correspond la date
								cur_index = i
								if DEBUG==True:
									print('old_index ',old_index,' cur_index ', cur_index)
								
								if old_ts!=None and old_index!=None: 
									#printTS(ts-old_ts)
									diff = ts2string(ts-old_ts)
									diffts = datetime.strptime(diff,'%Y-%m-%dT%H:%M:%S')
									#on verifie qu'on a deux slots consecutifs 
									if diffts < dixminutes:
										#printResults(cut, resume, All_Wifi, ts, top, homeWifi, workWifi, Old_Type, Type, old_index, cur_index, cuts_train_file, resumes_train_file, DEBUG, Wifi_Leaved )
										#Dump all data to the test_file
										printResults(cut, resume, All_Wifi, ts, top, homeWifi, workWifi, Old_Type, Type, old_index, cur_index, cuts_test_file, resumes_test_file, DEBUG, Wifi_Leaved )
										#on compte le nb de slots utiles 
										cpt=cpt+1
                						#on passe au slot suivant en se souvenant de l'ancien slot
								old_index=cur_index
								#et de l'ancien timestamp
								old_ts=ts
								#et de l'ancien Type
								Old_Type=Type
								
								
	
								break #stop for i in range(Nb_Slot)
							
						
					else:
						print('Mesure effectuée avant création de la table connectivity')


	#********** STORE RESULTS
	print('Wifi Leaved [0][%s]' % ', '.join(map(str, Wifi_Leaved[0])))
	print('Wifi Leaved [1][%s]' % ', '.join(map(str, Wifi_Leaved[1])))
	print('Wifi Leaved [2][%s]' % ', '.join(map(str, Wifi_Leaved[2])))
 
	# README file where we write for each phone when the training stops, slot_size
	# device_id	nbTrainingSlots		nbPredictions	slot_size
	#README_file.write('IMEI, nbTrainingSlots, nbPredictionSlots,  SlotSize(minutes) \n')
	README_file = open(README_filename, 'a')
	README_file.write("{}, ".format(device_id))
	README_file.write("{}, ".format(cpt))
	README_file.write("{}, ".format(NbPredictions))
	README_file.write("{} \n".format(Slot))

	README_file.close
	#cuts_train_file.close
	cuts_test_file.close
	#resumes_train_file.close
	resumes_test_file.close


	cursor_wifi.close()

	return #end of function predict()



