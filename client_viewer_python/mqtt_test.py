from paho.mqtt import client as mqtt_client

broker = "mqqt://192.168.177.35"
port = 1883
topic = "weed_sensors"
client_id = "weed_reader"
username = "weed_reader"
password = "ERT74hjk)"

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdate, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
        else:
            print("fuck ", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)

    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == "__main_":
    run()
