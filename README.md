# 8 Bit Sprite Clock
Game Room Nintendo Time w/ Friendly Sprites to greet you

#### Flashing RaspberriPi Hard Disk / Install Required Software (Using Ubuntu Linux)

Download "RASPBIAN JESSIE LITE"
https://www.raspberrypi.org/downloads/raspbian/

**Create your new hard disk for DashboardPI**
>Insert the microSD to your computer via USB adapter and create the disk image using the `dd` command
>
> Locate your inserted microSD card via the `df -h` command, unmount it and create the disk image with the disk copy `dd` command
> 
> $ `df -h`
> */dev/sdb1       7.4G   32K  7.4G   1% /media/XXX/1234-5678*
> 
> $ `umount /dev/sdb1`
> 
> **Caution: be sure the command is completely accurate, you can damage other disks with this command**
> 
> *if=location of RASPBIAN JESSIE LITE image file*
> *of=location of your microSD card*
> 
> $ `sudo dd bs=4M if=/path/to/raspbian-jessie-lite.img of=/dev/sdb`
> *(note: in this case, it's /dev/sdb, /dev/sdb1 was an existing factory partition on the microSD)*

**Setting up your RaspberriPi**

*Insert your new microSD card to the raspberrypi and power it on with a monitor connected to the HDMI port*

Login
> user: **pi**
> pass: **raspberry**

Change your account password for security
>`sudo passwd pi`

Enable RaspberriPi Advanced Options
>`sudo raspi-config`

Choose:
`1 Expand File System`

`9 Advanced Options`
>`A2 Hostname`
>*change it to "SpriteClock"*
>
>`A4 SSH`
>*Enable SSH Server*
>
>`A7 I2C`
>*Enable i2c interface*

**Enable the English/US Keyboard**

>`sudo nano /etc/default/keyboard`

> Change the following line:
>`XKBLAYOUT="us"`

**Reboot PI for Keyboard layout changes / file system resizing to take effect**
>$ `sudo shutdown -r now`

**Auto-Connect to your WiFi**

>`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

Add the following lines to have your raspberrypi automatically connect to your home WiFi
*(if your wireless network is named "linksys" for example, in the following example)*

	network={
	   ssid="linksys"
	   psk="WIRELESS PASSWORD HERE"
	}

**Reboot PI to connect to WiFi network**

>$ `sudo shutdown -r now`
>
>Now that your PI is finally on the local network, you can login remotely to it via SSH.
>But first you need to get the IP address it currently has.
>
>$ `ifconfig`
>*Look for "inet addr: 192.168.XXX.XXX" in the following command's output for your PI's IP Address*

**Go to another machine and login to your raspberrypi via ssh**

> $ `ssh pi@192.168.XXX.XXX`

**Start Installing required packages**

>$ `sudo apt-get update`
>
>$ `sudo apt-get upgrade`
>
>$ `sudo apt-get install vim git python-smbus i2c-tools python-imaging python-smbus build-essential python-dev rpi.gpio python3 python3-pip python-numpy`

**Update local timezone settings

>$ `sudo dpkg-reconfigure tzdata`

`select your timezone using the interface`

**Setup the simple directory `l` command [optional]**

>`vi ~/.bashrc`
>
>*add the following line:*
>
>`alias l='ls -lh'`
>
>`source ~/.bashrc`

**Fix VIM default syntax highlighting [optional]**

>`sudo vi  /etc/vim/vimrc`
>
>uncomment the following line:
>
>_syntax on_

**Install i2c Backpack Python Drivers**

>$ `cd ~`
>
>$ `git clone https://github.com/adafruit/Adafruit_Python_LED_Backpack`
>
>$ `cd Adafruit_Python_LED_Backpack/`
>
>$ `sudo python setup.py install`
>

**Install i2c Python Drivers**

Install the NeoPixel Driver as follows 

>`sudo apt-get install build-essential python-dev git scons swig`
>
>`sudo pip3 install --upgrade setuptools`
>
>`sudo pip3 install rpi_ws281x`
>
>`cd rpi_ws281x`
>
>`scons`
>
>`cd python`
>
>`sudo python setup.py install`
>
>`cd examples/`
>
>`sudo python strandtest.py`

# Supplies Needed

Pi Zero W/1.3/1.2

![Pi Zero](https://raw.githubusercontent.com/khinds10/NESClock/master/construction/PiZero.jpg "Pi Zero")

Wifi USB (if Pi Zero 1.3/1.2)

![WIFI USB](https://raw.githubusercontent.com/khinds10/NESClock/master/construction/wifi.jpg "WIFI USB")

Keyestudio I2C 8x8 LED Matrix HT16K33 (x7)

![LED 16x16](https://raw.githubusercontent.com/khinds10/NESClock/master/construction/16x16-led.png "LED 16x16 Matrix")

16x16 RGB LED Flexible WS2812B Matrix

![WS2812B Matrix](https://raw.githubusercontent.com/khinds10/NESClock/master/construction/16x16-RGB.png "WS2812B Matrix")

Frosted Paint

![Frosted Paint](https://raw.githubusercontent.com/khinds10/NESClock/master/construction/paint.jpg "Frosted Paint")

12x12 Picture Frame

![Picture Frame](https://raw.githubusercontent.com/khinds10/NESClock/master/construction/picture-frame.png "Picture Frame")

Cuttable thin plexi-glass sheet

![Thin Plexi Glass Sheet](https://raw.githubusercontent.com/khinds10/NESClock/master/construction/plexi.png "Thin Plexi Glass Sheet")

# Building the Sprite Clock

![Wiring Diagram](https://raw.githubusercontent.com/khinds10/NESClock/master/construction/wiringdiagram.png "Wiring Diagram")

**Clone the repository in your home directory for the clock to work**

> `cd ~`
>
> `git clone https://github.com/khinds10/NESClock.git`

### Set pi user crontab 

Enter the following line for a minute by minute crontab

`$ crontab -e`

`@reboot nohup python /home/pi/NESClock/MatrixClock.py > /dev/null 2>&1`

### Set root user crontab (this library requires root access)

Set "on reboot" to run the candle python script forever

`$ sudo su`

`$ crontab -e`

`@reboot nohup python /home/pi/NESClock/SpritePanel.py > /dev/null 2>&1`

# Finished!
