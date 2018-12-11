#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time
from PIL import Image, ImageDraw, ImageFont
from Adafruit_LED_Backpack import Matrix8x8

# all the displays by I2C address
displayBrightness = 5
displays = [Matrix8x8.Matrix8x8(address=0x70), Matrix8x8.Matrix8x8(address=0x71), Matrix8x8.Matrix8x8(address=0x72), Matrix8x8.Matrix8x8(address=0x73), Matrix8x8.Matrix8x8(address=0x74), Matrix8x8.Matrix8x8(address=0x75), Matrix8x8.Matrix8x8(address=0x76)]

def clearDisplays():
    """clear all the displays in the clock"""
    global displayBrightness
    for display in displays:
        display.begin()
        display.set_brightness(displayBrightness)
        display.clear()
        display.write_display()

def writeCharacter(displayNumber, textValue):
    """for given display number, write the text value"""
    global displays
    image = Image.new('1', (8, 8))
    draw = ImageDraw.Draw(image)
    fnt = ImageFont.truetype('PressStart2P.ttf', 9)
    draw.text((0,0), textValue, font=fnt, fill=255)
    image  = image.transpose(Image.ROTATE_90)
    displays[displayNumber].set_image(image)
    displays[displayNumber].write_display()

def writeTime(value):
    """for a complete time string, write it to the clock"""
    count = 6
    for c in value:
        writeCharacter(count, c)
        count = count - 1

# clear displays and start the time, with a blinking colon
clearDisplays()
showColon = True
while True:
    if showColon == True:
        now = time.strftime("%I:%M%p")
    if showColon == False:
            now = time.strftime("%I %M%p")
    showColon = not showColon
    writeTime(now)
    time.sleep(1)
