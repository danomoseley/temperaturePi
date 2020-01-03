#!/usr/bin/python3

from pyHS100 import SmartPlug

def runThermostat(thermostat_data):
    heat_plugs = {}
    for thermostat_reading in thermostat_data:
        sensor_config = thermostat_reading['sensor_config']
        current_temp_f = thermostat_reading['current_temp_f']

        if sensor_config.get("thermostat_enabled", False):
            target_temp = sensor_config["thermostat_target"]
            temp_variance = sensor_config["thermostat_temp_variance"]
            heat_smart_plug_ip = sensor_config["heat_smart_plug_ip"]

            on_temp = target_temp - (temp_variance/2)
            off_temp = target_temp + (temp_variance/2)

            if heat_smart_plug_ip not in heat_plugs:
                heat_plugs[heat_smart_plug_ip] = None

            if current_temp_f <= on_temp:
                heat_plugs[heat_smart_plug_ip] = True
            elif current_temp_f >= off_temp:
                turn_off_heat = not heat_plugs[heat_smart_plug_ip] and True
                heat_plugs[heat_smart_plug_ip] = not turn_off_heat

    for heat_smart_plug_ip, turn_on_heat_plug in heat_plugs.items():
        if turn_on_heat_plug is not None:
            heat_plug = SmartPlug(heat_smart_plug_ip)
            if turn_on_heat_plug:
                heat_plug.turn_on()
            else:
                heat_plug.turn_off()

