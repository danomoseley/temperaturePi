#!/usr/bin/python3

from pyHS100 import SmartPlug

def runThermostat(sensor_config, current_temp_f):
    if sensor_config.get("thermostat_enabled", False):
        target_temp = sensor_config["thermostat_target"]
        temp_variance = sensor_config["thermostat_temp_variance"]
        heat_smart_plug_ip = sensor_config["heat_smart_plug_ip"]
        heat_plug = SmartPlug(heat_smart_plug_ip)

        on_temp = target_temp - (temp_variance/2)
        off_temp = target_temp + (temp_variance/2)

        if current_temp_f <= on_temp:
            if heat_plug.state is "OFF":
                heat_plug.turn_on()
        elif current_temp_f >= off_temp:
            if heat_plug.state is "ON":
                heat_plug.turn_off()

