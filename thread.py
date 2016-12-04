#!/usr/bin/env python

import time
import datetime
import json
import os.path
import sqlite3
import pigpio
import DHT22
import RPi.GPIO as GPIO

import threading

def readDHT22(amount_of_trying = 5):
	# Initiate GPIO for pigpio
	pi = pigpio.pi()
	# Setup the sensor
	dht22 = DHT22.sensor(pi, 4) # use the actual GPIO pin name
	dht22.trigger()
	while 'temp' not in locals() or 'hum' not in locals() or temp == -999 or hum == -999:
		print "DHT22 doesn work"
		if amount_of_trying == 0:
			#sqlite_insert_into_log("Temp/Hum sensor doesn't work")
			break
		dht22.trigger()
		temp = dht22.temperature()
		hum = dht22.humidity()
		amount_of_trying -= 1
		#time.sleep(2)

	print temp
	print hum
	return (temp, hum)


def test(i):
	for x in xrange(10):
		print "Thread=%d" % i
		time.sleep(1)
	return

t1 = threading.Thread(target = readDHT22, args = (5,))

t1.start()