"""
this module is used to request things from the web
mysql_user = "data_feeder"
password = "smoke420"
"""

import datetime
import MySQLdb
import requests
from bs4 import BeautifulSoup

request = requests.get('http://192.168.177.36/', timeout=10)

soup = BeautifulSoup(request.content, 'html.parser')

for content in soup.select('p'):
    print(content.text)

raw_moisture = float(soup.select('p')[1].text)
# 53200 is the sensors max and 100 is the max percentile
moisture = int((raw_moisture * 100) / 53200)

temperature_in_c = float(soup.select('p')[3].text) - 4

current_time = datetime.datetime.now().strftime("%Y_%m_%d_-_%H_%M_%S")

mydb = MySQLdb.connect(
        host="localhost",
        user="data_feeder",
        password="smoke420",
        database="weed_sensors"
        )

mycursor = mydb.cursor()

SQL_COMMAND = "INSERT INTO sensor_data (moisture, temperature, time_stamp) VALUES (%s, %s, %s);"
val = (moisture, temperature_in_c, current_time)

mycursor.execute(SQL_COMMAND,val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")
