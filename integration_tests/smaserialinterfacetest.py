#!/usr/bin/env python

"""smaserialinterfacetest.py: Queries the solar PV datalogger device on LAN or web, pulls production data and 
instructs the solarcoin daemon to make a transaction to record onto blockchain"""

__author__ = "Steven Campbell AKA Scalextrix"
__copyright__ = "Copyright 2017, Steven Campbell"
__license__ = "The Unlicense"
__version__ = "2.0"

import gc
import getpass
import mininmalmodbus
import os.path
import subprocess
import sqlite3
import sys
import time
from urllib2 import urlopen

# solarcoin passphrase must be provided for usine in subprocess.call()
solarcoin_passphrase = getpass.getpass(prompt="What is your SolarCoin Wallet Passphrase: ")

# check if user already provided system details compliant with the ELCC syntax, if not request creation and commit to db
if os.path.isfile("APIlan.db"):
	print("Found SMA Serial API database")
else:
	solarcoin_address = raw_input ("What is your SolarCoin Address: ")
	solar_panel = raw_input ("What is the Make, Model & Part Number of your solar panel: ")
	solar_inverter = raw_input ("What is the Make, Model & Part Number of your inverter: ")
	peak_watt = raw_input ("In kW (kilo-Watts), what is the peak output of your system: ")
	latitude = raw_input ("What is the Latitude of your installation: ")
	longitude = raw_input ("What is the Longitude of your installation: ")
	message = raw_input ("Add an optional message describing your system: ")
	rpi = raw_input ("If you are staking on a Raspberry Pi note the Model: ")
	conn = sqlite3.connect("APIlan.db")
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS SYSTEMDETAILS (SLRaddress TEXT, panelid TEXT, inverterid TEXT, pkwatt TEXT, lat TEXT, lon TEXT, msg TEXT, pi TEXT)''')
	c.execute("INSERT INTO SYSTEMDETAILS VALUES (?,?,?,?,?,?,?,?);", (solarcoin_address, solar_panel, solar_inverter, peak_watt, latitude, longitude, message, rpi,))
	conn.commit()		
	conn.close()

# pull from db all items
conn = sqlite3.connect("APIlan.db")
c = conn.cursor()
solarcoin_address = c.execute('select SLRaddress from SYSTEMDETAILS').fetchall()
solar_panel = c.execute('select panelid from SYSTEMDETAILS').fetchall()
solar_inverter = c.execute('select inverterid from SYSTEMDETAILS').fetchall()
peak_watt = c.execute('select pkwatt from SYSTEMDETAILS').fetchall()
latitude = c.execute('select lat from SYSTEMDETAILS').fetchall()
longitude = c.execute('select lon from SYSTEMDETAILS').fetchall()
message = c.execute('select msg from SYSTEMDETAILS').fetchall()
rpi = c.execute('select pi from SYSTEMDETAILS').fetchall()
conn.close()

# make the lists into strings
solarcoin_address = str(solarcoin_address[0][0])
solar_panel = str(solar_panel[0][0])
solar_inverter = str(solar_inverter[0][0])
peak_watt = str(peak_watt[0][0])
latitude = str(latitude[0][0])
longitude = str(longitude[0][0])
message = str(message[0][0])
rpi = str(rpi[0][0])

# load serial data - assumes SunSpec compatible register, needs work here!!!
print("Loading Serial data")
instr = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
total_energy = instr.read_register(40094, 1)
total_energy = total_energy / 1000000
print("Total Energy MWh: {:.6f}") .format(total_energy)

# Instruct SolarCoin daemon to make the blockchain post
print("Initiating SolarCoin")
energylifetime = str('Note this is all public information '+solar_panel+'; '+solar_inverter+'; '+peak_watt+'kW ;'+latitude+','+longitude+'; '+message+'; '+rpi+'; Total MWh: {}' .format(total_energy)')
print("SolarCoin TXID:")
subprocess.call(['solarcoind', 'walletlock'], shell=False)
subprocess.call(['solarcoind', 'walletpassphrase', solarcoin_passphrase, '9999999'], shell=False)
subprocess.call(['solarcoind', 'sendtoaddress', solarcoin_address, '0.000001', '', '', energylifetime], shell=False)
subprocess.call(['solarcoind', 'walletlock'], shell=False)
subprocess.call(['solarcoind', 'walletpassphrase', solarcoin_passphrase, '9999999', 'true'], shell=False)

del solarcoin_passphrase
gc.collect()
