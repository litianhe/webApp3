#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Tianhe'

'web url handlers'

from www.coroweb import get,post
from www.models import User,Blog,Comment
from www.apis import Page
import time

@get('/test')
def homePage(request):
    users = yield from User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }

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
def api_get_users(*, page='1'):
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
    users = yield from User.findAll(orderBy='created_at desc', limit=(p.offset,p.limit,))
    '''  passwd = StringField(ddl='varchar(50)') '''
    for u in users:
        u.passwd = u.passwd + '**'
    return dict(page=p, users=users)


