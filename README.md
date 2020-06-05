# temperaturePi

### WIRING
- RJ12 (6P6C) connections and wire has 6 connectors which supports any number of temperature sensors plus 3 total humidity sensors. If you will never have more than 1 humidity sensor you can use RJ11 (6P4C) connections and wire, which only has 4 wires. 
- Crimp Connector Housing: 2x20-Pin 5-Pack - https://www.pololu.com/product/1992
- Wires with Pre-Crimped Terminals 10-Pack - https://www.pololu.com/product/1850
- Run the pre-crimped terminals to a multi-port RJ12 6P6C surface mount jack, this makes for a more durable connection and a place to wire the pullup resistor.
- GPIO pin 1 -> Red
- GPIO pin 6 -> Black
- GPIO pin 7 -> Yellow
- 4.7k ohm pullup resistor between red and yellow

![multi-port surface mount phone jack](https://github.com/danomoseley/temperaturePi/blob/master/media/surface_mount_jack_multi.jpg?raw=true)

- Terminate the temperature sensors using RJ12 6P6C surface mount jacks (https://www.cablesandkits.com/ethernet/surface-mount-boxes/rj11-rj12/rj12surfbox-1-wh/pro-3777/)

![rj12 surface mount phone jack](https://github.com/danomoseley/temperaturePi/blob/master/media/surface_mount_jack.jpg?raw=true)

- Use 6 wire phone line and female to female splitters to connect the network of sensors.

![RJ11 6P4C connectors](https://github.com/danomoseley/temperaturePi/blob/master/media/connectors.jpeg?raw=true)
![phone wire splitter](https://github.com/danomoseley/temperaturePi/blob/master/media/splitters.jpg?raw=true)

### SETUP
- Download Raspbian image, choose lite version: https://www.raspberrypi.org/downloads/raspbian/
- Write image to micro-sd: https://www.raspberrypi.org/documentation/installation/installing-images/linux.md
- Create empty file named `ssh` on boot partition of micro-sd, this will enable ssh server by default
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

