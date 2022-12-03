from os import path

a = { 1: 2, 3: 4, 5 : 6, 7: { 1: 3, 2:4}}
b = a

print(id(a))
print(id(b))

print(dir(a))

print('a:', a)
c = a.copy()

print('c:', c)

data = [[1, 2], [3, 4]]
fnd = { a:b for a, b in data }
print('fnd:', fnd)

def _bnames(pOld, pNew):
    return list(map(path.basename, [pOld, pNew]))

def _wumpel(old, new):
    print(old, new)

def wumpel(pOld, pNew):
    old, new = _bnames(pOld, pNew)
    _wumpel(*_bnames(pOld, pNew))

wumpel('D:/git/github/jagoda/tests/test_funtion_member.py', 'D:/git/github/jagoda/tests/test_mysql_connector.py')

def intify(data:dict, *args):
    for a in args:
        data[a] = 1 if data.get(a) else 0

data = { 'VAL':'on' }

intify(data, 'VAL', 'PUB')

print(data)