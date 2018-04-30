WordClock Display using RGB LED with Raspberry Pi GPIO
======================================================

The word clock aims to build a clock that is connected to a 
Raspberry Pi and uses words to display the current time in the day. 
Its use is pretty self-explanatory - it is a modern take on old grandfather 
clocks and adds tech to your home. The letters will be printed on an acrylic 
sheet and will be glued over an LED to produce a readable time. Further advancements
for this project may be enlarging it to include the weather and other smaller 
apps around the clock. 


Be aware that running the RGBMatrix requires root privileges. Therefore you will need to run all 
your Python scripts using sudo.




Overview
========

This project is based on using:
- 32x32 RGB LED matrix panel from Adafruit: https://www.adafruit.com/product/607
- Adafruit RGB Matrix HAT from https://www.adafruit.com/product/2345
- Raspberry Pi 3 B+
- hzeller's led-matrix library from https://github.com/hzeller/rpi-rgb-led-matrix
- slight modification of brettoliver's wordclock faceplate from https://github.com/brettoliver/wordclock
- dylex's 10x20B.bdf font file from https://github.com/dylex/fonts


Quick Installation Guide
========================

1. Connect the Pi to the Adafruit RGB Matrix HAT, and then connect the HAT to the LED matrix panel.
   Additional instructions can be found on: https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices
   
   
2. Log in to the Raspberry Pi and set up timezone by running `sudo raspi-config`

3. Configure the RTC at https://www.raspberrypi.org/forums/viewtopic.php?f=66&t=125003
   - Note that the RTC is a `ds1307`

4. Clone hzeller's library with: `git clone https://github.com/hzeller/rpi-rgb-led-matrix`

5. Change into the directoary of the repository: `cd rpi-rgb-led-matrix/lib/`

6. In the Makefile, change the line `HARDWARE_DESC?=regular` to `HARDWARE_DESC?=adafruit-hat`

7. Then, in the root directory for the matrix library `/rpi-rgb-led-matrix `, type in the following commands:

```shell
sudo apt-get update && sudo apt-get install python2.7-dev python-pillow -y
make build-python
sudo make install-python
```




