#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, json, string, cgi, subprocess, json, datetime, glob
from neopixel import *
from Adafruit_LED_Backpack import SevenSegment
from PIL import Image

# LED strip configuration:
LED_COUNT      = 256      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 20     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

############################################
######## YOU HAVE TO RUN AS ROOT!
############################################

# setup the strip
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()
strip.show()

for filename in glob.glob("./sprites/*.bmp"):
    try:
        im = Image.open(filename, 'r')
        pixVal = list(im.getdata())
        print pixVal
        for i in range(0, strip.numPixels(), 1):
            strip.setPixelColor(i, Color(pixVal[i][1], pixVal[i][0], pixVal[i][2]))
        strip.show()
        time.sleep(2)
    except: 
        pass
