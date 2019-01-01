config = {
    'temp_sensors': {
        '28-00043c93b0ff': {
            'name': 'Living Room',
            'disabled': True,
            'ds_name': 'living_room',
            'alert_threshold': 40,
            'display_order': 1,
            'rrd_order': 5,
            'color': '#66CCFF'
        },
        '28-00043c939cff': {
            'name': 'Bedroom',
            'ds_name': 'bedroom',
            'alert_threshold': 40,
            'display_order': 2,
            'rrd_order': 1,
            'color': '#0033CC'
        },
        '28-00044a37deff': {
            'name': 'Kitchen Sink',
            'ds_name': 'kitchen_sink',
            'alert_threshold': 40,
            'display_order': 3,
            'rrd_order': 6,
            'color': '#fdd80e'
        },
        '28-00043c93b8ff': {
            'name': 'Cellar',
            'ds_name': 'north_cellar',
            'alert_threshold': 40,
            'display_order': 4,
            'rrd_order': 3,
            'color': '#CC00CC'
        },
        '28-00043c92ddff': {
            'name': 'Well Pipe',
            'ds_name': 'under_stairs',
            'alert_threshold': 40,
            'display_order': 5,
            'rrd_order': 2,
            'color': '#009900'
        },
        '28-00043b6f76ff': {
            'name': 'Outside',
            'ds_name': 'outside',
            'display_order': 6,
            'rrd_order': 4,
            'color': '#CC0000'
        }
    },
    'humidity_sensors': {
        14: {
            'name': 'Living Room',
            'ds_name': 'living_room',
            'display_order': 1,
            'rrd_order': 1,
            'color': '#66CCFF'
        }
    },
    'lake_temp_sensors_disabled': False,
    'lake_temp_sensors': {
        'air_temperature': {
            'name': 'Air',
            'ds_name': 'temp_air',
            'display_order': 1,
            'rrd_order': 1,
            'color': '#f5d831'
        },
        'temp_0m': {
            'name': 'Surface',
            'ds_name': 'temp_0m',
            'display_order': 2,
            'rrd_order': 2,
            'color': '#66CCFF'
        },
        'temp_2m': {
            'name': '2 Meters',
            'ds_name': 'temp_2m',
            'display_order': 3,
            'rrd_order': 3,
            'color': '#5CBEFA'
        },
        'temp_4m': {
            'name': '4 Meters',
            'ds_name': 'temp_4m',
            'display_order': 4,
            'rrd_order': 4,
            'color': '#53B0F5'
        },
        'temp_10m': {
            'name': '10 Meters',
            'ds_name': 'temp_10m',
            'display_order': 5,
            'rrd_order': 5,
            'color': '#4AA2F1'
        },
        'temp_14m': {
            'name': '14 Meters',
            'ds_name': 'temp_14m',
            'display_order': 6,
            'rrd_order': 6,
            'color': '#4094EC'
        },
        'temp_20m': {
            'name': '20 Meters',
            'ds_name': 'temp_20m',
            'display_order': 7,
            'rrd_order': 7,
            'color': '#3786E7'
        },
        'temp_25m': {
            'name': '25 Meters',
            'ds_name': 'temp_25m',
            'display_order': 8,
            'rrd_order': 8,
            'color': '#2E78E3'
        },
        'temp_30m': {
            'name': '30 Meters',
            'ds_name': 'temp_30m',
            'display_order': 9,
            'rrd_order': 9,
            'color': '#256ADE'
        },
        'temp_35m': {
            'name': '35 Meters',
            'ds_name': 'temp_35m',
            'display_order': 10,
            'rrd_order': 10,
            'color': '#1B5CD9'
        },
        'temp_40m': {
            'name': '40 Meters',
            'ds_name': 'temp_40m',
            'display_order': 11,
            'rrd_order': 11,
            'color': '#124ED5'
        },
        'temp_44m': {
            'name': '44 Meters',
            'ds_name': 'temp_44m',
            'display_order': 12,
            'rrd_order': 12,
            'color': '#0940D0'
        },
        'temp_48m': {
            'name': '48 Meters',
            'ds_name': 'temp_48m',
            'display_order': 13,
            'rrd_order': 13,
            'color': '#0033CC'
        }
    },
    'gmail': {
        'username': 'email@gmail.com',
        'password': 'password',
        'from_address': 'email@gmail.com',
        'to_addresses': 'email@gmail.com',
        'site_url': 'http://my.awesometemp.com'
    },
    'remote': {
        'host': 'direct.myhost.com',
        'user': 'user',
        'path': '/var/www/temperaturePi'
    }
}
