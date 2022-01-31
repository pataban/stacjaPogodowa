from paho.mqtt import client as mqtt
import datetime
import json
import time

from ConnectionHandler import ConnectionHandler

addr="192.168.100.23"
port = 1833
sensorId = "123456789"  
interval=1
topicSend = "sensorData"
topicRecieve = "action"
tempMin = 21.1
tempMax = 22.8

def getTime():
    return datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


def makeData():
    data={"sensorId":123456789,
        "temp":20.5,
        "hum":66.40,
        "press":1023.1,
        "date":getTime()} 
    return data

def makeData2():
    data={"sensorId":123456789,
        "temp":21.7,
        "hum":66.21,
        "press":1023.4,
        "date":getTime()} 
    return data

def makeData3():
    data={"sensorId":123456789,
        "temp":22.4,
        "hum":65.40,
        "press":1023.5,
        "date":getTime()} 
    return data

def makeData4():
    data={"sensorId":123456789,
        "temp":23.5,
        "hum":64.97,
        "press":1022.1,
        "date":getTime()} 
    return data


def onRecieve(data):
    global tempMax
    global tempMin
    print(f"rec: {data}")
    if data.get('action') == "setAlarm":
        if data.get('sensorId') == sensorId or data.get('sensorId') == "":
            tempMax = data.get('tempMax')
            tempMin = data.get('tempMin')


def checkTemp(data):
    if data.get('temp') <= tempMin:
        print("BLUE LIGHTS ON")
    elif data.get('temp') >= tempMax:
        print("RED LIGHTS ON")
    else:
        print("ALARM LIGHTS OFF")


def afterMeasurment(data):
    checkTemp(data)  #sprawdzenie czy pomiar powinien wywołać alarm
    conn.send(data)
    time.sleep(interval)


if __name__ == '__main__':
    conn=ConnectionHandler(sensorId,addr,port,topicSend,topicRecieve,onRecieve)

    while(True):    #TODO przesylanie danych za pomoca przyciska zamiast czekania na kolejny interwal
        data=makeData()
        afterMeasurment(data)

        data=makeData2()
        afterMeasurment(data)

        data=makeData3()
        afterMeasurment(data)

        data=makeData4()
        afterMeasurment(data)



