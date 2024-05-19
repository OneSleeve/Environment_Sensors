import secrets
import network
from umqtt.simple import MQTTClient
from time import sleep

mqtt_server = "192.168.177.35"
client_id = "weed_poster"

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    sleep(5)
    
    client = MQTTClient(client_id, mqtt_server, keepalive=3600, password="ERT74hjk)", user=client_id)
    client.connect()
    
    return client
    
def consturct_string(moisture, air_temperature, ground_temperature, pressure, humidity, eco2, voc):
    return f"""
Sensor_Data
moisture:{moisture}
air_temperature:{air_temperature}
ground_temperature:{ground_temperature}
pressure:{pressure}
humidity:{humidity}
eco2:{eco2}
voc:{voc}
end
"""