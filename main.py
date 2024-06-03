from mqtt_script import MqttConnect
import time
from datetime import datetime
from random import uniform
from paho.mqtt.client import Client
import threading
from set_redis import set_data_to_redis

mq = MqttConnect()
mq.topic = ["847120588896324","588345813372649"]
stop_event = threading.Event()


    
def post_data_to_publish():
    # mq.connect_to_broker()
    while not stop_event.is_set():
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for i in mq.topic:
            rand_num = uniform(2.5, 5.2)
            cpu_temp = {"dataPoint": now, "paramType": 'cpu_temp', "paramValue": rand_num, "deviceId": i}
            # mq.data_publish(**cpu_temp)
            set_data_to_redis(expire_time=10,**cpu_temp)
        time.sleep(5)

def data_subscribe():
    mqtt_client = Client()
    mqtt_client.on_connect = mq.on_connect
    mqtt_client.on_message = mq.on_sub_message
    mqtt_client.username_pw_set(mq._username, mq._password)
    mqtt_client.connect(mq._mqttBroker, port=mq._port)
    mqtt_client.loop_start()
    try:
        while not stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        mqtt_client.loop_stop()

if __name__ == '__main__':
    try:
        pub_thread = threading.Thread(target=post_data_to_publish)
        sub_thread = threading.Thread(target=data_subscribe)
        
        pub_thread.start()
        sub_thread.start()

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping threads...")
        stop_event.set()
        pub_thread.join()
        sub_thread.join()
        print("Threads stopped.")
