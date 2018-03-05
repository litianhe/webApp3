#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from www import orm
from www.models import User,Blog, Comment
import asyncio

#id = StringField(is_primary_key=True, default=next_id, ddl='varchar(50)')
#email = StringField(ddl='varchar(50)')
#passwd = StringField(ddl='varchar(50)')
#admin = BooleanField()
#name = StringField(ddl='varchar(50)')
#image = StringField(ddl='varchar(500)')
#created_at = FloatField(default=time.time)

#testdb pass
def testdb(loop):
    'test class User - add a new user'
    print('Create db pool...')
    r = yield from orm.create_pool(loop=loop, host='127.0.0.1', port=3306, user='www-data', password='www-data', db='awesome')
    print('r : %s' % r)
    # 以下为测试:
    print('Create a new user...')

    "create a user with fixed <id> and <created_at>"
    #u = User(email='test2@test.com', passwd='password', admin=True, name='testname2', image='blank', id='testid2',created_at='1.0')

    "create a user with fixed auto-generated <id> and <created_at>"
    u = User(email='test2@test.com', passwd='password', admin=True, name='testname2', image='blank',id=None,created_at=None) #
    print('Save the new user into database...')
    r = yield from u.save()
    print('r : %s' % r)


loop = asyncio.get_event_loop()
loop.run_until_complete(testdb(loop))
#for i in testdb():
#    print('testdb: i=%s', i)
