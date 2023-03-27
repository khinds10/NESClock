#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
from __future__ import division
import time, sched, json, string, cgi, subprocess, json, datetime, glob, numpy, random
from rpi_ws281x import PixelStrip, Color
from PIL import Image

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

# Create NeoPixel object with appropriate configuration.
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

# Intialize the library (must be called once before other functions).
strip.begin()

def prepareSpriteForMatrix(imagePixels):
    """ create final LED pixels list for display, the pixel indexes zig-zag back and forth on the LED matrix """
    finalLEDPixels = []
    rowIndex = 0

    # every other row is reversed because the pixel positions are zig-zag back and forth as you cound
    for row in imagePixels:
        if rowIndex % 2 == 0:
            row = numpy.flipud(row)
        rowIndex = rowIndex + 1
        for pixel in row:
            finalLEDPixels.append(pixel)
    return finalLEDPixels

scheduler = sched.scheduler(time.time, time.sleep)
def animateRandomSprite(sc):
    """ get a random sprite sequence to animate on the panel, updating each minute """
    try:   
        files = glob.glob("/home/khinds/NESClock/sprites/**/")
        selectedSprite = random.choice(files)
        selectedSpriteFrames = glob.glob(selectedSprite + "/*.bmp")
        selectedSpriteFrames.sort()

        # create an array of LED matrix friendly pixels
        spriteFrameRawData = []
        for spriteFrame in selectedSpriteFrames:
            im = Image.open(spriteFrame, 'r')
            imagePixels = numpy.split(numpy.asarray(list(im.getdata())), 16)
            spriteFrameRawData.append(prepareSpriteForMatrix(imagePixels))
        
        # render all pixel values as colors on the matrix frame by frame, dividing equally inside of 1 second of animation
        animationCount = 0
        while animationCount < 12:
            for spriteFrame in spriteFrameRawData:
                for i in range(0, strip.numPixels(), 1):
                    strip.setPixelColor(i, Color(int(spriteFrame[i][0]), int(spriteFrame[i][1]), int(spriteFrame[i][2])))
                    
                    
                    #strip.setPixelColor(i, Color(int(spriteFrame[i][2]), int(spriteFrame[i][1]), int(spriteFrame[i][0])))
                    
                strip.show()
                time.sleep(1/len(selectedSpriteFrames))
            animationCount = animationCount + 1

        scheduler.enter(1, 1, animateRandomSprite, (sc,))
    except:
        animateRandomSprite(0)
    
# start animating!
animateRandomSprite(0)
scheduler.run()
