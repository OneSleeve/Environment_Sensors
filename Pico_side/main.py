import bme280
import co2
import moisture
import temperature
import display
import mqtt
from time import sleep

# i2c setup
i2c_bus = machine.I2C(0, sda=20, scl=21, freq=200000)

# bme280 setup (pressure sensor)
bme280_device = bme280.init(i2c_bus)

# CO2 Setup
ccs811_device = co2.init(i2c_bus)
raw_eco2 = 400
raw_voc = 0
ticks = 500

# moisture setup
moisture_device = moisture.init(26)

# temperatuer setup
temperature_device = temperature.init(28)

# display setup
display_device = display.init(i2c_bus)
display_device.init_display()

# mqtt setup
mqtt_client = mqtt.connect()

while True:
    display_device.fill(0)
    
    raw_moisture = moisture.moisture(moisture_device)
    raw_air_temperature = bme280.air_temperature(bme280_device)
    raw_ground_temperature = temperature.probe_temperature(temperature_device)
    raw_pressure = bme280.pressure(bme280_device)
    raw_humidity = bme280.humidity(bme280_device)
    
    result_temp_ccs811 = co2.data(ccs811_device)
    
    if ticks == 0:
        ticks = 500
        co2.reset(ccs811_device)
    else:
        ticks -= 1
    
    if result_temp_ccs811 != None:
        raw_eco2 = result_temp_ccs811[0]
        raw_voc = result_temp_ccs811[1]
    
    pixels = int((raw_moisture) * 64 // (100))
    display_device.fill_rect(0, 0, 10, pixels,1)
    
    if raw_moisture <= 80:
        display_device.fill_rect(1, 1, 8, pixels - 2, 0)
    
    display_device.text(f"air: {raw_air_temperature:05.2f} C", 10, 5)
    display_device.text(f"gnd: {raw_ground_temperature:05.2f} C", 10, 15)
    display_device.text(f"prs: {raw_pressure:05.2f} bar", 10, 25)
    display_device.text(f"hum: {raw_humidity:05.2f} %", 10, 35)
    display_device.text(f"co2: {raw_eco2:05} ppm", 10, 45)
    display_device.text(f"voc: {raw_voc:05} ppb", 10, 55)

    display_device.rotate(180)
    
    display_device.show()
    
    sensor_data = mqtt.consturct_string(raw_moisture, raw_air_temperature, raw_ground_temperature, raw_pressure, raw_humidity, raw_eco2, raw_voc)
    mqtt_client.publish(b"weed_sensors", sensor_data)