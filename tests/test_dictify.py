def qw(s:str):
    return list(s.split())

head = qw('DIM1 DIM2 DIM3')

data = [
    [1, 2, 3],
    [4, 5, 6],
    [6, 7, 8]
]

res = list(map(lambda a : dict(zip(head, a)), data))

print(res)

a = (1, 2, 3)
print(a[0])

def test(**args):
    print(type(args))
    print(args)

test(a=10, b=20)

#   dict by reference
def wumpel(d:dict):
    d.update({'a': 123})
    d['x'] = 222

dd = dict()

wumpel(dd)
print(dd)

c = 'ab\tc'
c = c.expandtabs(4).replace(' ', '_')
print(c)
c = 'abc\td'
c = c.expandtabs(4).replace(' ', '_')
print(c)

c = """abc\td
xy\tznn\twumpel
"""
c = c.expandtabs(4).replace(' ', '_')
print(c)
