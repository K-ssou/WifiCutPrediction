
#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys


#creates the list of all phones from the file created by Wifi_3G_Conso_withScanWifi23.py
def readPhones(filename):
	device_id_list=[]
	f = open(filename, 'r')
	for line in f:
		bouts = line.split("\t")
		device_id_list.append((bouts[0], bouts[1])) #store IMEI + nb of mes records
	return device_id_list

filename = sys.argv[1]
device_id_list = readPhones(filename)
for elt in device_id_list: 
	print(elt)
print('Number of phones',len(device_id_list))
