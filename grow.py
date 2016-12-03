#!/usr/bin/env python

import time
import datetime
import json
import os.path
import sqlite3
import pigpio
import DHT22
import RPi.GPIO as GPIO

def init(reset = 0):
	if reset:
		write_init_time_file()
	if os.path.exists('day_of_grow') == False:
		create_day_of_grow_file()

	if os.path.exists('init_time'):
		init_time = read_init_time_file()
		if int(time.time() - init_time) / 3600 < 24:
			return init_time
		else:
			return write_init_time_file()
	else:
		return write_init_time_file()

def relay_init(relay_status = 0):

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(23, GPIO.OUT) # First
	GPIO.setup(25, GPIO.OUT) # Second
	GPIO.setup(27, GPIO.OUT) # Third
	GPIO.setup(24, GPIO.OUT) # Fourth
	GPIO.setup(22, GPIO.OUT) # Fifth
	GPIO.setup(17, GPIO.OUT) # last
	GPIO.output(23, relay_status)
	GPIO.output(25, relay_status)
	GPIO.output(27, relay_status)
	GPIO.output(24, relay_status)
	GPIO.output(22, relay_status)
	GPIO.output(17, relay_status)

def enable_led():
	GPIO.output(23, 1)

def enable_cool():
	GPIO.output(25, 1)

def enable_watering():
	GPIO.output(27, 1)

def disable_led():
	GPIO.output(23, 0)

def disable_cool():
	GPIO.output(25, 0)

def disable_watering():
	GPIO.output(27, 0)

def init_config():
	config = '''
	{
		"DayOfGrow": 1,
		"DayDuration": 18,
		"NightDuration": 6,
		"WateringIntensity": 4,
		"DBPath": "grow.db"
	}
	'''
	json_config = json.loads(config)
	write_config(json_config)

def read_config(config_path = 'config.json'):
	json_file = open(config_path, 'r')
	config = json_file.read()
	json_file.close()
	json_config = json.loads(config)
	return json_config

def write_config(json_config, config_path = 'config.json'):
	json_file = open(config_path, 'w')
	json_file.write(json.dumps(json_config))
	json_file.close()

def readDHT22(amount_of_trying = 3):
	while 'temp' not in locals() or 'hum' not in locals() or temp == -999 or hum == -999:
		if amount_of_trying == 0:
			sqlite_insert_into_log("Temp/Hum sensor doesn't work")
			break
		dht22.trigger()
		temp = dht22.temperature()
		hum = dht22.humidity()
		amount_of_trying -= 1
		time.sleep(2)

	return (temp, hum)

def create_day_of_grow_file():
	day_of_grow_file = open('day_of_grow', 'w')
	day_of_grow_file.write("1")
	day_of_grow_file.close()

def inc_day_of_grow():
	day_of_grow = get_day_of_grow()
	day_of_grow = str(int(day_of_grow) + 1)
	day_of_grow_file = open('day_of_grow', 'w')
	day_of_grow_file.write(day_of_grow)
	day_of_grow_file.close()

def get_day_of_grow():
	day_of_grow_file = open('day_of_grow', 'r')
	day_of_grow = day_of_grow_file.read()
	day_of_grow_file.close()
	return day_of_grow

def write_init_time_file():
	init_time_file = open('init_time', 'w')
	init_time = int(time.time())
	init_time_file.write(str(init_time))
	init_time_file.close()
	return init_time

def read_init_time_file():
	init_time_file = open('init_time', 'r')
	init_time = init_time_file.read()
	init_time = int(float(init_time))
	return init_time

def sqlite_connect():
	if not os.path.exists('grow.db'):
		connect = sqlite3.connect('grow.db')
		cursor = sqlite_init(connect)
		cursor.execute("PRAGMA busy_timeout = 900000")
		return connect, cursor
	else:
		connect = sqlite3.connect('grow.db')
		cursor = connect.cursor()
		cursor.execute("PRAGMA busy_timeout = 900000")
		return connect, cursor

def sqlite_init(connect):
	cursor = connect.cursor()
	cursor.execute("CREATE TABLE sensors (id INTEGER PRIMARY KEY, temp REAL, hum REAL, temp_sensor_status, hum_sensor_status, timestamp REAL, date DATE DEFAULT (datetime('now','localtime')))")
	cursor.execute("CREATE TABLE log (id INTEGER PRIMARY KEY, message TEXT, timestamp REAL, datetime DATE DEFAULT (datetime('now','localtime')))")
	#cursor.execute("CREATE INDEX date ON sensors (date)")
	print "All tables was created\n"
	return cursor

def sqlite_insert_into_sensors(temp, hum):
	connect, cursor = sqlite_connect()
	cursor.execute("INSERT INTO sensors (temp, hum, timestamp) VALUES (?, ?, ?)", (temp, hum, time.time()))
	connect.commit()
	connect.close()

def sqlite_insert_into_log(message):
	connect, cursor = sqlite_connect()
	cursor.execute("INSERT INTO log (message, timestamp) VALUES (?, ?)", (message, time.time()))
	connect.commit()
	connect.close()

def sqlite_retrieve_sensors_last_data():	
	connect, cursor = sqlite_connect()
	cursor.execute("SELECT max(id) FROM sensors")
	sensor_last_record_id = str(cursor.fetchall().pop(0)[0])
	cursor.execute("SELECT temp, hum, timestamp FROM sensors WHERE id = " + sensor_last_record_id)
	data = cursor.fetchall()
	data = data.pop(0)
	connect.commit()
	connect.close()
	return data[0], data[1], data[2]

def sqlite_retrieve_log_last_data(number_of_last_records = 50):	
	connect, cursor = sqlite_connect()
	cursor.execute("SELECT max(id) FROM log")
	to_id = str(cursor.fetchall().pop(0)[0])
	from_id = str(int(to_id)-number_of_last_records)
	print from_id
	print to_id
	cursor.execute("SELECT message, timestamp FROM log WHERE id > " + from_id + " AND id < " + to_id + " LIMIT 100")
	data = cursor.fetchall()
	connect.commit()
	connect.close()
	return data


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
		enable_watering()
		time.sleep(2)
		disable_watering()
		enable_led()
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
		#if debug:
		break

	time.sleep(chronon)
	





