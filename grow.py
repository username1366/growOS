#!/usr/bin/env python

from functions import *

grow_day_duration = 2
grow_night_duration = 1
chronon = 60
debug = 1
init_time = init()
relay_init()
disable_led()
disable_cool()
disable_pump()

if debug:
	diff = 0

while True:

	temp, hum = readDHT22()
	sqlite_insert_into_sensors(str(temp), str(hum))
	print sqlite_retrieve_sensors_last_data()

	hour_of_cycle =  int(int(time.time() - init_time) / 3600)
	print "Current hour is:" + str(hour_of_cycle)

	#if mode == 'auto':
	#	pass
	#elif mode == 'manual':
	#	pass
	#else
	#	mode = 'auto'

	if hour_of_cycle >= 0 and hour_of_cycle < grow_day_duration: # DAY
		print "Day!"
		sqlite_insert_into_log("Day!")		
		enable_led()
		print "LED: enabled"
		print hour_of_cycle

	elif hour_of_cycle >= grow_day_duration and hour_of_cycle < (grow_day_duration + grow_night_duration):
		print "Night!"
		sqlite_insert_into_log("Night!")
		disable_led()	
		print "LED: disabled"
		print hour_of_cycle

	else:
		print "New day!"
		print hour_of_cycle
		sqlite_insert_into_log("New day!")
		diff = 0
		inc_day_of_grow()
		init_time = init(reset = 1)
		enable_pump()
		print "PUMP: enabled"
		time.sleep(2)
		disable_pump()		
		print "PUMP: disabled"
		#if debug:
		#break

	time.sleep(chronon)