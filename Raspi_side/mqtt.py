#! /usr/bin/env python

import random
from paho.mqtt import client as mqtt_client

import time
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

data_over_5s = []
time_for_5s = int(time.time())

def decode_msg(msg):
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
    current_time = int(time.time())

    return (moisture, air_temperature, gnd_temperature, pressure, humidity, co2, voc, current_time)

def write_to_database(data):
    data[-1] = int(time.time())
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
    global time_for_5s
    def on_message(client, userdata, msg):
        global time_for_5s
        data = decode_msg(msg.payload.decode())
        data_over_5s.append(data)

        if (int(time.time()) - time_for_5s) >= 5:
            time_for_5s = int(time.time())

            n = len(data_over_5s)
            m = len(data_over_5s[0])
            sums = [0] * m

            for subarray in data_over_5s:
                for i in range(m):
                    sums += subarray[i]

            data_to_write = [s / n for s in sums]

            write_to_database(data_to_write)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

run()
