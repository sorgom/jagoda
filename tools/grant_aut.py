import re

rxFind = re.compile('^ *CREATE +(PROCEDURE|FUNCTION) +(\w+)', re.I | re.M)

sqf = 'sql/init.sql'

with open(sqf, 'r') as fh:
    cont = fh.read()
    fh.close()
    res = [
        "GRANT EXECUTE ON %-10s jagoda.%-22s TO 'aut'@'%%';" %  (tp, fc)
        for tp, fc in rxFind.findall(cont)
    ]
    print('\n'.join(res))


