import PySimpleGUI as sg
from MQTT import *

global connected
global disconnect


def layout():
    layout = [[sg.Text('Name', text_color='black'), sg.InputText(pad=(5,20),size=(30,2),key='-name-'),
                   sg.Text("Address", text_color='black'), sg.InputText(size=(30, 2),key='-address-'), sg.Text('Port', text_color='black'),
                   sg.InputText(size=(30,2),key='-port-')],
                  [sg.Text('User_Name', text_color='black'), sg.InputText(pad=(3,4),size=(25,4),key='-user-'),
                   sg.Text('Password', text_color='black'), sg.InputText(pad=(1, 2), size=(30, 4),key='-password-'),
                   sg.Button('Connect', button_color=('white', 'firebrick3'), key='connect', size=(13, 1), pad=(8, 20)),
                   sg.Button('Disconnect', button_color=('white', 'firebrick3'), key='Disconnect', size=(13, 1),pad=(10, 20))],
                   [sg.Text(enable_events=True, key='status', text_color='black', size=(10, 1), pad=(1, 10)),
                   [sg.Text('Message status', text_color= 'black'),sg.Text(enable_events=True,key='status_m',text_color='black',size=(20,1)),
                   sg.ProgressBar(4, orientation='h', size=(30, 15), key='progressbar', bar_color=('Green', 'LightBlue4'))]],
                  [sg.Text("Published",text_color='black',font=('Bold',15),size=(36,1),background_color= 'azure3'),
                   sg.Text('Live_Data', background_color='azure3',text_color='black',font=('Bold',15),size=(37,1))],
                  [sg.Text(text_color=('black') ,size=(36, 19),pad=(5,3), enable_events=True, key="pub",
                           font=("Helvetica", 15),background_color='floral white'),
                   sg.Text(size=(45, 23), key='rec', font=("Helvetica", 13),background_color='floral white',text_color='black')],
                  ]

    global window
    window = sg.Window('MQTTX', layout)

    while True:
            global sub
            from MQTT import connected,data,connection,disconnect
            from MQTT import fire_base
            from database import fire_base
            event, values = window.read(timeout=1)
            if event in (sg.WIN_CLOSED, 'cancel'):
                exit()
                break
            if event in 'connect':
                try:
                    sub = ['krishna', 'joe', 'mosh', 'lal']
                    global fire_base
                    global data

                    fire_base = ''
                    data = ''
                    sub.append(values['-name-'])
                    addres_1 = values['-address-']
                    port_1 = int(values['-port-'])
                    username_1 = values['-user-']
                    password_1 = values['-password-']
                    subscribe = random.choice(sub)
                    taskConnect = Thread(target=connection, args=(addres_1, port_1, username_1, password_1))
                    taskConnect.start()
                except:
                    window['status_m'].update('check login')

            elif event in 'Disconnect':
                from MQTT import disconnect
                disconnected()


            if connected == True:
                window['status_m'].update('connected')
                if not data:
                    i = 5
                    for j in range(i):
                        time.sleep(0.4)
                        window['progressbar'].update(j)

                window['connect'].update(disabled=True)
                window['-name-'].update(disabled=True)
                window['-address-'].update(disabled=True)
                window['-port-'].update(disabled=True)
                window['-user-'].update(disabled=True)
                window['-password-'].update(disabled=True)
                window['Disconnect'].update(disabled=False)
            from MQTT import disconnect
            if connected == False :
                window['status_m'].update('disconnected')
                window['connect'].update(disabled=False)
                window['-name-'].update(disabled=False)
                window['-address-'].update(disabled=False)
                window['-port-'].update(disabled=False)
                window['-user-'].update(disabled=False)
                window['-password-'].update(disabled=False)
                window['Disconnect'].update(disabled=True)
            window['pub'].update(data)
            window['rec'].update(fire_base)


taskGUI = Thread(target=layout)
taskGUI.start()