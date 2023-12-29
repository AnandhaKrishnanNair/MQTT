import json
import time
from google.cloud import firestore
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import firebase_admin
import  threading
from MQTT import *

fire_base = ''
global all_received

creds = credentials.Certificate('ServiceAccountKey.json')
firebase_admin.initialize_app(creds)

def listToString(s):
    # initialize an empty string
    str1 = " "
    return (str1.join(s))

def send(topic, value):
    global fire_base

    if topic == "Temp/cond":
        fire_base = ''

    s = datetime.now()
    sda = str(s)
    dats = {"value": value,
            "time": sda}
    x = topic.replace("/", "-")

    db = firestore.client()
    ref = db.collection("MQTT").document(x)
    ref.set({'previous': firestore.firestore.ArrayUnion([dats]),
             'livedata': (x, ':', value),
             "time": firestore.firestore.SERVER_TIMESTAMP}, merge=True)
    call_back = threading.Event()

    def on_snapshot(doc_snapshot, changes, read_time):
        global fire_base
        for doc in doc_snapshot:
            for change in changes:
                if change.type.name == 'ADDED':
                    mrx = (doc.to_dict()['livedata'])
                    data = listToString(mrx)
                    fire_base += data + '\n'
            call_back.set()

    dog_watch = ref.on_snapshot(on_snapshot)