import re
import paths
from mod.config import *

USR = f"'{ DB_CONFIG['user']}'@'{DB_CONFIG['userhost']}'"
DB = DB_CONFIG['database']
# ROLE_AUT = "'author'"
# ROLE_ADM = "'admin'"

def replGenSql(what:str, data:list, txt:str) -> str:
    rx = re.compile(f'^(-- GENERATED {what}>).*\n(-- <GENERATED {what})', re.M | re.S)
    return rx.sub(r'\1\n' + '\n'.join(data) + r'\n\2', txt)

def iniitUsr():
    return [
        f"drop user if exists {USR};",
        f"create user {USR} identified by '{DB_CONFIG['password']}';"
    ]
