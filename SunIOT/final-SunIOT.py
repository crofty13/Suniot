#!/usr/bin/python
#
# SunIOT - Dan Croft
#
# September 2017
#

#IMPORTS

import sys
import os
sys.path.append('/root/Suniot/SunIOT/SDL_Pi_SI1145');
sys.path.append('/root/Suniot/SunIOT/SDL_Pi_INA3221');
import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt                         #pip install paho-mqtt
import datetime
import SDL_Pi_SI1145                                    #for light sensor
import SDL_Pi_INA3221                                   #for SunControl Board
import json


#VARIABLES

topic = '/solardata/office'

#set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)
LED = 4
#GPIO.setup(LED, GPIO.OUT, initial=0)
sensor = SDL_Pi_SI1145.SDL_Pi_SI1145()

ina3221 = SDL_Pi_INA3221.SDL_Pi_INA3221(addr=0x40)

LIPO_BATTERY_CHANNEL = 1
SOLAR_CELL_CHANNEL   = 2
OUTPUT_CHANNEL       = 3


#FUNCTIONS

def readSunLight():

        vis = sensor.readVisible()
        IR = sensor.readIR()
        UV = sensor.readUV()
        uvIndex = UV / 100.0
        
        ##print "Sending %s" % payload
        print '		Vis:             ' + str(vis)
        print '		IR:              ' + str(IR)
        print '		UV Index:        ' + str(uvIndex)
	returnValue = []
	returnValue.append(vis)
	returnValue.append(IR)
	returnValue.append(uvIndex)
        return returnValue


def readSunControl():
  	shuntvoltage1 = 0
  	busvoltage1   = 0
  	current_mA1   = 0
  	loadvoltage1  = 0


  	busvoltage1 = ina3221.getBusVoltage_V(LIPO_BATTERY_CHANNEL)
  	shuntvoltage1 = ina3221.getShuntVoltage_mV(LIPO_BATTERY_CHANNEL)
  	# minus is to get the "sense" right.   - means the battery is charging, + that it is discharging
  	current_mA1 = ina3221.getCurrent_mA(LIPO_BATTERY_CHANNEL)  

  	loadvoltage1 = busvoltage1 + (shuntvoltage1 / 1000)
  
  	print "LIPO_Battery Bus Voltage: %3.2f V " % busvoltage1
  	print "LIPO_Battery Shunt Voltage: %3.2f mV " % shuntvoltage1
  	print "LIPO_Battery Load Voltage:  %3.2f V" % loadvoltage1
  	print "LIPO_Battery Current 1:  %3.2f mA" % current_mA1
  	print

  	shuntvoltage2 = 0
  	busvoltage2 = 0
  	current_mA2 = 0
  	loadvoltage2 = 0

  	busvoltage2 = ina3221.getBusVoltage_V(SOLAR_CELL_CHANNEL)
  	shuntvoltage2 = ina3221.getShuntVoltage_mV(SOLAR_CELL_CHANNEL)
  	current_mA2 = -ina3221.getCurrent_mA(SOLAR_CELL_CHANNEL)
  	loadvoltage2 = busvoltage2 + (shuntvoltage2 / 1000)
  
  	print "Solar Cell Bus Voltage 2:  %3.2f V " % busvoltage2
  	print "Solar Cell Shunt Voltage 2: %3.2f mV " % shuntvoltage2
  	print "Solar Cell Load Voltage 2:  %3.2f V" % loadvoltage2
  	print "Solar Cell Current 2:  %3.2f mA" % current_mA2
  	print 

  	shuntvoltage3 = 0
  	busvoltage3 = 0
  	current_mA3 = 0
  	loadvoltage3 = 0

  	busvoltage3 = ina3221.getBusVoltage_V(OUTPUT_CHANNEL)
  	shuntvoltage3 = ina3221.getShuntVoltage_mV(OUTPUT_CHANNEL)
  	current_mA3 = ina3221.getCurrent_mA(OUTPUT_CHANNEL)
  	loadvoltage3 = busvoltage3 + (shuntvoltage3 / 1000)
  
  	print "Output Bus Voltage 3:  %3.2f V " % busvoltage3
  	print "Output Shunt Voltage 3: %3.2f mV " % shuntvoltage3
  	print "Output Load Voltage 3:  %3.2f V" % loadvoltage3
  	print "Output Current 3:  %3.2f mA" % current_mA3

        #Taking only Solar values at the mo.
        returnValue = []
        returnValue.append(shuntvoltage2)
        returnValue.append(busvoltage2)
        returnValue.append(current_mA2)
        returnValue.append(loadvoltage2)
        return returnValue

def sendMSG(payload):
        date = str(datetime.datetime.now())
        #MQTT message.
    
        #finalpayload= json.dumps([{'Data':{'Date':date,'Location':'Rear Office','VisualLight':vis,'Infared':IR,'UV':UV}}], separators=(',',':'))
        payload.insert( 0, date)

        print "Final payload:"
        print(str(payload))

        #Address of MQTT server
        broker_address="192.168.0.158"

        #create new instance
        client = mqtt.Client("DansClientID2345755346")

        #create connection
        client.connect(broker_address)

        #Publish a message
        client.publish(topic=topic,payload=str(payload),qos=0)
 
        client.disconnect()


#MAIN CODE

print "-----------------"
print "SunIOT"
print ""
print "Dan Croft" 
print "-----------------"
print ""


while True:
    #Get Sunlight sensor data 
    sunSensor = []
    sunSensor = readSunLight()
    print(sunSensor[1])

    #Get Solar Panel and Battery data.
    solarSensor = []
    solarSensor = readSunControl()
    print(solarSensor[1])

    #payload
    payload = sunSensor + solarSensor
    print(payload)
    
    sendMSG(payload)






    time.sleep(10)
