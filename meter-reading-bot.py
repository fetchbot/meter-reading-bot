#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import datetime

# Zaehler-Variable, global
counter = 0	# Zaehler
stopp = 0	# Zeitpunkt steigende Flanke
start = 0	# Zeitpunkt fallende Flanke
delta = 0	# Zeitdifferenz zwischen start und stopp

# Pinreferenz waehlen
GPIO.setmode(GPIO.BCM)

# GPIO 18 (Pin 12) als Input definieren und Pullup-Widerstand aktivieren
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Callback-Funktion fuer beide Flanken
def measure(channel):
	global start
	global stopp
	global delta
	if GPIO.input(18) == 0:		# fallende Flanke, Startzeit speichern
		start = time.time()
	else:						# steigende Flanke, Endezeit speichern
		stopp = time.time()
		delta = stopp - start	# Zeitdifferenz berechnen
		print("delta = %1.2f" % delta)

# Interrupt fuer beide Flanken aktivieren
GPIO.add_event_detect(18, GPIO.BOTH, callback=measure, bouncetime=200)

try:
	while True:
		counter = counter + 1
		print "Counter %d" % counter
		time.sleep(1)

# reset GPIO settings if user presses Ctrl+C
except KeyboardInterrupt:
	GPIO.cleanup()
	print("\nBye!")
