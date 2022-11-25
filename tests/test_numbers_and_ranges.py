import re

rxPrintStyle = re.compile('(\d+) *- *(\d+)|(\d+)')

#   ============================================================
#   database JSON   [[b, e], n] (print array pra)
#   user input      n n-m, n    (print string prs)
#   comparison set  { n, n, n } set is not sorted nor sortable


def prs2set(txt:str) -> set:
    res = []
    for b, e, n in rxPrintStyle.findall(txt):
        if b and e:
            res += list(range(int(b), int(e) + 1))
        else:
            res.append(int(n))
    return set(res)

def pra2set(pra:list) -> set:
    res = []
    for x in pra:
        if type(x) is list:
            res += list(range(x[0], x[-1] + 1))
        else:
            res.append(x)
    return set(res)

def set2pra(s:set) -> list:
    res = []
    tmp = []
    nxt = 0
    a = [n for n in s]
    a.sort()
    for n in a:
        if not tmp:
            tmp = [n]
        elif n == nxt:
            tmp.append(n)
        else:
            res += _a2x(tmp)
            tmp = [n]
        nxt = n + 1
    res += _a2x(tmp) 
    return res   

def pra2prs(pra:list):
    return ', '.join([_x2str(x) for x in pra])

def _x2str(x):
    return f'{x[0]}-{x[-1]}' if type(x) is list else str(x)

#   [[b, e]] or [n, n, n]
def _a2x(a:list) -> list:
    return [[a[0], a[-1]]] if len(a) > 2 else a


if __name__ == '__main__':

    text = '44, 1, 2-5 20 -22, 8- 12, 33'

    s = prs2set(text)
    print('s:', s)

    pra = set2pra(s)
    print('pra:', pra)

    s = pra2set(pra)
    print('s:', s)

    # a = s2a(s)
    # print('a:', a)

    # c = a2str(a)
    # print('c:', c)
