import random

class Wumpel(object):
#    self.idFunc = lambda : 0

    def __init__(self, idFunc):
        self.idFunc = idFunc

    def hello(self):
        print(f'hello {self.__class__.__name__} {self.idFunc()}')

class OberWumpel(Wumpel):
    def __init__(self, code:str, *args):
         super().__init__(*args)
        

def idFunc1():
    random.seed()
    return random.randint(1, 10)


w1 = Wumpel(idFunc1)
w1.hello()

w2 = OberWumpel('object 123', idFunc1)
w2.hello()
