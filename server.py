import time

from ConnectionHandler import ConnectionHandler

addr="192.168.100.23"
port = 1833
serverId="000"
topicSend = "action"
topicRecieve = "sensorData"
data={"action":"measurement",
    "sensorId":123456789}   
    #dla None dotyczy karzdy sensor #ewentualne dodatkowe klucze, wartosci

def onRecieve(data):    #TODO   przetwarzanie odebranych danych
    print(f"rec: {data}")


if __name__ == '__main__':
    conn=ConnectionHandler(serverId,addr,port,topicSend,topicRecieve,onRecieve)

    while(True):
        time.sleep(1)
        #choice=int(input("Twoj wybr: "))
        #conn.send(data)


