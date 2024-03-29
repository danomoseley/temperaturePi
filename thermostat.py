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
    is_day = datetime.now().hour in range(8,22)

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

            if 'smart_plug_mode' not in sensor:
                sensor['smart_plug_mode'] = 'heat'

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
                if is_day and "thermostat_target_day" in sensor:
                    verbose_errors.append("Using thermostat day temp setting")
                    target_temp = sensor["thermostat_target_day"]
                    if sensor["smart_plug_mode"] == 'cool' and "thermostat_target_day_cool" in sensor:
                        target_temp = sensor["thermostat_target_day_cool"]

                    if "thermostat_temp_variance_day" in sensor:
                        verbose_errors.append("Using thermostat day variance setting")
                        temp_variance = sensor["thermostat_temp_variance_day"]
                elif not is_day and "thermostat_target_night" in sensor:
                    verbose_errors.append("Using calculated thermostat night temp target")
                    target_temp = sensor["thermostat_target_night"]
                    if sensor["smart_plug_mode"] == 'cool' and "thermostat_target_night_cool" in sensor:
                        target_temp = sensor["thermostat_target_night_cool"]

                    if "thermostat_temp_variance_night" in sensor:
                        verbose_errors.append("Using thermostat night variance setting")
                        temp_variance = sensor["thermostat_temp_variance_night"]

            verbose_errors.append("Current Temp: "+str(round(sensor["current_temp_f"],2)))
            verbose_errors.append("Thermostat Target: "+str(target_temp))

            if sensor['smart_plug_mode'] == 'cool':
                on_temp = target_temp + (temp_variance/2)
                off_temp = target_temp - (temp_variance/2)
                verbose_errors.append("On Temp Threshold: "+str(on_temp))
                verbose_errors.append("Off Temp Threshold: "+str(off_temp))

                if sensor["current_temp_f"] >= on_temp:
                    verbose_errors.append("--Sensor calling for ac--")
                    sensors_calling_for_heat += 1
                elif sensor["current_temp_f"] <= off_temp:
                    verbose_errors.append("--Sensor satisfied, calling to turn off ac--")
                    sensors_satisfied += 1
            elif sensor['smart_plug_mode'] == 'heat':
                on_temp = target_temp - (temp_variance/2)
                off_temp = target_temp + (temp_variance/2)
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
        
        secondary_smart_plug=False
        #secondary_smart_plug = SmartPlug("192.168.2.106")

        verbose_errors.append("")
        verbose_errors.append("Sensors calling for heat: "+str(sensors_calling_for_heat))
        verbose_errors.append("Sensors satisfied: "+str(sensors_satisfied))
        verbose_errors.append("Total sensors: "+str(len(monitored_sensors)))
        verbose_errors.append("Heat plug: "+heat_plug_state)
        if secondary_smart_plug:
            verbose_errors.append("Secondary smart plug: "+secondary_smart_plug.state)

        if sensors_calling_for_heat:
            if heat_plug_state is 'OFF':
                verbose_errors.append("Turning on heater")
                heat_plug.turn_on()
            if secondary_smart_plug:
                if is_day and heat_plug_state is 'ON' and secondary_smart_plug.state is 'OFF':
                    verbose_errors.append("Turning on secondary smart plug")
                    secondary_smart_plug.turn_on()
        elif sensors_satisfied == len(monitored_sensors):
            if secondary_smart_plug and secondary_smart_plug.state is 'ON':
                verbose_errors.append("Turning off secondary smart plug")
                secondary_smart_plug.turn_off()
            elif heat_plug_state is 'ON':
                verbose_errors.append("Turning off heater")
                heat_plug.turn_off()

    if verbose:
        return errors + verbose_errors
    return errors

