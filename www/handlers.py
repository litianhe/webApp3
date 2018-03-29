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
import markdown2
import asyncio

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

def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()

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


def user2cookie(user, max_age=86400):
    '''
    Generate cookie str by user.
    '''
    if not isinstance(user, User):
        raise Exception('error input user.')
    # build cookie string by: id-expires-digest
    expire_time = str(int(time.time() + max_age))
    hash_str = 'userid:%s password:%s max_age:%s secert_key:%s' % (user.id, user.passwd, expire_time, _COOKIE_KEY)
    digest = hashlib.sha1(hash_str.encode('utf-8')).hexdigest()
    L = [user.id, expire_time, digest]
    return '-'.join(L)

def text2html(text):
    lines = map( lambda s: '<p>%s</p>' % s.replace('&','&amp;').replace('<','&lt;').replace('>', '&gt;'), filter(lambda  s: s.strip()!='', text.split('\n')) )
    return ''.join(lines)
  
@asyncio.coroutine
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
def index(*, page='1'):
    page_index = get_page_index(page)
    num = yield from Blog.findNumber('count(id)')
    page = Page(num)
    if num == 0:
        blogs = []
    else:
        blogs = yield from Blog.findAll(orderBy='created_at desc', limit=(page.offset, page.limit))
    return {
        '__template__': 'blogs.html',
        'page': page,
        'blogs': blogs
    }

@get('/blog/{id}')
def get_blog(id):
    blog = yield from Blog.find(id)
    comments = yield from Comment.findAll('blog_id=?', [id], orderBy='created_at desc')
    for c in comments:
        c.html_content = text2html()
    blog.html_content = markdown2.markdown(blog.content)
    return {
        '__template__': 'blog.html',
        'blog': blog,
        'comments': comments
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

@post('/api/authenticate')
def authenticate(*, email, passwd):
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email', 'Invalid email')
    if not passwd:
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
    sha1.update(passwd.encode('utf-8'))
    # password encoding in api_authenticate
    #sha1_password = '%s:%s' % (email.strip(), passwd)
    #passwd = hashlib.sha1(sha1_password.encode('utf-8')).hexdigest()
    if user.passwd != sha1.hexdigest():
        print('authenticate: user.password=%s' % user.passwd)
        print('authenticate: user input   =%s' % sha1.hexdigest())
        raise APIValueError('password', 'password verification failed!')

    # authentication OK, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user,86400), max_age=86400, httponly=True)
    user.passwd = user.passwd + '*'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME,'deleted', max_age=0, httponly=True)
    logging.info('user has signed out')
    return r

@get('/manage/')
def manage():
    return 'redirect: /manage/comments'

@get('/manage/comments')
def manage_comments(request,*, page='1'):
    page_index = get_page_index(page)
    return {
        '__template__': 'manage_comments.html',
        'page_index' : page_index
    }

@get('/manage/blogs')
def manage_blogs(*, page='1'):
    return {
        '__template__': 'manage_blogs.html',
        'page_index': get_page_index(page)
    }

@get('/manage/blogs/create')
def manage_create_blog():
    return {
        '__template__': 'manage_blog_edit.html',
        'id':'',
        'action': '/api/blogs'
    }

@get('/manage/blogs/edit')
def manage_edit_blog(*,id):
    return {
        '__template__': 'manage_blog_edit.html',
        'id': id,
        'action': '/api/blogs/%s' % id
    }

@get('/manage/users')
def manage_users(*,page='1'):
    return {
        '__template__': 'manage_users.html',
        'page_index': get_page_index(page)
    }

@get('/api/comments')
def api_comments(*, page='1'):
    page_index = get_page_index(page)
    num = yield from Comment.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, comments=())
    comments = yield from Comment.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, comments=comments)

@post('/api/blogs/{id}/comments')
def api_create_comment(id, request, *, content):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    if not content or not content.strip():
        raise APIValueError('content')
    blog = yield from Blog.find(id)
    if blog is None:
        raise APIResourceNotFoundError('Blog')
    comment = Comment(blog_id=blog.id, user_id=user.id, user_name=user.name, user_image=user.image, content=content.strip())
    yield from comment.save()
    return comment

@post('/api/comments/{id}/delete')
def api_delete_comments(id, request):
    check_admin(request)
    c = yield from Comment.find(id)
    if c is None:
        raise APIResourceNotFoundError('Comment')
    yield from c.remove()
    return dict(id=id)

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
def api_register_user(*,email,name,passwd):
    if name is None or name.strip() is None:
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('password')
    u = yield from User.findAll('email=?', [email])
    if len(u) > 0:
        raise APIError('register:failed, ', 'email', 'already exist.')
    sha1_password = '%s:%s' % (email.strip(), passwd)
    print('api_register_user: passwd=%s ' % passwd)
    print('api_register_user: sha1_password=%s ' % sha1_password)
    u = User(email=email,name=name.strip(),passwd=hashlib.sha1(sha1_password.encode('utf-8')).hexdigest(),image='')
    yield from u.save()
    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(u,86400),  max_age=86400, httponly=True)
    u.passwd = u.passwd + '*'
    r.content_type = 'application/json'
    r.body = json.dumps(u, ensure_ascii=False).encode('utf-8')
    return r

@get('/api/blogs')
def api_get_blogs(*, page='1'):
    page_index = get_page_index(page)
    num = yield from Blog.findNumber('count(id)')
    p = Page(num, page_index)
    if num==0:
        return dict(page=p, blogs=())
    blogs = yield from Blog.findAll(orderBy='create_at desc', limit=(p.offset,p.limit))
    return dict(page=p, blogs=blogs)

@get('/api/blogs/{id}')
def api_get_blog(*, id):
    blog = yield from Blog.find(id)
    return blog


@post('/api/blogs')
def api_create_blog(request,*, name,summary,content):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'blog name can not be empty')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'blog summary can not be empty')
    if not content or not content.strip():
        raise APIValueError('content', 'blog content can not be empty')
    user = request.__user__
    blog = Blog(user_id = user.id , user_name = user.name ,user_image = user.image,
                name = name, summary=summary,content=content)
    yield from blog.save()
    return blog

@post('/api/blogs/{id}')
def api_update_blog(id,request,*, name,summary,content):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'blog name can not be empty')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'blog summary can not be empty')
    if not content or not content.strip():
        raise APIValueError('content', 'blog content can not be empty')
    user = request.__user__
    blog = yield from Blog.find(id)
    blog.name = name.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()
    yield from blog.update()
    return blog

@post('/api/blogs/{id}/delete')
def api_delete_blog(id,request):
    check_admin(request)
    blog = yield from Blog.find(id)
    yield from blog.remove()
    return dict(id=id)

