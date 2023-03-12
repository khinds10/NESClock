#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, board
from PIL import Image, ImageDraw, ImageFont
from adafruit_ht16k33.matrix import Matrix8x8

# all the displays by I2C address
i2c = board.I2C()
displayBrightness = 0.5
displays = [Matrix8x8(i2c,address=0x70), Matrix8x8(i2c,address=0x71), Matrix8x8(i2c,address=0x72), Matrix8x8(i2c,address=0x73), Matrix8x8(i2c,address=0x74), Matrix8x8(i2c,address=0x75), Matrix8x8(i2c,address=0x76)]

def clearDisplays():
    """clear all the displays in the clock"""
    global displayBrightness
    for display in displays:
        display.brightness = displayBrightness
        display.fill(0)

def writeCharacter(displayNumber, textValue):
    """for given display number, write the text value"""
    global displays
    image = Image.new('1', (8, 8))
    draw = ImageDraw.Draw(image)
    fnt = ImageFont.truetype('/home/khinds/NESClock/LED.ttf', 10)
    draw.text((0,0), textValue, font=fnt, fill=255)
    image  = image.transpose(Image.ROTATE_270)
    displays[displayNumber].shift_right(True)
    time.sleep(0.02)
    displays[displayNumber].shift_up(True)
    time.sleep(0.02)    
    displays[displayNumber].shift_up(True)
    time.sleep(0.02)   
    displays[displayNumber].shift_up(True)
    time.sleep(0.02)
    displays[displayNumber].shift_left(True)
    time.sleep(0.02)        
    displays[displayNumber].image(image)

def writeTime(value):
    """for a complete time string, write it to the clock"""
    count = 6
    for c in value:
        writeCharacter(count, c)
        count = count - 1

# clear displays and start the time, with a blinking colon
clearDisplays()
while True:
    now = time.strftime("%I:%M%p")
    writeTime(now)
    time.sleep(1)
