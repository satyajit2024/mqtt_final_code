import paho.mqtt.client as mqtt

#Connection success callback
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe('testtopic/#')

# Message receiving callback
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()

# Specify callback function
client.on_connect = on_connect
client.on_message = on_message

# Establish a connection
client.username_pw_set("BarifloLabs","Bfl@12345")
client.connect('localhost', 8083, 60)
# Publish a message
client.publish('emqtt',payload='Hello World',qos=0)

client.loop_forever()