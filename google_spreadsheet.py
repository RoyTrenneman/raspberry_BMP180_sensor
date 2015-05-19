#!/usr/bin/python

# Google Spreadsheet BMP Sensor Data-logging 
# Depends on the libary Adafruit_BMP.BMP085
# Depends on the 'gspread' package being installed.  If you have pip installed
# execute:
#   sudo pip install gspread

import sys
import time
import datetime
import json
import Adafruit_BMP.BMP085 as BMP085
import gspread

spreadsheet_name = 'weather'

# How long to wait (in seconds) between measurements.
freq = 600 # 10 min

from oauth2client.client import SignedJwtAssertionCredentials

labeltime = 2 #cell coordinate for google spreadsheet
labeltemp = 2
labelpressure = 2

while True:
	
	#Google API (visit http://www.indjango.com/access-google-sheets-in-python-using-gspread/) 
	json_key = json.load(open('Weather-feef9f3504ab.json'))
	scope = ['https://spreadsheets.google.com/feeds']
	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
	gc = gspread.authorize(credentials)
	worksheet = gc.open(spreadsheet_name ).sheet1
	
	#Sensor reading
	bmp = BMP085.BMP085()
	temper = bmp.read_temperature()
	pressure = bmp.read_sealevel_pressure()
	roundedpressure = str((round(pressure/100, 1))).replace(".",",") # readable for google spredsheet
	roundtemp = str(temper).replace(".",",")
	
	#Update 
	try:
		maintenant = time.strftime("%d/%m/%Y %H:%M:%S")
		worksheet.update_cell(labeltime, 1, maintenant) # Update using cell coordinates
		worksheet.update_cell(labeltemp, 3, roundtemp) # Update using cell coordinates
		worksheet.update_cell(labelpressure, 2, roundedpressure) # Update using cell coordinates
		labeltemp = labeltemp + 1 
		labeltime = labeltime + 1
		labelpressure = labelpressure +1
	except:
		print 'error, logging in again'
		time.sleep(freq)
		continue

	time.sleep(freq)
