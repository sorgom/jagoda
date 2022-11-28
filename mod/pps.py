#   ============================================================
#   Print pages style (pps) notation
#   ============================================================
#   database JSON   [[b, e], n] (print page style list psl)
#   user input      n n-m, n    (print page style string pss)
#   comparison set  { n, n, n } set is neither sorted nor sortable
#   ============================================================

import re

PRINT_SYTLE_SEP = ' '

rxPss = re.compile('(\d+) *- *(\d+)|(\d+)')


#   print page style string to set
def ppss2set(txt:str) -> set:
    res = []
    for b, e, n in rxPss.findall(txt):
        if b and e:
            res += list(range(int(b), int(e) + 1))
        else:
            res.append(int(n))
    return set(res)

#   print page style list to set
def ppsl2set(ppsl:list) -> set:
    res = []
    for x in ppsl:
        if type(x) is list:
            res += list(range(x[0], x[-1] + 1))
        else:
            res.append(x)
    return set(res)

#   set to print page style list
def set2ppsl(s:set) -> list:
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

#   print page style list to print page style string
def ppsl2ppss(ppsl:list):
    return PRINT_SYTLE_SEP.join([
        f'{x[0]}-{x[-1]}' if type(x) is list else str(x)
        for x in ppsl
    ])

#   [[b, e]] or [n, n, n]
def _a2x(a:list) -> list:
    return [[a[0], a[-1]]] if len(a) > 2 else a


if __name__ == '__main__':

    ppss = '44, 1, 2-5 20 -22, 8- 12, 33'
    print('ppss:', ppss)

    s = ppss2set(ppss)
    print('s:', s)

    ppsl = set2ppsl(s)
    print('ppsl:', ppsl)

    s = ppsl2set(ppsl)
    print('s:', s)

    ppss = ppsl2ppss(ppsl)
    print('ppss:', ppss)
