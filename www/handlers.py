#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Tianhe'

'web url handlers'

from www.coroweb import get,post
from www.models import User,Blog,Comment
from www.apis import *
import time
import re
import hashlib
from aiohttp import web
import json
from www.config import configs
import logging

COOKIE_NAME = 'WebApp3Cookie'
#_COOKIE_KEY = configs.session.secret
_COOKIE_KEY = configs['session']['secret']

@get('/test')
def homePage(request):
    users = yield from User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }


def user2cookie(user, max_age=86400):
    if not isinstance(user, User):
        raise Exception('error input user.')
    # build cookie string by: id-expires-digest
    expire_time = str(int(time.time() + max_age))
    hash_str = 'userid:%s password:%s max_age:%s secert_key:%s' % (user.id, user.passwd, expire_time, _COOKIE_KEY)
    digest = hashlib.sha1(hash_str.encode('utf-8')).hexdigest()
    L = [user.id, expire_time, digest]
    return '-'.join(L)

def cookie2user(cookie_str):
    '''
    parse cookit and load user
    :param cookie_str:
    :return:
    '''
    if not cookie_str:
        return None
    L = cookie_str.split('-')  # see '-'.join(L)
    if(len(L)) !=3:
        return None
    id, expire_time, digest = L #unpack
    if int(expire_time) < int(time.time()):
        return None
    user = yield from User.find(id)
    if user is None:
        return None
    hash_str = 'userid:%s password:%s max_age:%s secert_key:%s' % (user.id, user.passwd, expire_time, _COOKIE_KEY)
    if hashlib.sha1(hash_str.encode('utf-8')).hexdigest() != digest:
        logging.info('invalid digest in cookie')
        return None
    user.passwd = user.passwd + "*cookie"
    return user

@get('/')
def index(request):
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id='1',name='Test Blog', summary=summary, created_at=time.time()-120),
        Blog(id='2',name='New Blog', summary=summary, created_at=time.time()-3600),
        Blog(id='3',name='Learn Python', summary=summary, created_at=time.time()-7200),
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }


@get('/register')
def api_register_new(request):
    return {
        '__template__': 'register.html'
    }

@get('/signin')
def signin(request):
    return {
        '__template__': 'signin.html'
    }

def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        print(e)
        p = 1
    if p<1:
        p = 1
    return p

@get('/api/users')
def api_get_users(page='1'):
    page_index = get_page_index(page)
    '''
    SELECT count(id) _num_ FROM `users`
    '''
    num = yield from User.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p,users=())
    '''
    select `id`, `email`,`passwd`,`admin`,`name`,`image`,`created_at` from `users` order by created_at desc limit 0, 10
    '''
    users = yield from User.findAll(orderBy='created_at desc', limit=(p.offset,p.limit))
    '''  passwd = StringField(ddl='varchar(50)') '''
    for u in users:
        u.passwd = u.passwd + '**'
    return dict(page=p, users=users)


_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

@post('/api/users')
def api_register_user(*,email,name,password):
    if name is None or name.strip() is None:
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not password or not _RE_SHA1.match(password):
        raise APIValueError('password')
    u = yield from User.findAll('email=?', [email])
    if len(u) > 0:
        raise APIError('register:failed, ', 'email', 'already exist.')
    sha1_password = '%s %s' % (name.strip(), password)
    u = User(email=email,name=name.strip(),passwd=hashlib.sha1(sha1_password.encode('utf-8')).hexdigest(),image='')
    yield from u.save()
    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(u,86400),  max_age=86400, httponly=True)
    u.passwd = u.passwd + '*'
    r.content_type = 'application/json'
    r.body = json.dumps(u, ensure_ascii=False).encode('utf-8')
    return r

@post('/api/authenticate')
def authenticate(*, email,password ):
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email', 'Invalid email')
    if not password:
        raise APIValueError('password', 'invalid password')
    user = yield from User.findAll('email=?', [email])  #return email list
    if len(user) == 0:
        raise APIValueError('email', 'email is not exist')
    user = user[0]

    # check password
    # register.html-> password: CryptoJS.SHA1(email + ':' + this.password1).toString()
    sha1 = hashlib.sha1()
    sha1.update(user.email.encode('utf-8'))
    sha1.update(b':')
    sha1.update(password.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('password', 'password verification failed')

    # authentication OK, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user,86400), max_age=86400, httponly=True)
    user.passwd = user.passwd + '*'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r





