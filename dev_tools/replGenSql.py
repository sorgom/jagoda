import re

USR = "'aut'@'%'"
DB = 'jagoda'
ROLE_AUT = "'author'"
ROLE_ADM = "'admin'"

def replGenSql(what:str, data:list, txt:str) -> str:
    rx = re.compile(f'^(-- GENERATED {what}>).*\n(-- <GENERATED {what})', re.M | re.S)
    return rx.sub(r'\1\n' + '\n'.join(data) + r'\n\2', txt)

