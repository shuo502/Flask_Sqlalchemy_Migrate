# from sqlalchemy import *
#
# engine = create_engine()
import datetime
# a=datetime.datetime.now+(datetime.datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
print((datetime.datetime.utcnow()+datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=8, weeks=0)).strftime("%Y-%m-%d %H:%M:%S"))

a={"a":"1","b":"2","c":"3"}
if "a" in a:
    print(a["a"])
import datetime,time
print( int(time.time()))

b=[1,2,3,4,5,6]

b.remove(3)
print(b)
a.pop("a")
print(a)