#!/usr/bin/python3

from pyHS100 import SmartPlug
from datetime import datetime
from config import config

def runThermostat(thermostat_data):
    verbose = False
    verbose_errors = []
    errors = []

    out = config["thermostat_out"]
    away = config["thermostat_away"]

    heat_plugs = {}
    now = datetime.now()
    for thermostat_reading in thermostat_data:
        sensor_config = thermostat_reading['sensor_config']
        current_temp_f = thermostat_reading['current_temp_f']

        if sensor_config.get("thermostat_enabled", False):
            heat_smart_plug_ip = sensor_config["heat_smart_plug_ip"]

            sensor_config["current_temp_f"] = current_temp_f

            if heat_smart_plug_ip not in heat_plugs:
                heat_plugs[heat_smart_plug_ip] = []

            heat_plugs[heat_smart_plug_ip].append(sensor_config)

    verbose_errors.append("Thermostat Data")
    for heat_smart_plug_ip, monitored_sensors in heat_plugs.items():
        sensors_calling_for_heat = 0
        sensors_satisfied = 0
        for sensor in monitored_sensors:

            verbose_errors.append("")
            verbose_errors.append(sensor["name"])

            target_temp = sensor["thermostat_target"]
            temp_variance = sensor["thermostat_temp_variance"]

            if away:
                if "thermostat_target_away" in sensor:
                    verbose_errors.append("Using themorstat away temp setting")
                    target_temp = sensor["thermostat_target_away"]
                    if "thermostat_temp_variance_away" in sensor:
                        verbose_errors.append("Using thermostat away variance setting")
                        temp_variance = sensor["thermostat_temp_variance_away"]
            elif out:
                if "thermostat_target_out" in sensor:
                    verbose_errors.append("Using thermostat out temp setting")
                    target_temp = sensor["thermostat_target_out"]
                    if "thermostat_temp_variance_out" in sensor:
                        verbose_errors.append("Using thermostat out variance setting")
                        temp_variance = sensor["thermostat_temp_variance_out"]
            else:
                if now.hour > 7 and "thermostat_target_day" in sensor:
                    verbose_errors.append("Using thermostat day temp setting")
                    target_temp = sensor["thermostat_target_day"]
                    if "thermostat_temp_variance_day" in sensor:
                        verbose_errors.append("Using thermostat day variance setting")
                        temp_variance = sensor["thermostat_temp_variance_day"]
                elif now.hour < 7 and "thermostat_target_night" in sensor:
                    verbose_errors.append("Using thermostat night temp target")
                    target_temp = sensor["thermostat_target_night"]
                    if "thermostat_temp_variance_night" in sensor:
                        verbose_errors.append("Using thermostat night variance setting")
                        temp_variance = sensor["thermostat_temp_variance_night"]
            on_temp = target_temp - (temp_variance/2)
            off_temp = target_temp + (temp_variance/2)

            verbose_errors.append("Current Temp: "+str(round(sensor["current_temp_f"],2)))
            verbose_errors.append("Thermostat Target: "+str(target_temp))
            verbose_errors.append("On Temp Threshold: "+str(on_temp))
            verbose_errors.append("Off Temp Threshold: "+str(off_temp))

            if sensor["current_temp_f"] <= on_temp:
                verbose_errors.append("--Sensor calling for heat--")
                sensors_calling_for_heat += 1
            elif sensor["current_temp_f"] >= off_temp:
                verbose_errors.append("--Sensor satisfied, calling to turn off heat--")
                sensors_satisfied += 1

        heat_plug = SmartPlug(heat_smart_plug_ip)
        heat_plug_state = heat_plug.state
        verbose_errors.append("")
        verbose_errors.append("Sensors calling for heat: "+str(sensors_calling_for_heat))
        verbose_errors.append("Sensors satisfied: "+str(sensors_satisfied))
        verbose_errors.append("Total sensors: "+str(len(monitored_sensors)))
        verbose_errors.append("Heat plug: "+heat_plug_state)
        if sensors_calling_for_heat:
            if heat_plug_state is 'OFF':
                verbose_errors.append("Turning on heater")
                heat_plug.turn_on()
        elif sensors_satisfied == len(monitored_sensors):
            if heat_plug_state is 'ON':
                verbose_errors.append("Turning off heater")
                heat_plug.turn_off()

    if verbose:
        return errors + verbose_errors
    return errors

