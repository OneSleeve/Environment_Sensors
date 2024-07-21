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

SQL_COMMAND = "SELECT * FROM advanced_sensor_data;"

mycursor.execute(SQL_COMMAND)

data = mycursor.fetchall()

moisture = []
air_temperature = []
gnd_temperature = []
pressure = []
humidity = []
co2 = []
voc = []
time_stamps = []

temp_moisture = []
temp_air_temperature = []
temp_gnd_temperature = []
temp_pressure = []
temp_humidity = []
temp_co2 = []
temp_voc = []

one_week_ago = datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=2)

current_second = datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=2)

for index in range(len(data) - 1):
    data_point = data[index]
    if datetime.datetime.strptime(data_point[7], "%Y_%m_%d_-_%H_%M_%S.%f") > one_week_ago:
        print(datetime.datetime.strptime(data_point[7],"%Y_%m_%d_-_%H_%M_%S.%f").replace(microsecond=0), current_second)
        if datetime.datetime.strptime(data_point[7],"%Y_%m_%d_-_%H_%M_%S.%f").replace(microsecond=0) == current_second:
            print("append",current_second)
            moisture.append(np.average(temp_moisture))
            air_temperature.append(np.average(temp_air_temperature))
            gnd_temperature.append(np.average(temp_gnd_temperature))
            pressure.append(np.average(temp_pressure))
            humidity.append(np.average(temp_humidity))
            co2.append(np.average(temp_co2))
            voc.append(np.average(temp_voc))
            
            temp_moisture = []
            temp_air_temperature = []
            temp_gnd_temperature = []
            temp_pressure = []
            temp_humidity = []
            temp_co2 = []
            temp_voc = []
            temp_time_stamps = []
            
            time_stamps.append(data_point[7].split(".")[0])

            current_second += datetime.timedelta(seconds=1)
        
        if datetime.datetime.strptime(data_point[7], "%Y_%m_%d_-_%H_%M_%S.%f") > current_second:
            print("old ")
            temp_moisture.append(0)
            temp_air_temperature.append(0)
            temp_gnd_temperature.append(0)
            temp_pressure.append(0)
            temp_humidity.append(0)
            temp_co2.append(0)
            temp_voc.append(0)
            current_second += datetime.timedelta(seconds=1)
        else:
            print("new")
            temp_moisture.append(data_point[0])
            temp_air_temperature.append(data_point[1])
            temp_gnd_temperature.append(data_point[2])
            temp_pressure.append(data_point[3])
            temp_humidity.append(data_point[4])
            temp_co2.append(data_point[5])
            temp_voc.append(data_point[6])

for date in time_stamps:
    date = datetime.datetime.strptime(date, "%Y_%m_%d_-_%H_%M_%S")

moisture = np.array(moisture)
air_temperature = np.array(air_temperature)
gnd_temperature = np.array(gnd_temperature)
pressure = np.array(pressure)
humidity = np.array(humidity)
co2 = np.array(co2)
voc = np.array(voc)
time_stamps = np.array(time_stamps)

plt.plot(
        time_stamps, moisture,
        time_stamps, air_temperature,
        time_stamps, gnd_temperature,
        time_stamps, pressure,
        time_stamps, humidity,
#        time_stamps, co2,
#        time_stamps, voc
        )
plt.yticks(np.arange(0, 101, step= 2.5))
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))
plt.xticks(rotation=-30, ha="left", rotation_mode="anchor")
plt.grid()
plt.show()
