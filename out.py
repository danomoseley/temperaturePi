#!/usr/bin/env python

import os
from config import config
import pprint

DIR = os.path.dirname(os.path.realpath(__file__))

config["thermostat_out"] = not config["thermostat_out"]
print(config["thermostat_out"])

pp = pprint.PrettyPrinter(indent=4)
f = open(DIR+'/config.py', 'w')
f.write('config = %s' % pp.pformat(config))
