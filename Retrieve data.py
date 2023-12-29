import json
import time
from google.cloud import firestore
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import firebase_admin
import  threading
from MQTT import *
from iteration_utilities import unique_everseen

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
                    testing1 = listToString(mrx)
                    print(testing1)
                    fire_base += testing1 + '\n'
            call_back.set()

    dog_watch = ref.on_snapshot(on_snapshot)


if connected == True:
    window['connect'].update(disabled=True)
    window['-name-'].update(disabled=True)
    window['-address-'].update(disabled=True)
    window['-port-'].update(disabled=True)
    window['-User-'].update(disabled=True)
    window['-Password-'].update(disabled=True)
    window['Disconnect'].update(disabled=False)
    window['status_m'].update('connected')
    if not data:
        i = 5
        for j in range(i):
            time.sleep(0.4)
            window['progressbar'].update(j)

if connected != True:
    window['connect'].update(disabled=False)
    window['-name-'].update(disabled=False)
    window['-address-'].update(disabled=False)
    window['-port-'].update(disabled=False)
    window['-User-'].update(disabled=False)
    window['-Password-'].update(disabled=False)
    window['Disconnect'].update(disabled=True)
import PySimpleGUI as sg
from MQTT import *

def layout():
    layout = [[sg.Text('Name', text_color='black'), sg.InputText(pad=(5,20),size=(30,2)),
                   sg.Text("Address", text_color='black'), sg.InputText(size=(30, 2)), sg.Text('Port', text_color='black'),
                   sg.InputText(size=(30,2))],
                  [sg.Text('User_Name', text_color='black'), sg.InputText(pad=(3,4),size=(25,4)),
                   sg.Text('Password', text_color='black'), sg.InputText(pad=(1, 2), size=(30, 4)),
                   sg.Button('Connect',button_color=('white', 'firebrick3'),key='connect', size=(15,1), pad=(25,1)),
                   sg.Text(enable_events=True,key='status',text_color='black',size=(10,1),pad=(1,10))],
                  [sg.Text('Message status', text_color= 'black'),sg.Text(enable_events=True,key='status_m',text_color='black',size=(20,1)),
                   sg.ProgressBar(4, orientation='h', size=(30, 15), key='progressbar', bar_color=('Green', 'LightBlue4'))],
                  [sg.Text("Published",text_color='black',font=('Bold',15),size=(36,1),pad=(3,0),background_color= 'azure3'),
                   sg.Text('Live_Data',pad=(3, 0), background_color='azure3',text_color='black',font=('Bold',15),size=(37,1))],
                  [sg.Text(text_color=('black') ,size=(36, 19),pad=(1,3), enable_events=True, key="pub",
                           font=("Helvetica", 15),background_color='floral white'),
                   sg.Text(size=(45, 23), key='rec', font=("Helvetica", 13),background_color='floral white',text_color='black')],
                  ]



    while True:
            from MQTT import connected,data
            from MQTT import fire_base
            from database import fire_base
            event, values = window.read(timeout=1)
            if event in (sg.WIN_CLOSED, 'cancel'):
                exit()
                break
            if event in 'connect':
                try:
                    name_1 = values[0]
                    addres_1 = values[1]
                    port_1 = int(values[2])
                    username_1 = values[3]
                    password_1 = values[4]
                    taskConnect = Thread(target=connection, args=(name_1, addres_1, port_1, username_1, password_1))
                    taskConnect.start()
                except:
                    window['status_m'].update('check login')

            if connected == True:
                window['status_m'].update('connected')
                if not data:
                    i = 5
                    for j in range(i):
                        time.sleep(0.4)
                        window['progressbar'].update(j)

            window['pub'].update(data)
            window['rec'].update(fire_base)

taskGUI = Thread(target=layout)
taskGUI.start()
import PySimpleGUI as sg
from MQTT import *

global connected
def layout():
    layout = [[sg.Text('Name', text_color='black'), sg.InputText(pad=(5,20),size=(30,2),key='-name-'),
                   sg.Text("Address", text_color='black'), sg.InputText(size=(30, 2),key='-address-'), sg.Text('Port', text_color='black'),
                   sg.InputText(size=(30,2),key='-port-')],
                  [sg.Text('User_Name', text_color='black'), sg.InputText(pad=(3,4),size=(25,4),key='-User-'),
                   sg.Text('Password', text_color='black'), sg.InputText(pad=(10, 2), size=(30, 4),key='-Password-'),
                   sg.Button('Connect',button_color=('white', 'firebrick3'),key='connect', size=(13,1), pad=(8,1)),
                   sg.Button('Disconnect', button_color=('white', 'firebrick3'), key='Disconnect', size=(13, 1), pad=(5, 1)),
                   sg.Text(enable_events=True,key='status',text_color='black',size=(10,1),pad=(1,10))],
                  [sg.Text('Message status', text_color= 'black'),sg.Text(enable_events=True,key='status_m',text_color='black',size=(20,1)),
                   sg.ProgressBar(4, orientation='h', size=(30, 15), key='progressbar', bar_color=('Green', 'LightBlue4'))],
                  [sg.Text("Published",text_color='black',font=('Bold',15),size=(40,1),pad=(3,0),background_color= 'azure3'),
                   sg.Text('Live_Data',pad=(3, 0),background_color='azure3',text_color='black',font=('Bold',15),size=(40,1))],
                  [sg.Text(text_color=('black') ,size=(40, 19),pad=(3,5), enable_events=True, key="pub",
                           font=("Helvetica", 15),background_color='floral white'),
                   sg.Text(size=(49, 23), key='rec',pad=(3,13), font=("Helvetica", 13),background_color='floral white',text_color='black')],
                  ]

    window = sg.Window('MQTTX', layout)

    while True:
            from MQTT import connected,data
            from MQTT import fire_base
            from database import fire_base
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'cancel'):
                exit()
                break
            if event in 'connect':
                try:
                    name_1 = values['-name-']
                    addres_1 = values['-address-']
                    port_1 = int(values['-port-'])
                    username_1 = values['-User-']
                    password_1 = values['-Password-']
                    taskConnect = Thread(target=connection, args=(name_1, addres_1, port_1, username_1, password_1))
                    taskConnect.start()
                except:
                    window['status_m'].update('check login')
                    '''
            if event in 'Disconnect':
                client = mqttclient.Client(values['-name-'])
                client.disconnect()
                    '''
            if connected == True:
                window['connect'].update(disabled=True)
                window['-name-'].update(disabled=True)
                window['-address-'].update(disabled=True)
                window['-port-'].update(disabled=True)
                window['-User-'].update(disabled=True)
                window['-Password-'].update(disabled=True)
                window['Disconnect'].update(disabled=False)
                window['status_m'].update('connected')
                if not data:
                    i = 5
                    for j in range(i):
                        time.sleep(0.4)
                        window['progressbar'].update(j)

            if connected != True:
                window['connect'].update(disabled=False)
                window['-name-'].update(disabled=False)
                window['-address-'].update(disabled=False)
                window['-port-'].update(disabled=False)
                window['-User-'].update(disabled=False)
                window['-Password-'].update(disabled=False)
                window['Disconnect'].update(disabled=True)

            window['pub'].update(data)
            window['rec'].update(fire_base)


taskGUI = Thread(target=layout)
taskGUI.start()

