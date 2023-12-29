import paho.mqtt.client as mqttclient
from threading import *
import time
from database import send
from database import *
from database import fire_base
import random
global count
data = ''
global client

def convertTuple(tup):
    str = ''.join(tup)
    return str


def on_connect(client, userdata, flags, rc):
    print(rc)
    if rc == 0:
        print("Client is connected")
        global connected
        connected = True
    else:
        print("Connection failed")


def on_disconnect(client, userdata, rc):

    print("disconnecting reason  " + str(rc))

    #client.connected_flag = False
    #client.disconnect_flag = True


def on_message(client, userdata, message):
    global MessageReceived
    MessageReceived = True
    # print("in message")
    # print("Data" + str(message.topic) + " : " + str(message.payload.decode("utf-8")))
    # data = json.loads(message.payload)
    # print(data)
    # db.collection("mqtt").document(s["key"]).set("fasksaf")

    if connected is True:
        global data, firebase
        topic = str(message.topic)
        mes_age = str(message.payload.decode("utf-8"))
        sub = {topic: mes_age}
        if topic == "Temp/cond":
            data = ''

        for topic, message in sub.items():
            arrange = (topic, ':', mes_age)
            duplicate = convertTuple(arrange)
            dup = duplicate + '\n'
            data += dup
            taskDBMS = Thread(target=send, args=(str(message.topic), str(message.payload.decode("utf-8"))))
            taskDBMS.start()
         task = asyncio.create_task(send(str(message.topic), str(message.payload.decode("utf-8"))))

    # asyncio.run(send(str(message.topic), str(message.payload.decode("utf-8"))))


disconnect = False
connected = False
MessageReceived = False
broker_address = "driver.cloudmqtt.com"
port = 18744
user = "fqwsrtij"
password = "x`"



def connection(b, c, d, w):
    global client
    sub = ['krishna', 'joe', 'mosh', 'lal']
    name_1 = random.choice(sub)
    client = mqttclient.Client(name_1)
    client.username_pw_set(d, password=w)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.connect(b, port=c)
    client.loop_start()
    client.subscribe('#')
    while connected != True:
        time.sleep(0.2)

    while MessageReceived == True:
        time.sleep(0.2)
        client.loop_stop()


def disconnected():
    global disconnect, connected, MessageReceived
    client.disconnect()
    disconnect = False
    connected = False
    MessageReceived = False
'''
    
    try:
        name = (random.uniform(0, 1))
        address = random.uniform(2,3)
        portnum = random.uniform(4,5)
        sub = random.uniform(6, 7)
        username = random.uniform(1,6)
        passs = random.uniform(9,19)
        #dup = Thread(target=connection, args=(address, portnum, sub, username, passs))
        #dup.start()
    except:
        



'''