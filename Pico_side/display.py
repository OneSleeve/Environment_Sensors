import machine
import sh1106_lib

def init(i2c_bus):
    oled_width = 128
    oled_height = 64
    
    sh1106_device = sh1106_lib.SH1106_I2C(oled_width, oled_height, i2c_bus)
    
    return sh1106_device