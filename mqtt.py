from paho.mqtt.client import Client
import json
from datetime import datetime

class MqttConnect:
    def __init__(self):
        self._connected = False
        self._client = Client("MQTT")
        self._mqttBroker = "4.240.114.7"
        self._port = 1883
        self._username = "BarifloLabs"
        self._password = "Bfl@123"
        self._client.on_connect = self.on_connect
        self._client.on_message = self.on_message
        self._client.on_log = self.log_message
        self._client.on_disconnect = self.on_disconnect
        self._client.connect_fail_callback = self.connect_fail_callback
        self.topic = ""


    def on_connect(self, client, userdata, flags, rc):
        print(f"Connection result: {rc}")
        if rc == 0:
            print("Client Is Connected")
            self._connected = True
            client.subscribe(self.topic)
        else:
            print("Connection Failed")

    def on_disconnect(self, userdata, flags, rc=0):
        print("Disconnected " + str(rc))
        self._connected = False

    def connect_fail_callback(self, userdata, flags, rc):
        print("Connection failed:", rc)
        self._connected = False

    def log_message(self, message):
        print("log: " + message)
        try:
            with open("mqtt_logs.log", "a") as log_file:
                log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        except Exception as e:
            print(f"Error writing to log file: {e}")

    def on_message(self, client, userdata, message):
        self.log_message("Received message: " + str(message.payload.decode("utf-8")))

    def connect_to_broker(self):
        try:
            self._client.username_pw_set(self._username, self._password)
            self._client.connect(self._mqttBroker, port=self._port)
            self._client.loop_start()
        except Exception as e:
            print(f"Error during connection: {e}")

    def data_publish(self, publish_data):
        if not self._connected:
            self.log_message("Not connected to the broker.")
            return

        publish_topic = self.topic
        publish_data = json.dumps(publish_data)
        self._client.publish(publish_topic + "/data", publish_data)
        self.log_message(f"Just published {str(publish_data)} to {publish_topic}")
    
    def on_sub_message(self , client, userdata, message):
        global status
        data = json.loads(message.payload.decode('utf-8'))
        status = data[0]["status"]
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        topic = message.topic
        print(f"Received message: {data}")
        print(f"status val :---{status}")
        with open("status.txt", 'a') as f:
            f.write(f"{current_time} - Status: {status}, Topic: {topic}\n")
    
    def open_file(self , file_name):
        if file_name.lower().endswith(".json"):
            with open(file_name) as json_file:
                data = json.load(json_file)
            return data


