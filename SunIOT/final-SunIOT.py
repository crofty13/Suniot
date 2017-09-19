#!/usr/bin/python
#
# SunIOT - Dan Croft
#
# September 2017
#

#IMPORTS

import sys
import os
sys.path.append('/git/SunIOT/SDL_Pi_SI1145');
import time
import RPi.GPIO as GPIO
#pip install paho-mqtt
import paho.mqtt.client as mqtt
import datetime
import SDL_Pi_SI1145



#VARIABLES

#set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)
LED = 4
GPIO.setup(LED, GPIO.OUT, initial=0)
sensor = SDL_Pi_SI1145.SDL_Pi_SI1145()

#FUNCTIONS

def readSunLight():
        date = str(datetime.datetime.now())

        vis = sensor.readVisible()
        IR = sensor.readIR()
        UV = sensor.readUV()
        uvIndex = UV / 100.0
        
        #MQTT message.
        payload="%s,office,%d,%d,%d" % (date, vis, IR, UV)

        broker_address="192.168.0.158"
        #broker_address="iot.eclipse.org" #use external broker

        #create new instance
        client = mqtt.Client("P2")

        #create connection
        client.connect(broker_address)

        #Publish a message
        client.publish(topic='danshouse/office',payload=payload,qos=0)
 
        client.disconnect()

        print "sending:  %s,/danshouse/office,%d,%d,%d" % (date, vis, IR, UV)
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
print "Dan Croft" 
print "-----------------"
print ""


	# DEBUG Mode - because the functions run in a separate thread, debugging can be difficult inside the functions.
	# we run the functions here to test them.
	#tick()
	#print readSunLight()
	

	# IOT Jobs are scheduled here (more coming next issue) 
	
while True:
    readSunLight()
    time.sleep(30)
