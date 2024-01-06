import paho.mqtt.client as mqtt #import the client1
import json
import threading



def on_log(c, userdata, level, buf):
    print("log: "+buf)

 

def on_connect(c, userdata, flags, rc):
    if rc==0:
        print("connected OK")
        try:
            c.subscribe("/prod/"+c.accountId+"/"+c.subscriptionId+"/intermsg/#")
        except:
            print ("Exception  While sub in remote messages")
        c.subscribe(c.subscriptionId)  # Subscribed for Device Notifications
        payload = {"dId": c.subscriptionId,"status": True}
        c.publish("/prod/" + c.accountId + "/" +c.subscriptionId + "/status",json.dumps(payload),1,True)
        c.isConnected = True
    else:
        print("Bad connection Returned code=",rc)
        c.isConnected = False

 

def on_disconnect(c,userdata,flags,rc=0):
    print("Disconnected "+str(rc))
    c.isConnected = False

 

def on_message(c,userdata,msg):
    try:
        print(msg.payload)  
        print(msg.topic)  
        m_decode=str(msg.payload.decode("utf-8"))
        print(m_decode)
        #print(m_decode)
        data = json.loads(m_decode)
        topics = msg.topic.split("/")
        print("topics")
        print(topics)
        print("data:")
        print(data)
        vpin = 0
        print(vpin)
        if(len(topics) > 4 ):
            inTopic = topics[-2]
            if inTopic == "intermsg" :
                vpin = int(topics[-1])
        else:
            vpin = int(data['virtualPin'])

        if c.receivedMessage != None:
            c.receivedMessage(vpin,data)
    except Exception as ex:
        print(ex)

 

def connect_fail_callback(client, userdata, flags, rc):
    print("Connection failed:", rc)
    client.isConnected = True

 

class iotMQTT:
    def lpClose(c):
        payload = {"dId": c.subscriptionId,"status": False}
        c.client.publish("/prod/" + c.accountId + "/" +c.subscriptionId + "/status",json.dumps(payload),1,True)
        c.client.disconnect()
        c.client.loop_stop()

 

    def lp(c):
        # broker_address="mqtt.bariflolabs.com" #"165.22.212.69"
        broker = "4.240.114.7"
        port = 1883
        
        print("connecting to broker ",broker)
        try :
            c.client.connect_async(broker,port, keepalive=10) #connect to broker
            c.client.loop_forever()
        except :
            print("connect failed, sleeping for 10 seconds: ")
            threading.Timer(10.0,c.lp).start() # We can remove this based on DO Changes we can call this function



#{"id":"4717343766349979923","createdDate":1606092802842,"updatedDate":null,"status":"INITIAL","communicationId":"4717338695197810894","virtualPin":"1","currentState":false}

 

    def postData(c,virtualPin,state):
        msg = {"communicationId":c.subscriptionId ,"virtualPin":virtualPin,"currentState":state}
        c.post(msg)

 

    def postRemoteMsg(c,virtualPin,state):
        c.client.publish("/prod/"+c.remoteACID+"/"+c.remoteDeviceID+"/intermsg/"+virtualPin,state,1,True)

    def postDataFeed(c,dt,did):
        dt["deviceId"]= did
        dtStr = json.dumps(dt)
        c.client.publish("topic1234",dtStr)
        c.client.publish(did+"/data",dtStr) 

    def postHeartBeat(c):
        payload = {"dId": c.subscriptionId,"status": True}
        c.client.publish("/prod/" + c.accountId + "/" +c.subscriptionId + "/status",json.dumps(payload),1,True)

    def post(c,dt):
        dtStr = json.dumps(dt)
        c.client.publish("/prod/"+c.subscriptionId+"/instruction",dtStr)

    def __init__(self):
        self.client=None
        self.subscriptionId=""
        self.accountId=""
        self.remoteACID=""
        self.remoteDeviceID=""
        with open('./deviceid.json') as json_file:
            data = json.load(json_file)
            self.subscriptionId=data["deviceCommuncationId"]
            # self.accountId=data["accountId"]
        # try:
        #     self.remoteACID = data["RemoteACId"]
        #     self.remoteDeviceID = data["RemoteDeviceID"]
        # except:
        #     print("Ignore errors while loading config file")                
        self.client = mqtt.Client(self.subscriptionId) #create new instance
        self.client.subscriptionId = self.subscriptionId
        self.client.accountId = self.accountId
        self.client.remoteACID = self.remoteACID
        self.client.remoteDeviceID = self.remoteDeviceID
        self.client.receivedMessage=None
        # self.client.username_pw_set("bariflo", "Bfl@1234")
        self.client.username_pw_set("BarifloLabs", "Bfl@123")
        self.client.on_connect = on_connect
        self.client.on_log=on_log
        self.client.isConnected=False
        self.client.on_disconnect=on_disconnect
        self.client.on_message = on_message
        self.client.connect_fail_callback=connect_fail_callback
        payload = {"dId": self.subscriptionId,"status": False}
        self.client.will_set("/prod/" + self.accountId + "/"+self.subscriptionId+"/status",json.dumps(payload),1,retain=True)

