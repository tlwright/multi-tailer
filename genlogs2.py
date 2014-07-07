#!/usr/bin/env python3 

import datetime, time, random

o1 = open("log1.log", 'a')
o2 = open("log2.log", 'a')
o3 = open("log3.log", 'a')
o4 = open("log4.log", 'a')

def genlog(r):
    fmt = "%a %b %d %H:%M:%S %Z %Y"
    now = datetime.datetime.today()
    ts = now.strftime(fmt)
    j = '{"content":{"key1":"value1","key2":{"key2.1":"value2.1","key2.2":"value2.1"},"key3":"Value3"}'
    n = '"note": "note content"'
    x = 'ERROR: could not render object: no such field!\n'
    if r == 0:
        return j + ',' + n + '}\n'
    elif r == 1:
        return j + ',' + n + ',' + '"at":"' + ts  + '"}\n'
    elif r == 2:
        return j + ',' + '"at":"' + ts + '"}\n'
    else:
        return x

random.seed()

for i in range(10):
    for o in (o1, o2, o3, o4):
        n = random.randint(0,3)
        a = genlog(n)
        o.write(a)
        o.flush()
        time.sleep(random.random())

o1.close()
o2.close()
o3.close()
o4.close()
