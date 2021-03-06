To create a datalogger that can read from an LED pulse generation meter you will need to have a Raspberry Pi 2b or 3b,
with the SolarCoin daemon installed.

Log into the Pi and check for updates with:
> sudo apt-get update -y && sudo apt-get upgrade

Then install the RPi.GPIO package, this is needed to read GPIO pin inputs:
> sudo apt-get install RPi.GPIO

You will need a photsensitive cell device that has an output that is digital.  This is what I used 
https://www.aliexpress.com/item/Photosensitive-Sensor-Module-Light-Detection-Module/32587261191.html?spm=2114.13010608.0.0.KhrZUj

You will need to carefully check the GPIO pin layout and connect the pins on your sensor (failure may damage your Pi!), 
most sensors are 3.3v, you can use the GPIO pin layout available from 
https://www.raspberrypi.org/documentation/usage/gpio-plus-and-raspi2/.  The datalogger program is written to expect data on GPIO 
pin 17, and from the digital output on the sensor.

When you have everthing connected:
> git clone https://github.com/Scalextrix/ELCC

> cd ELCC/LED

> chmod +x datalogger.py

> ./datalogger.py

You will need to enter the start kWh reading from your PV generation meter each time you start/re-start the datalogger program.

