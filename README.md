# temperaturePi

https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware

### WIRING
- Follow this guide on wiring the sensors to the raspberry pi gpio, using a 4.7k ohm resistor: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware
- Crimp Connector Housing: 2x20-Pin 5-Pack - https://www.pololu.com/product/1992
- Wires with Pre-Crimped Terminals 10-Pack - https://www.pololu.com/product/1850
- Run the pre-crimped terminals to a multi-port surface mount jack, this makes for a more durable connection and a place to wire the pullup resistor

![multi-port surface mount phone jack](https://github.com/danomoseley/temperaturePi/blob/master/media/surface_mount_jack.jpg?raw=true)
- Terminate the temperature sensors using RJ11 6P4C connectors. 

![RJ11 6P4C connectors](https://github.com/danomoseley/temperaturePi/blob/master/media/connectors.jpeg?raw=true)
- Use 4 wire phone line, phone couplers, and female to female splitters to connect the network of sensors.

![phone wire coupler](https://github.com/danomoseley/temperaturePi/blob/master/media/couplers.jpg?raw=true)
![phone wire splitter](https://github.com/danomoseley/temperaturePi/blob/master/media/splitters.jpg?raw=true)

### SETUP
- Download Raspbian image, choose lite version: https://www.raspberrypi.org/downloads/raspbian/
- Write image to micro-sd: https://www.raspberrypi.org/documentation/installation/installing-images/linux.md
- Create empty file named ssh on boot partition of micro-sd, this will enable ssh server by default
- Hard wire the network of the raspberry pi, boot, and find the local ip of the pi on the router
- ssh pi@llocal-ip-address, password raspberry
- run raspi-config and change the hostname to temperaturePi
- sudo apt update
- sudo apt install vim
- vim /boot/config.txt
- Add a line at the end of the file: dtoverlay=w1-gpio
- Reboot
- sudo modprobe w1-gpio
- sudo modprobe w1-therm
- cd /sys/bus/w1/devices
- ls
- If the sensors are wired correctly there should be a folder for each sensor with the name 28-xxxx
- Take note of each sensor ID, this will be needed for config.py
- Download this repo https://github.com/danomoseley/temperaturePi/archive/master.zip
- unzip temperaturePi-master.zip
- mv temperaturePi-master temperaturePi
- cd temperaturePi
- sudo apt install rrdtool
- sudo apt install python-pip libffi-dev libssl-dev
- pip install -r requirements.txt
- Run setup.py
- chmod 600 config.py
- Run create_rrd.py
- run ssh-keygen
- Add ~/.ssh/id_rsa.pub to authorized_keys on remote server
- Populate crontab using crontab_example.txt as a guide
- Profit

