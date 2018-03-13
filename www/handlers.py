#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Tianhe'

'web url handlers'

from www.coroweb import get,post

@get('/home')
def homePage():
    return {
        '__template__': 'signin.html'
    }

@get('/signin')
def signin():
    return {
        '__template__': 'signin.html'
    }