#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt
import asyncio
import time

def reader_generator():
    print('      reader_generator start')
    # 模拟从文件读取数据的生成器
    for i in range(4):
        print('      !going to yield << %s in Generator: i=%s' % (i,i))
        x = yield '<< %s' % i
        time.sleep(1)
        print('      -after yield << %s  in Generator: i=%s' % (i,i))
        print('      -after yield x=%s' % x)
    print('      reader_generator end')
    return 9



def reader_distributer(gen):
    print('   reader_distributer start')
    n = 0
    # 循环迭代从reader_generator产生的数据
    #for value in gen:
    #    print('   !going to yield (%s) in Distributer' % (value+'+'+ str(n)))
    #    yield value+'+'+ str(n)
    #    print("   -after yield (%s) in Distributer" % (value+'+'+ str(n)))
    #    n += 1
    y = yield from gen
    print('   reader_distributer y=%s' % y)
    print('   reader_distributer end')

print('start to learn yield.')
r = reader_distributer(reader_generator())
#r= reader_generator()
print('start the loop.')
for i in r:
    print('start to do something...')
    print(i)
    print('start to send something...')
    r.send(dt.datetime.now())
    print('going to next loop...')
print('end to learn yield.')