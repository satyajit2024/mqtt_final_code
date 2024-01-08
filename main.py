from mqtt import MqttConnect
import time
from datetime import datetime
from random import uniform
import json
from paho.mqtt.client import Client
import threading
from main import MqttConnect



mq = MqttConnect()
mq.topic = "661526019560586"
mqttBroker = "4.240.114.7"
port = 1883
username = "BarifloLabs"
password = "Bfl@123"


def post_data_to_publish():
    mq.connect_to_broker()
    while True:
        rand_num = uniform(1.0, 2.0)
        rand_num2 = uniform(1.0, 2.0)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        mq.data_publish({"dataPoint": now, "paramType": 'Sensor1', "paramValue": rand_num, "deviceId": mq.topic})
        mq.data_publish({"dataPoint": now, "paramType": 'Sensor2', "paramValue": rand_num2, "deviceId": mq.topic})
        time.sleep(1)


def data_subscribe():
    mqtt_client = Client()
    mqtt_client.on_connect = mq.on_connect
    mqtt_client.on_message = mq.on_sub_message
    mqtt_client.username_pw_set(username, password)
    mqtt_client.connect(mqttBroker, port=port)
    mqtt_client.loop_start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        mqtt_client.loop_start()


if __name__ == '__main__':
    t1 = threading.Thread(target=post_data_to_publish)
    t2 = threading.Thread(target=data_subscribe)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    
    