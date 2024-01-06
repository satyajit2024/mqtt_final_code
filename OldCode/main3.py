import os
import sys
#sys.path.append('/home/pi')
import time
from threading import *
#import RPi.GPIO as GPIO
from time import sleep
import threading
from datetime import datetime
import client as c
import json
import random
from paho.mqtt.client import Client
import random_gw
mqtt = c.iotMQTT()

delay_random = 1800
last_random_off = time.time()
status = True
def doFeed():
    if __name__ == "__main__":
        threading.Timer(5.0,doFeed).start()
    with open('config.json') as json_file:
        did = json.load(json_file)
    now = time.time()
    global status
    global last_random_off
    if now - last_random_off >= delay_random:
        current1, current2 = 0,0
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current1}")
        print(f"{current2}")
        if now-delay_random - last_random_off >= delay_random:
            last_random_off = now
    else:
        if status:
            current_datetime = datetime.now()
            current1, current2 = random_gw.generate_values()
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{current1}")
            print(f"{current2}")
        else:
            current1, current2 = 0,0
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            print(current1)
            print(current2)        
    for i in did["deviceCommuncationId"]:
        if i == "661526019560586":
            mqtt.postDataFeed({"dataPoint": formatted_datetime, "paramType": 'Sensor1', "paramValue": current1},i) 
            mqtt.postDataFeed({"dataPoint": formatted_datetime, "paramType": 'Sensor2', "paramValue": current2},i)

sleep(.6)
if __name__ == "__main__":
    threading.Timer(5.0,doFeed).start()
def anotherFunction():
    broker_address = "4.240.114.7"
    broker_port = 1883
    username = "BarifloLabs"
    password = "Bfl@123"
    topics = ["661526019560586","495888677862344","910366006590890"]
    def on_connect(client, userdata, flags, rc):
            if rc == 0:
                for topic in topics:
                    client.subscribe(topic)
            else:
                pass           

    def on_message(client, userdata, message):
        global status
        data = json.loads(message.payload.decode('utf-8'))
        status = data[0]["status"]
        print(f"Received message: {data}")
        print(f"status val :---{status}")
        with open ("status.txt",'w') as f:
            f.write(str(data[0]["status"]))

    from paho.mqtt.client import Client
    while True:
        if __name__ == "__main__":
            mqtt_client = Client()
            mqtt_client.on_connect = on_connect
            mqtt_client.on_message = on_message
            mqtt_client.username_pw_set(username, password)
            mqtt_client.connect(broker_address, broker_port)
            mqtt_client.loop_start()
        try: 
            while True:
                pass
        except KeyboardInterrupt:
            mqtt_client.loop_stop()
            
if __name__ == "__main__":
    threading.Timer(5.0,anotherFunction).start()
    mqtt.lp()