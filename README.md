# Smart Bartender
Why spend lots of money going out for drinks when you can have your own smart personal bartender at your service right in your home?! This bartender is built from a Raspberry Pi 3 and some common DIY electronics.

## Prerequisites for the Raspberry Pi
Make sure you can connect a screen and keyboard to your Raspberry Pi. I like to use VNC to connect to the Pi. I created a [tutorial](https://www.youtube.com/watch?v=2iVK8dn-6x4) about how to set that up on a Mac.

### Enable SPI
You'll need to enable SPI for the OLED screen to work properly. Typing the following command in the terminal will bring you to a configuration menu.

```
raspi-config 
```
Then navigate to `Interfacing Options` and select `SPI`. Make sure it's turned on and reboot.

See this [article](https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/) for more help if you need it.

### I2C
Make sure i2c is also configured properly. Type

```
sudo vim /etc/modules
```

in the terminal

press `i`, then make sure to paste the following two lines in the file:

```
i2c-bcm2708
i2c-dev
```
press `esc` then `ZZ` to save and exit.

## OLED Setup
The Raspberry Pi Guy has a nice script to setup the OLED screen on your raspberry pi. Download the following repository on your Pi:

https://github.com/the-raspberry-pi-guy/OLED

then navigate to the folder with the terminal

```
cd ~/path/to/directory
```

and run the installation script

```
sh OLEDinstall.sh
```

There is also a [guide](https://learn.adafruit.com/adafruit-oled-displays-for-raspberry-pi/setting-up) on the Adafruit website if you get stuck.

## Running the Code

First, make sure to download this repository on your raspberry pi. Once you do, navigate to the downloaded folder in the terminal:

```
cd ~/path/to/directory
```

and install the dependencies

```
sudo pip install -r requirements.txt
```

You can start the bartender by running

```
sudo python bartender.py
```

### Running at Startup

You can configure the bartender to run at startup by starting the program from the `rc.local` file. First, make sure to get the path to the repository directory by running

```
pwd
```

from the repository folder. Copy this to your clipboard.

Next, type

```
sudo vim /etc/rc.local
```

to open the rc.local file. Next, press `i` to edit. Before the last line, add the following two lines:

```
cd your/pwd/path/here
sudo python bartender.py &
```

`your/pwd/path/here` should be replaced with the path you copied above. `sudo python bartender.py &` starts the bartender program in the background. Finally, press `esc` then `ZZ` to save and exit. 

If that doesn't work, you can consult this [guide](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/) for more options.
