#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from www import orm
#from www.models import User,Blog, Comment
import asyncio

def testdb():
    'test orm and database connection'
    # 以下为测试:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(orm.create_pool( loop=loop,host='127.0.0.1', port=3306, user='www-data', password='www-data', db='awesome'))
    #rs = loop.run_until_complete(orm.select('select `id` from users', None))
    args = ['test@test.com', 'password', True, 'testname', 'blank', '1.0', 'testid']
    rs = loop.run_until_complete(orm.execute('insert into `users` (`email`,`passwd`,`admin`,`name`,`image`,`created_at`, `id`) values (?,?,?,?,?,?,?)', args))
    # 获取到了数据库返回的数据
    print("rs:%s" % rs)
    pass


testdb()
