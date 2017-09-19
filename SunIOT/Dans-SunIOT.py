#!/usr/bin/python
#
# SunIOT - SwitchDoc Labs
#
# October 2016
#

#IMPORTS

import sys
import os
sys.path.append('./SDL_Pi_SI1145');
import time
import RPi.GPIO as GPIO
#pip install paho-mqtt
import paho.mqtt.client as mqtt
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import SDL_Pi_SI1145

import logging
logging.basicConfig()


#VARIABLES

#set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)
LED = 4
GPIO.setup(LED, GPIO.OUT, initial=0)

sensor = SDL_Pi_SI1145.SDL_Pi_SI1145()

#FUNCTIONS

def killLogger():
    scheduler.shutdown()
    print "Scheduler Shutdown...."
    exit()


def readSunLight():
        
        #Mosquitto Broker address
        broker_address="192.168.0.158"

        #create new instance
        client = mqtt.Client("P1")

        #create connection
        client.connect(broker_address)

        vis = sensor.readVisible()
        IR = sensor.readIR()
        UV = sensor.readUV()
        uvIndex = UV / 100.0
        
        #Publish to Mosquitto
        client.publish("/danshouse/office","uv1=100,hum=50,something=500")

        print('SunLight Sensor read at time: %s' % datetime.now())
        print '		Vis:             ' + str(vis)
        print '		IR:              ' + str(IR)
        print '		UV Index:        ' + str(uvIndex)
	returnValue = []
	returnValue.append(vis)
	returnValue.append(IR)
	returnValue.append(uvIndex)
	return returnValue


print "-----------------"
print "SunIOT"
print ""
print "SwitchDoc Labs" 
print "-----------------"
print ""


if __name__ == '__main__':

    	scheduler = BackgroundScheduler()


	# DEBUG Mode - because the functions run in a separate thread, debugging can be difficult inside the functions.
	# we run the functions here to test them.
	#tick()
	#print readSunLight()
	

	# IOT Jobs are scheduled here (more coming next issue) 
	scheduler.add_job(readSunLight, 'interval', seconds=10)
	
    	# start scheduler
	scheduler.start()
	print "-----------------"
	print "Scheduled Jobs" 
	print "-----------------"
    	scheduler.print_jobs()
	print "-----------------"

    	print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    	try:
        	# This is here to simulate application activity (which keeps the main thread alive).
        	while True:
            		time.sleep(2)
    	except (KeyboardInterrupt, SystemExit):
        	# Not strictly necessary if daemonic mode is enabled but should be done if possible
        	scheduler.shutdown
