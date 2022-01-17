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

def getTime():
    return datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


def makeData():       #TODO pomiar danych, zwracany w tej postaci 
    data={"sensorId":123456789,
        "temp":20.5,
        "hum":66.40,
        "press":1023.1,
        "date":getTime()} 
    return data


def onRecieve(data):    #TODO wykonanie polecenia nadanego przez serwer (ustawienie alarmu)
    print(f"rec: {data}")


if __name__ == '__main__':
    conn=ConnectionHandler(sensorId,addr,port,topicSend,topicRecieve,onRecieve)

    while(True):    #TODO przesylanie danych za pomoca przyciska zamiast czekania na kolejny interwal
        data=makeData()
        conn.send(data)
        time.sleep(interval)

