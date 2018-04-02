#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Tianhe'

'''
app monitor web application
'''

import os, sys,time,subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def log(s):
    print('[monitor]: %s' % s)

class MyFileSystemEventHandler(FileSystemEventHandler):
    def __init__(self, fn):
        super(MyFileSystemEventHandler,self).__init__()
        self.reset = fn

    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            log('source file is changed: %s' % event.src_path)
            self.reset()

process = None
cmd = ['echo','ok']

def kill_process():
    global process,cmd
    if process:
        log('Kill process [%s]' % process.pid)
        process.kill()
        process.wait()
        log('process ended with code %s' % process.returncode)
        process = None

def start_process():
    global process,cmd
    log('start process [%s]...' % ' '.join(cmd))
    process = subprocess.Popen(cmd,stdin=sys.stdin,stdout=sys.stdout,stderr=sys.stderr)

def restart_process():
    kill_process()
    start_process()
    print('restared process.')

def start_watch(path, callback):
    observer = Observer()
    observer.schedule(MyFileSystemEventHandler(restart_process),path, recursive=True)
    observer.start()
    log('start watching dictory [%s]' % path)
    start_process()
    try:
        while(True):
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    print('observer.join()...')
    observer.join()

if __name__ == '__main__':
    print('sys.argv=%s' % sys.argv)
    argv = sys.argv[1:]
    print(sys.argv[0:])
    argv = ['test_async_database.py']
    if not argv:
        print('usage: app_monitor <your_py.py>')
        #exit(0)
    if argv[0]!='python':
        argv.insert(0,'python')
    #if argv[0] != 'python3':
    #    argv.insert(0,'python3')
    cmd = argv
    path = os.path.abspath('.')
    start_watch(path,None)




