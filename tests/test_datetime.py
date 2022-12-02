from datetime import date, timedelta, datetime
from time import time

now = time()

print(now)
dtn = datetime.now()

print(dtn)

td = timedelta(minutes=10)

print(td)

dtn -= td
print(dtn)

mins = 10000
print(dtn -  timedelta(minutes=mins))