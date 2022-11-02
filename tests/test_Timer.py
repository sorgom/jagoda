from threading import Timer
from time import sleep


class TimerUser():
    def __init__(self, v1=10, v2=20):
        self.v1 = v1
        self.v2 = v2
        self.tmr = Timer(2, self.timerEvent)
        self.tmr.start() 

    def timerEvent(self):
        print('timer event')
        print('v1:', self.v1)
        print('v2:', self.v2)

class DerivedTimerUser(TimerUser):
    def __init__(self, v1=10, v2=50):
        super().__init__(v1, v2)

# def startup():
#     print('startup')

# t = Timer(2, startup)
# t.start()

# print('hello')
# sleep(10)
# print('bye')


# def foo():
#   global next_call
#   print(datetime.datetime.now())
#   next_call = next_call+1
#   threading.Timer( next_call - time.time(), foo).start()

# foo()

if __name__ == '__main__':
    tu = DerivedTimerUser(v1=1000)