#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def reader_generator():
    print('      reader_generator start')
    # 模拟从文件读取数据的生成器
    for i in range(4):
        print('      !going to yield << %s in Generator: i=%s' % (i,i))
        yield '<< %s' % i
        print('      -after yield << %s  in Generator: i=%s' % (i,i))
    print('      reader_generator end')


def reader_distributer(gen):
    print('   reader_distributer start')
    n = 0
    # 循环迭代从reader_generator产生的数据
    #for value in gen:
    #    print('   !going to yield (%s) in Distributer' % (value+'+'+ str(n)))
    #    yield value+'+'+ str(n)
    #    print("   -after yield (%s) in Distributer" % (value+'+'+ str(n)))
    #    n += 1
    yield from gen
    print('   reader_distributer end')

print('start to learn yield.')
r = reader_distributer(reader_generator())
print('start the loop.')
for i in r:
    print('start to print something...')
    print(i)
    print('going to next loop...')
print('end to learn yield.')

'''
start to learn yield.
start the loop.
   reader_distributer start
      reader_generator start
      !going to yield << 0 in Generator: i=0
start to print something...
<< 0
going to next loop...
      -after yield << 0  in Generator: i=0
      !going to yield << 1 in Generator: i=1
start to print something...
<< 1
going to next loop...
      -after yield << 1  in Generator: i=1
      !going to yield << 2 in Generator: i=2
start to print something...
<< 2
going to next loop...
      -after yield << 2  in Generator: i=2
      !going to yield << 3 in Generator: i=3
start to print something...
<< 3
going to next loop...
      -after yield << 3  in Generator: i=3
      reader_generator end
   reader_distributer end
end to learn yield.
'''