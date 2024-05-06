from mqtt_update import MqttConnect
import time
from datetime import datetime
from random import uniform
import json
from paho.mqtt.client import Client
import threading


mq = MqttConnect()
mq.topic = ["578689832956829","542484815423712","372582595849208"]

def post_data_to_publish():
    mq.connect_to_broker()
    while True:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for i in mq.topic:
            rand_num = uniform(2.5,5.2)
            rand_num2 = uniform(210.0 , 220.0)
            mq.data_publish({"dataPoint": now, "paramType": 'current', "paramValue": rand_num, "deviceId": i})
            mq.data_publish({"dataPoint": now, "paramType": 'voltage', "paramValue": rand_num2, "deviceId": i})
        time.sleep(5)



def data_subscribe():
    mqtt_client = Client()
    mqtt_client.on_connect = mq.on_connect
    mqtt_client.on_message = mq.on_sub_message
    mqtt_client.username_pw_set(mq._username, mq._password)
    mqtt_client.connect(mq._mqttBroker, port=mq._port)
    mqtt_client.loop_start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        mqtt_client.loop_start()


if __name__ == '__main__':
    threading.Thread(target=post_data_to_publish).start()
    threading.Thread(target=data_subscribe).start()