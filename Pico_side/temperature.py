import machine
import ds18x20
import onewire

def init(pin):
    return machine.Pin(pin, machine.Pin.IN)

def probe_temperature(temperature_device):
    sensor = ds18x20.DS18X20(onewire.OneWire(temperature_device))
    roms = sensor.scan()
    sensor.convert_temp()
    
    for rom in roms:
        temperature_in_c = round(sensor.read_temp(rom),1)
    
    return temperature_in_c
