import re

USR = "'aut'@'%'"

def replGenSql(what:str, data:list, txt:str) -> str:
    rx = re.compile(f'^(-- GENERATED {what}>).*\n(-- <GENERATED {what})', re.M | re.S)
    print(rx)
    print('data', len(data))
    return rx.sub(r'\1\n' + '\n'.join(data) + r'\n\2', txt)

