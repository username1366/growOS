#!/usr/bin/env python

from flask import Flask, render_template, request
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)

def sqlite_get_sensors_data():
  connect = sqlite3.connect('../grow.db')
  cursor = connect.cursor()
  delta = datetime.today() - timedelta(days=1)
  delta = str(delta.strftime("%Y-%m-%d %H:%M:%S"))
  today = datetime.today()
  today = str(today.strftime("%Y-%m-%d %H:%M:%S"))
  print today
  print delta
  cursor.execute("PRAGMA busy_timeout = 900000")
  #cursor.execute("SELECT temp, hum, strftime('%H:%M-%d.%m', datetime(timestamp, 'unixepoch')) FROM sensors WHERE temp != -999 and hum != -999")
  cursor.execute("SELECT temp, hum, strftime('%H:%M', datetime(timestamp, 'unixepoch')) FROM sensors WHERE date BETWEEN ? AND ? AND hum != -999 AND temp != -999", (delta, today))


  data = cursor.fetchall()
  connect.commit()
  connect.close()
  return data

#print sqlite_get_sensors_data()[0][2]

@app.route("/")
def main():
	sensors = sqlite_get_sensors_data()
	return render_template('index.html', sensors=sensors)


#@app.route("/profile/<username>")
#def profile(username):
#    return "Hey %s" % username

#@app.route("/graph", methods=['GET'])
#def index():
#	if  request.method  == 'GET':
#		return 'GET'
#	else:
#		return "Hey!"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

