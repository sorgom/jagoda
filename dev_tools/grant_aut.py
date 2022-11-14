import re
from glob import glob

rxCreate = re.compile('^ *CREATE +(PROCEDURE|FUNCTION) +(\w+)', re.I | re.M)
rxGrant = re.compile('^(-- GENERATED GRANT>) *\n.*\n(-- <GENERATED GRANT)', re.M | re.S)
rxDrop  = re.compile('^(-- GENERATED DROP>) *\n.*\n(-- <GENERATED DROP)', re.M | re.S)

def repl(what:str, data:list, txt:str) -> str:
    rx = re.compile(f'^(-- GENERATED {what}>).*\n(-- <GENERATED {what})', re.M | re.S)
    print(rx)
    print('data', len(data))
    return rx.sub(r'\1\n' + '\n'.join(data) + r'\n\2', txt)

def genSql(fpath:str):
    with open(fpath, 'r') as fh:
        cont = fh.read()
        fh.close()
        grant = []
        drop  = []
        for tp, fc in rxCreate.findall(cont):
            grant.append("grant execute on %-9s jagoda.%-22s to 'aut'@'%%';" %  (tp.lower(), fc))
            drop.append("drop %-9s if exists %s;" % (tp.lower(), fc))

        txt = repl('GRANT', grant, repl('DROP', drop, cont))

        with open(fpath, 'w') as fh:
            fh.write(txt)

for sqf in glob('sql/*init*functions.sql'):
    genSql(sqf)

# sqfs = glob('sql/*init*functions.sql')
# print(sqfs)

# sqf = 'sql/init_functions.sql'


# with open(sqf, 'r') as fh:
#     cont = fh.read()
#     fh.close()
#     grant = []
#     drop  = []
#     for tp, fc in rxFind.findall(cont):
#         grant.append("grant execute on %-9s jagoda.%-22s to 'aut'@'%%';" %  (tp.lower(), fc))
#         drop.append("drop %-9s if exists %s;" % (tp.lower(), fc))
    

#     txt = rxGrant.sub(r'\1\n' + '\n'.join(grant) + r'\n\2', rxDrop.sub(r'\1\n' + '\n'.join(drop) + r'\n\2', cont))

#     print(txt)

#     # # map(print, grant)
#     # print('\n'.join(grant))

#     # print('======================================================')

#     # print('\n'.join(drop))



