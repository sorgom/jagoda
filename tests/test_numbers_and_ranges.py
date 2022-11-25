import re

rx = re.compile('(\d+) *- *(\d+)|(\d+)')

text = '1, 2-5 20 -22, 8- 12,'

res = []
for b, e, n in rx.findall(text):
    if b and e:
        res += range(int(b), int(e) + 1)
    else:
        res.append(int(n))
    print(b, e, n) 

res = set(res)

print(list(res))

moved = [9, 11, 20]

rem = list(res - set(moved))
print(list(rem))

def aToStr(a:list):
    if len(a) > 3:
        return f'{a[0]}-{a[-1]}'
    return ', '.join([str(n) for n in a])
res = []
tmp = []
nxt = 0
for n in rem:
    if not tmp:
        tmp = [n]
    elif n == nxt:
        tmp.append(n)
        nxt = n + 1
    else:
        if (tmp): res.append(aToStr(tmp))
        tmp = [n]
    nxt = n + 1
if (tmp): res.append(aToStr(tmp))

res = ', '.join(res)

print(res)

# l1 = [1, 2, 3]
# l2 = [4, 3, 0]

# l3 = l1 + l2
# s1 = set(l1 + l2)
# print(l3)
# print(s1)