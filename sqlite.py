#!/usr/bin/env python

import sqlite3
import os.path
import time


def sqlite_connect():
	if not os.path.exists('grow.db'):
		connect = sqlite3.connect('grow.db')
		cursor = connect.cursor()
		cursor.execute("PRAGMA busy_timeout = 900000")
		return connect, cursor
	else:
		print "Connected to db\n"
		connect = sqlite3.connect('grow.db')
		cursor = connect.cursor()
		cursor.execute("PRAGMA busy_timeout = 900000")
		return connect, cursor

def sqlite_init(connect):
	cursor = connect.cursor()
	cursor.execute('CREATE TABLE sensors (id INTEGER PRIMARY KEY, temp REAL, hum REAL, timestamp REAL)')
	cursor.execute('CREATE TABLE log (id INTEGER PRIMARY KEY, message TEXT, timestamp REAL)')
	print "All dbs was created\n"
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


#sqlite_insert_into_sensors('2222.122', '68')
#temp, hum, timestamp = sqlite_retrieve_sensors_last_data()
#print temp
#print hum
#print timestamp

print sqlite_retrieve_log_last_data()

#connect, cursor = sqlite_connect()
#cursor.execute("SELECT max(id) FROM sensors")
##sensor_last_record_id = str(cursor.fetchall().pop(0)[0])
#print cursor.fetchall()
#sqlite_insert_into_log('ALLAH')
#print data.pop(0)[0]