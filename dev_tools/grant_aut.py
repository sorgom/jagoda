import re
from glob import glob

rxFind = re.compile('^ *CREATE +(PROCEDURE|FUNCTION) +(\w+)', re.I | re.M)
rxGrant = re.compile('^(-- GENERATED GRANT>) *\n.*\n(-- <GENERATED GRANT)', re.M | re.S)
rxDrop  = re.compile('^(-- GENERATED DROP>) *\n.*\n(-- <GENERATED DROP)', re.M | re.S)

def genSql(fpath:str):
    with open(sqf, 'r') as fh:
        cont = fh.read()
        fh.close()
        grant = []
        drop  = []
        for tp, fc in rxFind.findall(cont):
            grant.append("grant execute on %-9s jagoda.%-22s to 'aut'@'%%';" %  (tp.lower(), fc))
            drop.append("drop %-9s if exists %s;" % (tp.lower(), fc))
        

        txt = rxGrant.sub(r'\1\n' + '\n'.join(grant) + r'\n\2', rxDrop.sub(r'\1\n' + '\n'.join(drop) + r'\n\2', cont))

        print(txt)    

sqfs = glob('sql/*init*functions.sql')
print(sqfs)

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



