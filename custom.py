from lcu_driver import Connector
import time
import keyboard
import os
import json

#import subprocess

#subprocess.run(['pip', 'install', '-r', 'requirements.txt'], shell=True)

connector = Connector()

availability = ["chat", "online", "offline", "away", "mobile", "dnd"]

async def set_availability(connection):
    
    user = input("0 - chat\n1 - online\n2 - offline\n3 - away\n4 - mobile\n5 - in Queue/Game\n: ")
    
    availabilit = await connection.request('put', '/lol-chat/v1/me',
                                    data={'availability': availability[int(user)]})
                                    
    if(user == "2" or user == "4" or user == "5"):
        availabilit = await connection.request('put', '/lol-chat/v1/me',
                                        data={'statusMessage': ''})

    print("done")
        
    
username = ""
password = ""
async def set_status(connection):
    
    statusMessage = input("Message: ")
    
    if statusMessage == "0":
        pass
    else:
        availabilit = await connection.request('put', '/lol-chat/v1/me',
                                        data={'statusMessage': statusMessage})

    print("done")

   

async def orig_status(connection):
    global orig_status_message
    originalStatus = await connection.request('get', '/lol-chat/v1/me')
    message = await originalStatus.json()
    orig_status_message = message['statusMessage']
    
async def set_temp_status(connection):
    
    statusMessage = input("temporary Message: ")
    
    if statusMessage == "0":
        pass
    else:
        availabilit = await connection.request('put', '/lol-chat/v1/me',
                                        data={'statusMessage': statusMessage})

    print("done")
    
    
async def set_animated_status(connection):
    
    statusMessages = ["🕛", "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚"]
    
    sure = input("Animated status 1/0: ")
    
    originalStatus = await connection.request('get', '/lol-chat/v1/me')
    message = await originalStatus.json()
    status_message = message['statusMessage']
    
    if int(sure) == 1:
        i = 0
        while keyboard.is_pressed("x") == False:
            animatedstatus = await connection.request('put', '/lol-chat/v1/me',
                                    data={'statusMessage': statusMessages[i]})
            time.sleep(2)
            i += 1
            if i == len(statusMessages):
                i = 0
    
    animatedstatus = await connection.request('put', '/lol-chat/v1/me',
                        data={'statusMessage': status_message})
    print("done")
    

def login():
    sure = input("do u want to start lol and autologin(1), manual login(2) or nothing? 0/1/2: ")
    if int(sure) == 1:
        os.startfile("C:\Riot Games\League of Legends\LeagueClient.exe")
        time.sleep(5)
        keyboard.write(username)
        keyboard.press_and_release('tab')
        time.sleep(0.25)
        keyboard.write(password)
        time.sleep(0.25)
        keyboard.press_and_release('enter')
        time.sleep(10)
    elif int(sure) == 2:
        inusername = input("Username: ")
        inpassword = input("Password: ")
        os.startfile("C:\Riot Games\League of Legends\LeagueClient.exe")
        time.sleep(5)
        keyboard.write(inusername)
        keyboard.press_and_release('tab')
        time.sleep(0.25)
        keyboard.write(password)
        time.sleep(0.25)
        keyboard.press_and_release('enter')
        time.sleep(10)
    else:
        pass

login()

async def exit(connection):
    exit = input("Do you want to exit? 1: ")
    if exit == "1":
        animatedstatus = await connection.request('put', '/lol-chat/v1/me',
                    data={'statusMessage': orig_status_message})

# fired when LCU API is ready to be used
@connector.ready
async def connect(connection):
    print('LCU API is ready to be used.')

    # check if the user is already logged into his account
    summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
    if summoner.status != 200:
        print('Please login into your account to change your icon and restart the script...')
    else:
        print('Setting...')
        await orig_status(connection)
        print("my mess: " + orig_status_message)
        await set_availability(connection)
        await set_status(connection)
        await set_temp_status(connection)
        await set_animated_status(connection)
        await exit(connection)


# fired when League Client is closed (or disconnected from websocket)
@connector.close
async def disconnect(_):
    print('The client have been closed!')

# starts the connector
connector.start()