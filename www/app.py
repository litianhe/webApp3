#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging; logging.basicConfig(level=logging.INFO)

import asyncio,os,json,time
from datetime import datetime

from aiohttp import web

def index(request):
    print('index...')
    return web.Response(body=b'<h1>awesome</h1>',headers={'content-type':'text/html'})   #Tianhe:add headers={'content-type':'text/html'} to avoid file download issue

@asyncio.coroutine
def init(loop):
    print('init...')
    app = web.Application(loop=loop)
    app.router.add_route('Get', '/', index)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000 ...')
    #return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()