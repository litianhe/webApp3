#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import asyncio

@asyncio.coroutine
def hello(n):
    print('start task#%s %s seconds!' % (n,n) )
    yield from asyncio.sleep(n)
    print('%s second passes in task %s, wait again %s!' % (n,n,n) )
    yield from asyncio.sleep(n)
    print('%s second passes again in task#%s!' % (n,n) )

loop = asyncio.get_event_loop()
tasks = [hello(2), hello(1),hello(5),hello(4),hello(3)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

'''
Hello 5! (<_MainThread(MainThread, started 199256)>)
Hello 2! (<_MainThread(MainThread, started 199256)>)
Hello 1! (<_MainThread(MainThread, started 199256)>)
Hello 4! (<_MainThread(MainThread, started 199256)>)
Hello 3! (<_MainThread(MainThread, started 199256)>)
Hello again 1! (<_MainThread(MainThread, started 199256)>)
Hello again 2! (<_MainThread(MainThread, started 199256)>)
Hello again 3! (<_MainThread(MainThread, started 199256)>)
Hello again 4! (<_MainThread(MainThread, started 199256)>)
Hello again 5! (<_MainThread(MainThread, started 199256)>)

start task#5 5 seconds!
start task#2 2 seconds!
start task#1 1 seconds!
start task#4 4 seconds!
start task#3 3 seconds!
1 second passes in task 1, wait again 1!
2 second passes in task 2, wait again 2!
1 second passes again in task#1!
3 second passes in task 3, wait again 3!
4 second passes in task 4, wait again 4!
2 second passes again in task#2!
5 second passes in task 5, wait again 5!
3 second passes again in task#3!
4 second passes again in task#4!
5 second passes again in task#5!
'''