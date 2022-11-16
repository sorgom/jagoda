from replGenSql import replGenSql, USR
import re
from glob import glob

rxCreate = re.compile('^ *CREATE +(PROCEDURE|FUNCTION) +(\w+)', re.I | re.M)

def genSql(fpath:str):
    with open(fpath, 'r') as fh:
        cont = fh.read()
        fh.close()
        grant = []
        drop  = []
        for tp, fc in rxCreate.findall(cont):
            grant.append("grant execute on %-9s jagoda.%-22s to %s;" %  (tp.lower(), fc, USR))
            drop.append("drop %-9s if exists %s;" % (tp.lower(), fc))

        cont = replGenSql('GRANT', grant, replGenSql('DROP', drop, cont))
        # print(txt)

        with open(fpath, 'w') as fh:
            fh.write(cont)

for sqf in glob('sql/*init*functions.sql'):
    genSql(sqf)

