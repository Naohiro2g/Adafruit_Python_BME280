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

from matplotlib import pyplot as plt
from numpy import arange, pi, sin, cos


image = Image.new('1',oled.size)  # make 128x64 bitmap image
draw  = ImageDraw.Draw(image)

f = ImageFont.truetype(
    font='/usr/share/fonts/truetype/GenShinGothic/GenShinGothic-Monospace-Bold.ttf',
    size=14)
oled.begin()

sensor = BME280(t_mode=BME280_OSAMPLE_2, p_mode=BME280_OSAMPLE_16, h_mode=BME280_OSAMPLE_1,
         filter=BME280_FILTER_16, standby=BME280_STANDBY_125)


plt.ion()
fig = plt.figure(figsize=(8,8),dpi=100)
fig.suptitle('BME280 Environmental Measurement', fontsize=18)
plt.tight_layout()

plt.subplots_adjust(hspace=0.5)
plt.rcParams["font.size"] = 16
plt.rcParams["font.family"] = "Gen Shin Gothic"



#ax1 = fig.add_subplot(311, xticks=[], ylim=[-10, 50])
ax1 = fig.add_subplot(311, ylim=[-10, 50])
ax2 = fig.add_subplot(312, ylim=[20,80], sharex=ax1)
ax3 = fig.add_subplot(313, ylim=[900,1100], sharex=ax1)

ax1.grid()
ax2.grid()
ax3.grid()

ax1.set_title("Temperature   温度  (°C)")
ax2.set_title("Humidity   湿度  (%)")
ax3.set_title("Pressure   気圧  (hPa  ヘクトパスカル)")

LIST_NUM = 120  # number of plot points
RATE = 2

t = [0] * LIST_NUM
h = [0] * LIST_NUM
p = [0] * LIST_NUM
x = [0] * LIST_NUM
s = 0

lines1, = ax1.plot(x, t, color='#882222', linewidth=4)
lines2, = ax2.plot(x, t, color='#228822', linewidth=4)
lines3, = ax3.plot(x, t, color='#222288', linewidth=4)


while True:
    temperature = sensor.read_temperature()
    pascals = sensor.read_pressure()
    hectopascals = pascals / 100
    humidity = sensor.read_humidity()


# console
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '  {0:0.1f}°C'.format(temperature),  '  {0:0.1f}%'.format(humidity),  '  {0:0.2f}hPa'.format(hectopascals))

# OLED
    draw.rectangle(((0, 0), (127, 63)), fill=0)
    draw.text((0, 0), datetime.now().strftime('%Y%m%d %H:%M:%S'), font=f, fill=255)
    draw.text((0, 16), ' 気温   {0:0.1f} °C'.format(temperature), font=f, fill=255)
    draw.text((0, 32), ' 湿度   {0:0.1f}  %'.format(humidity), font=f, fill=255)
    draw.text((0, 48), ' 気圧 {0:0.2f} hPa'.format(hectopascals), font=f, fill=255)
    oled.image(image)
    
# matplotlib
    x.pop(0)
    t.pop(0)
    h.pop(0)
    p.pop(0)

    x.append(s)
    t.append(temperature)
    h.append(humidity)
    p.append(hectopascals)

    ax1.set_xlim(x[0], x[0] + LIST_NUM / RATE)

#    ax1.plot(x, t, color='#FF7777', linewidth=4)
    lines1.set_data(x, t)
#    ax2.plot(x, h, color='#77FF77', linewidth=4)
    lines2.set_data(x, h)
#    ax3.plot(x, p, color='#7777FF', linewidth=4)
    lines3.set_data(x, p)

    s += 1.0 / RATE
    plt.pause(0.001)

    sleep(1.0 / RATE)


plt.ioff()
plt.show()
