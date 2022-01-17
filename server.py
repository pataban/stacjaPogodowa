import time
import sqlalchemy as db
import pandas as pd

from ConnectionHandler import ConnectionHandler

addr="192.168.100.23"
port = 1833
serverId="000"
topicSend = "action"
topicRecieve = "sensorData"
data={"action":"measurement",
    "sensorId":123456789}   
    #dla None dotyczy karzdy sensor #ewentualne dodatkowe klucze, wartosci
dbEngine,sensors,weather=None,None,None


def openDB():
    engine = db.create_engine('sqlite:///weather.db')
    dbConnection = engine.connect()
    metadata = db.MetaData()

    sensors = db.Table('sensors', metadata,
        db.Column('id', db.String(255),nullable=False)
        )

    weather = db.Table('weather', metadata,
        db.Column('sensorId', db.String(255),nullable=False),
        db.Column('temp', db.Float(), nullable=False),
        db.Column('hum', db.Float(), nullable=False),
        db.Column('press', db.Float(), nullable=False),
        db.Column('date', db.String(255), nullable=False)
        )

    metadata.create_all(engine)
    return engine,sensors,weather


def chkDefaultSensors():    #gwarantuje istnienie sensorow 123456789 i 987654321
    dbConn=dbEngine.connect()
    query=db.select([sensors]).where(sensors.columns.id == "123456789")
    resultProxy = dbConn.execute(query)
    resultSet = resultProxy.fetchall()
    if (len(resultSet)==0):
        query = db.insert(sensors).values(id="123456789")
        resultProxy = dbConn.execute(query)

    query=db.select([sensors]).where(sensors.columns.id == "987654321")
    resultProxy = dbConn.execute(query)
    resultSet = resultProxy.fetchall()
    if (len(resultSet)==0):
        query = db.insert(sensors).values(id="987654321")
        resultProxy = dbConn.execute(query)
    dbConn.close()


def prtDB():
    dbConn=dbEngine.connect()
    query=db.select([sensors])
    resultProxy = dbConn.execute(query)
    resultSet = resultProxy.fetchall()
    print("Sensors:")
    print(resultSet)

    query=db.select([weather])
    resultProxy = dbConn.execute(query)
    resultSet = resultProxy.fetchall()
    print("Weather:")
    print(resultSet)
    dbConn.close()



def verifySensor(sensorId):
    if((sensorId=="") or (sensorId=="000")):
        return False

    dbConn=dbEngine.connect()
    query=db.select([sensors]).where(sensors.columns.id == sensorId)
    resultSet = dbConn.execute(query).fetchall()
    dbConn.close()

    if (len(resultSet)==0):
        return False
    else:
        return True



def onRecieve(data):    #uruchamiany asynchronicznie na innym watku
    print(f"rec: {data}")
    
    if(not verifySensor(data["sensorId"])):
        print("User not valid")
        return

    dbConn=dbEngine.connect()
    query = db.insert(weather).values(sensorId=data["sensorId"]
        ,temp=data["temp"],hum=data["hum"],press=data["press"],date=data["date"])
    resultProxy = dbConn.execute(query)
    dbConn.close()



if __name__ == '__main__':
    dbEngine,sensors,weather=openDB()
    chkDefaultSensors()
    conn=ConnectionHandler(serverId,addr,port,topicSend,topicRecieve,onRecieve)
    prtDB()

    while(True):
        time.sleep(1)
        #choice=int(input("Twoj wybr: "))
        #conn.send(data)


