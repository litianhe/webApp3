#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Tianhe'

'webApp3 configration'

import www.config_default as configDefault


def merge(defaults, override):
    for name, value in defaults.items():
        if name in override:
            if isinstance(value,dict):
                merge(value, override[name])
            else:
                defaults[name] =  override[name]
    return defaults


'''
def merge(defaults, override):
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r
'''

configs = configDefault.configs

try:
    import www.config_override as config_override
    configs = merge(configs, config_override.configs)
    print('config %s' % configs)
    print('config override %s' % config_override.configs)

except ImportError:
    pass
