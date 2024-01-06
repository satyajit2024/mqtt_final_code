import time
from threading import *
# import RPi.GPIO as GPIO
from time import sleep
import threading
from datetime import datetime
import client as c
import json
import random
from paho.mqtt.client import Client
from random import uniform , randrange


mqtt = c.iotMQTT()



# main_thread = threading.current_thread()


#IOT Data Uploading
def doFeed():
    threading.Timer(5.0,doFeed).start()
    with open('./a1.json') as json_file:
        data = json.load(json_file)
    with open('./config.json') as json_file:
        did = json.load(json_file)
    with open('./gw.json') as json_file:
        gw = json.load(json_file)
        # print(data['NodeId'])
    now = datetime.now()
    date_tm = now.strftime("%Y-%m-%d %H:%M:%S")
    randNum = uniform(1.0,2.0)
    randNum2 = uniform(1.0,2.0)

    if did['deviceCommuncationId'][0]=="661526019560586":
        mqtt.postDataFeed({"dataPoint": date_tm, "paramType": 'Sensor1', "paramValue": randNum},"661526019560586") 
        mqtt.postDataFeed({"dataPoint": date_tm, "paramType": 'Sensor2', "paramValue": randNum2},"661526019560586")

    if str(data[0]['NodeId'])==did['deviceCommuncationId'][1]:
        mqtt.postDataFeed({"dataPoint": data[0]['Sensor1_time'], "paramType": 'Sensor1', "paramValue": data[0]['Sensor1']},did['deviceCommuncationId'][1]) 
        mqtt.postDataFeed({"dataPoint": data[0]['Sensor2_time'], "paramType": 'Sensor2', "paramValue": data[0]['Sensor2']},did['deviceCommuncationId'][1])
        mqtt.postDataFeed({"dataPoint": data[0]['Sensor3_time'], "paramType": 'Sensor3', "paramValue": data[0]['Sensor3']},did['deviceCommuncationId'][1])
        mqtt.postDataFeed({"dataPoint": data[0]['Sensor4_time'], "paramType": 'Sensor4', "paramValue": data[0]['Sensor4']},did['deviceCommuncationId'][1])
        mqtt.postDataFeed({"dataPoint": data[0]['Sensor4_time'], "paramType": 'X', "paramValue": data[0]['XVal']},did['deviceCommuncationId'][1])
        mqtt.postDataFeed({"dataPoint": data[0]['Sensor4_time'], "paramType": 'Y', "paramValue": data[0]['YVal']},did['deviceCommuncationId'][1])
        mqtt.postDataFeed({"dataPoint": data[0]['Sensor4_time'], "paramType": 'Z', "paramValue": data[0]['ZVal']},did['deviceCommuncationId'][1])
    if str(data[1]['NodeId'])==did['deviceCommuncationId'][2]:
        mqtt.postDataFeed({"dataPoint": data[1]['Sensor1_time'], "paramType": 'Sensor1', "paramValue": data[1]['Sensor1']},did['deviceCommuncationId'][2]) 
        mqtt.postDataFeed({"dataPoint": data[1]['Sensor2_time'], "paramType": 'Sensor2', "paramValue": data[1]['Sensor2']},did['deviceCommuncationId'][2])
        mqtt.postDataFeed({"dataPoint": data[1]['Sensor3_time'], "paramType": 'Sensor3', "paramValue": data[1]['Sensor3']},did['deviceCommuncationId'][2])
        mqtt.postDataFeed({"dataPoint": data[1]['Sensor4_time'], "paramType": 'Sensor4', "paramValue": data[1]['Sensor4']},did['deviceCommuncationId'][2])
        mqtt.postDataFeed({"dataPoint": data[1]['Sensor4_time'], "paramType": 'X', "paramValue": data[1]['XVal']},did['deviceCommuncationId'][2])
        mqtt.postDataFeed({"dataPoint": data[1]['Sensor4_time'], "paramType": 'Y', "paramValue": data[1]['YVal']},did['deviceCommuncationId'][2])
        mqtt.postDataFeed({"dataPoint": data[1]['Sensor4_time'], "paramType": 'Z', "paramValue": data[1]['ZVal']},did['deviceCommuncationId'][2])

sleep(.6)

threading.Timer(5.0,doFeed).start()

def anotherFunction():
    broker_address = "4.240.114.7"
    broker_port = 1883
    username = "BarifloLabs"
    password = "Bfl@123"
    topics = ["topic1234"]
    def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT broker")
                for topic in topics:
                    client.subscribe(topic)
            else:
                print(f"Connection failed with code {rc}")           

    def on_message(client, userdata, message):
        # payload = message.payload.decode()
        # print(f"Received message: {payload}")
        data = json.loads(message.payload.decode('utf-8'))
        print(f"Received message: {data}")
        # from app1.models import Mqtt_device,Parameter


    from paho.mqtt.client import Client
    while True:
        mqtt_client = Client()
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        mqtt_client.username_pw_set(username, password)
        mqtt_client.connect(broker_address, broker_port)
        mqtt_client.loop_start()


        try:
            print('MQTT listener started')
            while True:
                pass
        except KeyboardInterrupt:
            mqtt_client.loop_stop()
            print('MQTT listener stopped')

threading.Timer(5.0,anotherFunction).start()


print("Both threads have finished")


mqtt.lp()




