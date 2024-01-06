import paho.mqtt.client as mqtt
from random import uniform
import time
from paho.mqtt.client import Client
import json
from datetime import datetime

class MqttConnect:
    def __init__(self):
        self._connected = False
        self._client = mqtt.Client("MQTT")
        self._mqttBroker = "4.240.114.7"
        self._port = 1883
        self._username = "BarifloLabs"  
        self._password = "Bfl@123"
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.on_log=self._log_message
        self._client.on_disconnect=self._on_disconnect
        self._client.connect_fail_callback=self._connect_fail_callback
        self.topic = "661526019560586"
    
    def _on_disconnect(self,userdata,flags,rc=0):
        print("Disconnected "+str(rc))
        self._connected = False

    def _connect_fail_callback(client, userdata, flags, rc):
        print("Connection failed:", rc)
        client.isConnected = True

    def _log_message(self,message):
        print("log: "+message)
        with open("mqtt_logs.log", "a") as log_file:
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")


    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Client Is Connected")
            self._connected = True
        else:
            print("Connection Failed")


    def _on_message(self, client, userdata, message):
        self._log_message("Received message: " + str(message.payload.decode("utf-8")))


    def connect_to_broker(self):
        self._client.username_pw_set(self._username, self._password)
        self._client.connect(self._mqttBroker, port=self._port)


    def _data_publish(self, publish_data):
        # if self._connected is False:
        #     self._log_message("Not connected to the broker.")
        #     return

        publish_topic = self.topic
        publish_data = json.dumps(publish_data)
        self._client.publish(publish_topic + "/data", publish_data)
        self._log_message(f"Just published {str(publish_data)} to {publish_topic}")


    def post_data_to_publish(self):
        self.connect_to_broker()

        while True:
            randNum = uniform(1.0, 2.0)
            randNum2 = uniform(1.0, 2.0)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self._data_publish({"dataPoint": now, "paramType": 'Sensor1', "paramValue": randNum, "deviceId": self.topic})
            self._data_publish({"dataPoint": now, "paramType": 'Sensor2', "paramValue": randNum2, "deviceId": self.topic})
            time.sleep(1)



    def data_subscribe(self):
        def on_sub_connect(client, userdata, flags, rc):
            if rc == 0:
                client.subscribe("661526019560586/data")
            else:
                pass 


        def on_sub_message(client, userdata, message):
            global status
            data = json.loads(message.payload.decode('utf-8'))
            status = data[0]["status"]
            print(f"Received message: {data}")
            print(f"status val :---{status}")
            with open ("status.txt",'w') as f:
                f.write(str(data[0]["status"]))
                
        while True:
            if __name__ == "__main__":
                mqtt_client = Client()
                mqtt_client.on_connect = on_sub_connect
                mqtt_client.on_message = on_sub_message
                mqtt_client.username_pw_set(self._username, self._password)
                mqtt_client.connect(self._mqttBroker, self._port)
                mqtt_client.loop_start()
            try: 
                while True:
                    pass
            except KeyboardInterrupt:
                mqtt_client.loop_stop()

    






