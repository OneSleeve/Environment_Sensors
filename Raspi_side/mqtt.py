#! /usr/bin/env python

import random
from paho.mqtt import client as mqtt_client

import datetime
import MySQLdb
import requests

# Mysql Setup
mydb = MySQLdb.connect(
        host="localhost",
        user="data_feeder",
        password="smoke420",
        database="weed_sensors"
)

mycursor = mydb.cursor()

def decode_msg(msg):
    print("decode")
    data = []

    for line in msg.splitlines():
        if ":" in line:
            line = line.split(":")[1]
            data.append(line)

    moisture = data[0]
    air_temperature = data[1]
    gnd_temperature = data[2]
    pressure = data[3]
    humidity = data[4]
    co2 = data[5]
    voc = data[6]
    current_time = datetime.datetime.now().strftime("%Y_%m_%d_-_%H_%M_%S.%f")

    return (moisture, air_temperature, gnd_temperature, pressure, humidity, co2, voc, current_time)

def write_to_database(data):
    print("write")
    SQL_COMMAND = "INSERT INTO advanced_sensor_data (moisture, air_temperature, gnd_temperature, pressure, humidity, co2, voc, time_stamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"

    mycursor.execute(SQL_COMMAND,data)
    
    mydb.commit()

# MQTT Setup
broker = '192.168.177.35'
port = 1883
topic = "weed_sensors"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
username = 'weed_reader'
password = 'ERT74hjk)'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print("in msg")
        data = decode_msg(msg.payload.decode())
        write_to_database(data)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

print("run")
run()
