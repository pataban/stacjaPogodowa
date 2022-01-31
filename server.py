import time
import sqlalchemy as db
import pandas as pd
import datetime

from ConnectionHandler import ConnectionHandler

addr="192.168.100.23"
port = 1833
serverId="000"
topicSend = "action"
topicRecieve = "sensorData"
dbEngine,sensors,weather=None,None,None


def getTime():
    return datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

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
    dbConn.close()

    printData(getData())
    



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
    #print(f"rec: {data}")
    
    if(not verifySensor(data["sensorId"])):
        print("User not valid")
        return

    dbConn=dbEngine.connect()
    query = db.insert(weather).values(sensorId=data["sensorId"]
        ,temp=data["temp"],hum=data["hum"],press=data["press"],date=data["date"])
    resultProxy = dbConn.execute(query)
    dbConn.close()


def printData(data):
    for i in range(0,len(data)):
        data[i]={"sensorId":data[i][0],"temp":data[i][1]
        ,"hum":data[i][2],"press":data[i][3],"date":data[i][4]}
    df=pd.DataFrame(data)
    if len(df)>0:
        print(df)
    else:
        print("No Data")


def getData(sensorId=None,tempMin=None,tempMax=None,date=None):
    query=db.select([weather])
    if(sensorId!=None):
        query=query.where(weather.columns.sensorId == sensorId)
    if(tempMin!=None and tempMax!=None):
        query=query.where(weather.columns.temp >= tempMin)
        query=query.where(weather.columns.temp < tempMax)
    if(date!=None):
        query=query.where(weather.columns.date.contains(date))
    dbConn=dbEngine.connect()
    resultProxy = dbConn.execute(query)
    res = resultProxy.fetchall()
    dbConn.close()
    return res



def menu():
    print("")
    print("Menu:")
    print("1. Przegladaj dane.")
    print("2. Ustaw alarm.")
    choice=int(input("Twoj wybr: "))
    if(choice==1):
        menuDane()
    elif(choice==2):
        menuAlarm()
    return menu()

def menuDane():
    print("")
    print("Wybor danych:")
    print("1. Wszystkie.")
    print("2. Dla danego sensora.")                 #sensorId="123456789"
    print("3. Dla danego przedzialu temperatur.")   #tempMin=21.1,tempMax=22.8
    print("4. Dla danego okresu czasu.")            #date="17.01.2022 22"
    choice=int(input("Twoj wybr: "))
    if(choice==1):
        printData(getData())
    elif(choice==2):
        printData(getData(sensorId=input("Podaj Id sensora: ")))
    elif(choice==3):
        printData(getData(tempMin=float(input("Podaj temperature minimalna: "))
        ,tempMax=float(input("Podaj temperature maksymalna: "))))
    elif(choice==4):
        printData(getData(date=input("Podaj okres: ")))
    return menu()

def menuAlarm():
    #menu
    id=str(input("Id sensora: "))
    min=float(input("Dolna granica: "))
    max=float(input("Górna granica: "))
    if max <= min:
        print("Niepoprawne granice")
        return menuAlarm()
    else:
        data={"action":"setAlarm",
        "sensorId":id,  #w przypadku pustego dotyczy każdego sensora
        "tempMin":min,
        "tempMax":max}
        conn.send(data)
        return menu()
    
    

if __name__ == '__main__':
    dbEngine,sensors,weather=openDB()
    chkDefaultSensors()
    conn=ConnectionHandler(serverId,addr,port,topicSend,topicRecieve,onRecieve)
    
    prtDB()

    #make custom data
    """dbConn=dbEngine.connect()    
    query = db.insert(weather).values(sensorId="987654321"
        ,temp="22.6",hum="90.5",press="1030.0",date=getTime())
    resultProxy = dbConn.execute(query)
    dbConn.close()"""


    while(True):
        menu()
        time.sleep(3)
        
        


