"""
this is a script that turns data gather from the weed
and turns in into a graph
mysql_user = "data_consumer"
passort = "high69"
"""

import mysql.connector
import matplotlib.pyplot as plt
import datetime
import numpy as np

mydb = mysql.connector.connect(
        host="192.168.177.35",
        user="data_consumer",
        password="high69",
        database="weed_sensors"
        )

mycursor = mydb.cursor()

SQL_COMMAND = "SELECT time_stamp, moisture, temperature FROM sensor_data;"

mycursor.execute(SQL_COMMAND)

data = mycursor.fetchall()

dates = []
moisture = []
temperature = []

one_week_ago = datetime.datetime.now() - datetime.timedelta(days=14)

for data_point in data:
    if datetime.datetime.strptime(data_point[0], "%Y_%m_%d_-_%H_%M_%S") > one_week_ago:
        dates.append(data_point[0])
        moisture.append(data_point[1])
        temperature.append(data_point[2])

for date in dates:
    date = datetime.datetime.strptime(date, "%Y_%m_%d_-_%H_%M_%S")

dates = np.array(dates)
moisture = np.array(moisture)
temperature = np.array(temperature)

plt.plot(dates, moisture, dates, temperature)
plt.yticks(np.arange(0, 101, step=2.5))
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))
plt.xticks(rotation=-30, ha="left", rotation_mode="anchor")
plt.grid()
plt.show()
