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