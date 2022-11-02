

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

