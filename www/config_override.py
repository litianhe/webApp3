#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Tianhe'

'webApp3 configration override'

#config_override.py

configs = {
    'debug': False,
    'db':{
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'www-data',
        'password': 'www-data',
        'database': 'awesome'
    }
}