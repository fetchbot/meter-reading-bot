#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import datetime
import subprocess

# global variables
value = 0	# old meter value
start = 0	# rising edge
stopp = 0	# falling edge
delta = 0	# time delta between start and stopp, gradient

# GPIO BCM mode
GPIO.setmode(GPIO.BCM)

# GPIO 17 (Pin 11) as input with pull up for power meter
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# GPIO 18 (Pin 12) as input with pull up for gas meter
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# GPIO 27 (Pin 13) as input with pull up for water meter
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)


# callback function for ISR power meter
def ISR_power(channel):
	global start
	global stopp
	global delta
	if GPIO.input(17) == 1:
		start = time.time()		# time rising edge
	else:
		stopp = time.time()		# time falling edge
		delta = stopp - start	# calculate time difference

		print("power time delta = %1.2f" % delta)

		lastValue = 'SELECT LAST(value) from MEASUREMENT'

		lastValue = subprocess.Popen(['influx', '-username', 'USERNAME', '-password', 'PASSWORD', '-database', 'DATABASE', '-execute', lastValue], stdout=subprocess.PIPE)

		stdoutdata = lastValue.communicate()[0]
		value = int(''.join(stdoutdata.split()[6:7]))
		print "Value %d" % value

		command = 'insert MEASUREMENT,TAG_KEY1=TAG_VALUE1,TAG_KEY2=TAG_VALUE2,TAG_KEY3=TAG_VALUE3,TAG_KEY4=TAG_VALUE4 FIELD_KEY1=' + str(delta) + ',FIELD_KEY2=' + str(value+1)

		subprocess.Popen(['influx', '-username', 'USERNAME', '-password', 'PASSWORD', '-database', 'DATABASE', '-execute', command])


# callback function for ISR gas meter
def ISR_gas(channel):
	global start
	global stopp
	global delta
	if GPIO.input(18) == 1:
		start = time.time()		# time rising edge
	else:
		stopp = time.time()		# time falling edge
		delta = stopp - start	# calculate time difference

		print("gas time delta = %1.2f" % delta)

		lastValue = 'SELECT LAST(value) from MEASUREMENT'

		lastValue = subprocess.Popen(['influx', '-username', 'USERNAME', '-password', 'PASSWORD', '-database', 'DATABASE', '-execute', lastValue], stdout=subprocess.PIPE)

		stdoutdata = lastValue.communicate()[0]
		value = int(''.join(stdoutdata.split()[6:7]))
		print "Value %d" % value

		command = 'insert MEASUREMENT,TAG_KEY1=TAG_VALUE1,TAG_KEY2=TAG_VALUE2,TAG_KEY3=TAG_VALUE3,TAG_KEY4=TAG_VALUE4 FIELD_KEY1=' + str(delta) + ',FIELD_KEY2=' + str(value+1)

		subprocess.Popen(['influx', '-username', 'USERNAME', '-password', 'PASSWORD', '-database', 'DATABASE', '-execute', command])


# callback function for ISR power meter
def ISR_water(channel):
	global start
	global stopp
	global delta
	if GPIO.input(27) == 1:
		start = time.time()		# time rising edge
	else:
		stopp = time.time()		# time falling edge
		delta = stopp - start	# calculate time difference

		print("water time delta = %1.2f" % delta)

		lastValue = 'SELECT LAST(value) from MEASUREMENT'

		lastValue = subprocess.Popen(['influx', '-username', 'USERNAME', '-password', 'PASSWORD', '-database', 'DATABASE', '-execute', lastValue], stdout=subprocess.PIPE)

		stdoutdata = lastValue.communicate()[0]
		value = int(''.join(stdoutdata.split()[6:7]))
		print "Value %d" % value

		command = 'insert MEASUREMENT,TAG_KEY1=TAG_VALUE1,TAG_KEY2=TAG_VALUE2,TAG_KEY3=TAG_VALUE3,TAG_KEY4=TAG_VALUE4 FIELD_KEY1=' + str(delta) + ',FIELD_KEY2=' + str(value+1)

		subprocess.Popen(['influx', '-username', 'USERNAME', '-password', 'PASSWORD', '-database', 'DATABASE', '-execute', command])


# ISR for both edge detection
GPIO.add_event_detect(17, GPIO.BOTH, callback=ISR_power, bouncetime=100)

# ISR for both edge detection
GPIO.add_event_detect(18, GPIO.BOTH, callback=ISR_gas, bouncetime=100)

# ISR for both edge detection
GPIO.add_event_detect(27, GPIO.BOTH, callback=ISR_water, bouncetime=100)

try:
	while True:
		time.sleep(1)

# reset GPIO settings if user presses Ctrl+C
except KeyboardInterrupt:
	GPIO.cleanup()
	print("\n... smart meter readout stopped")
