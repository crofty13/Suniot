#!/usr/bin/python

#pip install paho-mqtt
import paho.mqtt.client as mqtt #import the client1


broker_address="192.168.0.158"
#broker_address="iot.eclipse.org" #use external broker

#create new instance
client = mqtt.Client("P1")

#create connection
client.connect(broker_address)

#Publish a message
client.publish("/danshouse/front","uv1=100,hum=50,something=500")
