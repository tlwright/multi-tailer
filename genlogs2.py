#!/usr/bin/env python3 

import datetime, time

o1 = open("log1.log", 'a')
o2 = open("log2.log", 'a')
o3 = open("log3.log", 'a')
o4 = open("log4.log", 'a')
print("o1.fileno()=",o1.fileno()) # 3
print("o2.fileno()=",o2.fileno()) # 4

fmt = "%a %b %d %H:%M:%S %Z %Y"

j = '{"content":{"key1":"value1","key2":{"key2.1":"value2.1","key2.2":"value2.1"},"key3":"Value3"}'
n = '"note": "note content"'
x = 'ERROR: could not render object: no such field!\n'

for i in range(10):
    a = j + ',' + n + '}\n'
    o1.write(a)
    o1.flush()
    time.sleep(0.7)
    now = datetime.datetime.today()
    ts = now.strftime(fmt)
    a = j + ',' + n + ',' + '"at":"' + ts  + '"}\n'
    o2.write(a)
    o2.flush()
    time.sleep(0.7)
    a = j + ',' + '"at":"' + ts + '"}\n'
    o3.write(a)
    o3.flush()
    time.sleep(0.7)
    a = x
    o4.write(a)
    o4.flush()
    time.sleep(0.7)

o1.close()
o2.close()
o3.close()
o4.close()
