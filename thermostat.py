#!/usr/bin/python3

from pyHS100 import SmartPlug

def runThermostat(thermostat_data):
    errors = []
    heat_plugs = {}
    for thermostat_reading in thermostat_data:
        sensor_config = thermostat_reading['sensor_config']
        current_temp_f = thermostat_reading['current_temp_f']

        if sensor_config.get("thermostat_enabled", False):
            heat_smart_plug_ip = sensor_config["heat_smart_plug_ip"]

            sensor_config["current_temp_f"] = current_temp_f

            if heat_smart_plug_ip not in heat_plugs:
                heat_plugs[heat_smart_plug_ip] = []

            heat_plugs[heat_smart_plug_ip].append(sensor_config)

    for heat_smart_plug_ip, monitored_sensors in heat_plugs.items():
        sensors_calling_for_heat = 0
        sensors_satisfied = 0
        for sensor in monitored_sensors:
            target_temp = sensor["thermostat_target"]
            temp_variance = sensor["thermostat_temp_variance"]
            on_temp = target_temp - (temp_variance/2)
            off_temp = target_temp + (temp_variance/2)

            if sensor["current_temp_f"] <= on_temp:
                sensors_calling_for_heat += 1
            elif sensor["current_temp_f"] >= off_temp:
                sensors_satisfied += 1

        heat_plug = SmartPlug(heat_smart_plug_ip)
        heat_plug_state = heat_plug.state

        if sensors_calling_for_heat:
            if heat_plug_state is 'OFF':
                heat_plug.turn_on()
        elif sensors_satisfied == len(monitored_sensors):
            if heat_plug_state is 'ON':
                heat_plug.turn_off()

    return errors

