#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, json, string, cgi, subprocess, json, datetime, glob, numpy
from neopixel import *
from Adafruit_LED_Backpack import SevenSegment
from PIL import Image

#

# LED strip configuration:
LED_COUNT      = 256     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 10      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

############################################
######## YOU HAVE TO RUN AS ROOT!
############################################

# setup the strip
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()
strip.show()

# get all the BMP files in the directory
files = glob.glob("./sprites/**/*.bmp")
files2 = glob.glob("./sprites/*.bmp")
for file in files2:
    files.append(file)

while True:
    for filename in files:
        print "displaying: " + filename
        im = Image.open(filename, 'r')
        imagePixels = list(im.getdata())    
        imagePixels = numpy.split(numpy.asarray(imagePixels), 16)

        # create final LED pixels list for display, the pixel indexes zig-zag back and forth on the LED matrix
        finalLEDPixels = []
        rowIndex = 0
        for row in imagePixels:
            # every other row is reversed because the pixel positions are zig-zag back and forth as you cound
            if rowIndex % 2 == 0:
                row = numpy.flipud(row)
            rowIndex = rowIndex + 1
            for pixel in row:
                finalLEDPixels.append(pixel)
                
        # render all pixel values as colors on the matrix
        for i in range(0, strip.numPixels(), 1):
            strip.setPixelColor(i, Color(finalLEDPixels[i][1], finalLEDPixels[i][0], finalLEDPixels[i][2]))
        strip.show()
        time.sleep(2)
