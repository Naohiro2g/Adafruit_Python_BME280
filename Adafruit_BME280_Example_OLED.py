from time import sleep
from datetime import datetime

from Adafruit_BME280 import BME280
from Adafruit_BME280 import BME280_OSAMPLE_1, BME280_OSAMPLE_2, BME280_OSAMPLE_4, BME280_OSAMPLE_8, BME280_OSAMPLE_16
from Adafruit_BME280 import BME280_FILTER_off, BME280_FILTER_2, BME280_FILTER_4, BME280_FILTER_8, BME280_FILTER_16
from Adafruit_BME280 import BME280_STANDBY_0p5, BME280_STANDBY_62p5, BME280_STANDBY_125, BME280_STANDBY_250
from Adafruit_BME280 import BME280_STANDBY_500, BME280_STANDBY_1000, BME280_STANDBY_10, BME280_STANDBY_20

import RaspiOled.oled as oled
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

image = Image.new('1',oled.size)  # make 128x64 bitmap image
draw  = ImageDraw.Draw(image)

f = ImageFont.truetype(
    font='/usr/share/fonts/truetype/GenShinGothic/GenShinGothic-Monospace-Bold.ttf',
    size=14)
oled.begin()

sensor = BME280(t_mode=BME280_OSAMPLE_2, p_mode=BME280_OSAMPLE_16, h_mode=BME280_OSAMPLE_1,
         filter=BME280_FILTER_16, standby=BME280_STANDBY_125)

#sensor = BME280()


while True:
    temperature = sensor.read_temperature()
    pascals = sensor.read_pressure()
    hectopascals = pascals / 100
    humidity = sensor.read_humidity()

    #print('Temp      = {0:0.3f} deg C'.format(temperature))
    #print('Pressure  = {0:0.2f} hPa'.format(hectopascals))
    #print('Humidity  = {0:0.2f} %'.format(humidity))

    print(temperature, humidity, hectopascals)

    draw.text((0, 0), datetime.now().strftime('%Y%m%d %H:%M:%S'), font=f, fill=255)
    draw.text((0, 16), ' 気温   {0:0.1f} °C'.format(temperature), font=f, fill=255)
    draw.text((0, 32), ' 湿度   {0:0.1f}  %'.format(humidity), font=f, fill=255)
    draw.text((0, 48), ' 気圧 {0:0.2f} hPa'.format(hectopascals), font=f, fill=255)
    oled.image(image)

    sleep(0.25)
    draw.rectangle(((0, 0), (127, 63)), fill=0)
    
