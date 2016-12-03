#!/usr/bin/env python

execfile("functions.py")

grow_day_duration = 16
grow_night_duratin = 8
chronon = 1
debug = 1
init_time = init()

# Initiate GPIO for pigpio
pi = pigpio.pi()
# Setup the sensor
dht22 = DHT22.sensor(pi, 4) # use the actual GPIO pin name
dht22.trigger()

relay_init()


if debug:
	diff = 0

while True:
	#if debug:
	#	print diff
	#	diff += 1
	#else:
	#	diff = int(time.time() - init_time)


	temp, hum = readDHT22()
	sqlite_insert_into_sensors(str(temp), str(hum))
	print sqlite_retrieve_sensors_last_data()

	hour_of_cycle =  int(int(time.time() - init_time) / 3600)
	print "Current hour is:" + str(hour_of_cycle)
	if hour_of_cycle >= 0 and hour_of_cycle < grow_day_duration:
		print "Day!"
		sqlite_insert_into_log("Day!")
		#enable_led()

		### ENABLE WATERING ###
		### DISABLE WATERING ###
		### ENABLE LED ###

	### ENABLE COOL ###

	elif hour_of_cycle >= grow_day_duration and hour_of_cycle < grow_day_duration + grow_night_duratin:
		print "Night!"
		sqlite_insert_into_log("Night!")
		disable_led()
		### DISABLE LED ###
	else:
		print "New day!"
		sqlite_insert_into_log("New day!")
		diff = 0
		inc_day_of_grow()
		init_time = init(reset = 1)
		enable_watering()
		time.sleep(2)
		disable_watering()
		#if debug:
		break

	#time.sleep(chronon)