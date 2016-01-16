config = {
    'temp_sensors': {
        '28-00043c93b0ff': {
            'name': 'Living Room',
            'ds_name': 'living_room',
            'alert_threshold': 40,
            'display_order': 1,
            'color': '#66CCFF'
        },
        '28-00043c939cff': {
            'name': 'Bedroom',
            'ds_name': 'bedroom',
            'alert_threshold': 40,
            'display_order': 2,
            'color': '#0033CC'
        },
        '28-00044a37deff': {
            'name': 'Kitchen Sink',
            'ds_name': 'kitchen_sink',
            'alert_threshold': 40,
            'display_order': 3,
            'color': '#fdd80e'
        },
        '28-00043c93b8ff': {
            'name': 'Cellar',
            'ds_name': 'north_cellar',
            'alert_threshold': 40,
            'display_order': 4,
            'color': '#CC00CC'
        },
        '28-00043c92ddff': {
            'name': 'Well Pipe',
            'ds_name': 'under_stairs',
            'alert_threshold': 40,
            'display_order': 5,
            'color': '#009900'
        },
        '28-00043b6f76ff': {
            'name': 'Outside',
            'ds_name': 'outside',
            'display_order': 6,
            'color': '#CC0000'
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
