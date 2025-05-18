# MIT License
#
# Copyright (c) 2018 Airthings AS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# https://airthings.com

import bluepy.btle as btle
import argparse
import os
import signal
import struct
from subprocess import getstatusoutput
import sys
import time
from utils import sendAlertEmail, getExceptionInfo

from config import config

DIR = os.path.dirname(os.path.realpath(__file__))


class Wave2():

    CURR_VAL_UUID = btle.UUID("b42e4dcc-ade7-11e4-89d3-123b93f75cba")

    def __init__(self, serial_number):
        self._periph = None
        self._char = None
        self.mac_addr = None
        self.serial_number = serial_number

    def is_connected(self):
        try:
            return self._periph.getState() == "conn"
        except Exception:
            return False

    def discover(self):
        scan_interval = 0.1
        timeout = 3
        scanner = btle.Scanner()
        for _count in range(int(timeout / scan_interval)):
            advertisements = scanner.scan(scan_interval)
            for adv in advertisements:
                if self.serial_number == _parse_serial_number(adv.getValue(btle.ScanEntry.MANUFACTURER)):
                    return adv.addr
        return None

    def connect(self, retries=1):
        tries = 0
        while (tries < retries and self.is_connected() is False):
            tries += 1
            if self.mac_addr is None:
                self.mac_addr = self.discover()
            try:
                self._periph = btle.Peripheral(self.mac_addr)
                self._char = self._periph.getCharacteristics(uuid=self.CURR_VAL_UUID)[0]
            except Exception:
                if tries == retries:
                    raise
                else:
                    pass

    def read(self):
        rawdata = self._char.read()
        return CurrentValues.from_bytes(rawdata)

    def disconnect(self):
        if self._periph is not None:
            self._periph.disconnect()
            self._periph = None
            self._char = None


class CurrentValues():

    def __init__(self, humidity, radon_sta, radon_lta, temperature):
        self.humidity = humidity
        self.radon_sta = radon_sta
        self.radon_lta = radon_lta
        self.temperature = temperature

    @classmethod
    def from_bytes(cls, rawdata):
        data = struct.unpack("<4B8H", rawdata)
        if data[0] != 1:
            raise ValueError("Incompatible current values version (Expected 1, got {})".format(data[0]))
        return cls(data[1]/2.0, round(data[4]/37.0, 1), round(data[5]/37.0, 1), data[6]/100.0)

    def __str__(self):
        msg = "Humidity: {} %rH, ".format(self.humidity)
        msg += "Temperature: {} *C, ".format(self.temperature)
        msg += "Radon STA: {} pCi/L, ".format(self.radon_sta)
        msg += "Radon LTA: {} pCi/L".format(self.radon_lta)
        return msg


def readRadonSensors():
    errors = []

    rrd_path = os.path.join(DIR, 'database', 'radon.rrd')
    
    serial_number = next(iter(config['radon_sensors']))
    wave2 = Wave2(serial_number)

    def _signal_handler(sig, frame):
        wave2.disconnect()
        sys.exit(0)

    signal.signal(signal.SIGINT, _signal_handler)

    connection_tries = 0
    while True:
        try:
            wave2.connect(retries=6)
            current_values = wave2.read()
            radon_sta = current_values.radon_sta
            wave2.disconnect()
            command = '/usr/bin/rrdtool update %s N:%s' % (rrd_path, radon_sta)
            status, message = getstatusoutput(command)
            if status != 0:
                errors.append('Error running %s - %d - %s' % (command, status, message))
        except btle.BTLEDisconnectError as e:
            connection_tries += 1
            if connection_tries > 5:
                errors.append('Could not connect to radon sensor after 5 tries, giving up..')
            else:
                continue
        break

    return errors


def process():
    errors = []
    try:
        sensor_errors = readRadonSensors()
        errors.extend(sensor_errors)
    except Exception as e:
        errors.append(getExceptionInfo(e))

    if len(errors):
        if 'gmail' in config:
            sendAlertEmail(errors)
        print('\n'.join(errors))


def _parse_serial_number(manufacturer_data):
    try:
        (ID, SN, _) = struct.unpack("<HLH", manufacturer_data)
    except Exception:  # Return None for non-Airthings devices
        return None
    else:  # Executes only if try-block succeeds
        if ID == 0x0334:
            return SN

