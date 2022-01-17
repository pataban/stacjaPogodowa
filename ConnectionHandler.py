from paho.mqtt import client as mqtt
import json


class ConnectionHandler():
    def __init__(self,id,addr,port,topicSend,topicRecieve,onRecieve):
        self.id=id
        self.topicSend=topicSend
        self.topicRecieve=topicRecieve

        def on_message(client, userdata, message):
            #print("recData")
            message=str(message.payload.decode("utf-8"))
            data=json.loads(message)
            onRecieve(data)

        self.client = mqtt.Client(self.id)
        self.client.on_message=on_message
        self.client.connect(addr,port)
        self.client.loop_start()
        self.client.subscribe(self.topicRecieve)

    def send(self,data):
        data=json.dumps(data)
        print(f"send: {data}")
        self.client.publish(self.topicSend,data)



    



