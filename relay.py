#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT) # First
GPIO.setup(25, GPIO.OUT) # Second
GPIO.setup(27, GPIO.OUT) # Third
GPIO.setup(24, GPIO.OUT) # Fourth
GPIO.setup(22, GPIO.OUT) # Fifth
GPIO.setup(17, GPIO.OUT) # last


time.sleep(1)


GPIO.output(23, 1)
GPIO.output(25, 1)
GPIO.output(27, 1)
GPIO.output(24, 1)
GPIO.output(22, 1)
GPIO.output(17, 1)

time.sleep(10)



#for x in range(1, 30):
#	print x
#	GPIO.setup(x, GPIO.OUT)
#	GPIO.output(x, 1)
#	GPIO.output(x, 0)
#	time.sleep(1)

for x in range(0, 3):

  GPIO.output(23, 1)
  time.sleep(1)
  GPIO.output(25, 1)
  time.sleep(1)
  GPIO.output(27, 1)
  time.sleep(1)
  GPIO.output(24, 1)
  time.sleep(1)
  GPIO.output(22, 1)
  time.sleep(1)
  GPIO.output(17, 1)
  time.sleep(1)

  
  
  GPIO.output(23, 0)
  time.sleep(1)
  GPIO.output(25, 0)
  time.sleep(1)
  GPIO.output(27, 0)
  time.sleep(1)
  GPIO.output(24, 0)
  time.sleep(1)
  GPIO.output(22, 0)
  time.sleep(1)
  GPIO.output(17, 0)
  time.sleep(1)
