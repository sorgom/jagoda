import re

rxFind = re.compile('^ *CREATE +(PROCEDURE|FUNCTION) +(\w+)', re.I | re.M)

sqf = 'sql/init_functions.sql'

with open(sqf, 'r') as fh:
    cont = fh.read()
    fh.close()
    grant = []
    drop  = []
    for tp, fc in rxFind.findall(cont):
        grant.append("GRANT EXECUTE ON %-9s jagoda.%-22s TO 'aut'@'%%';" %  (tp, fc))
        drop.append("DROP %-9s IF EXISTS %s;" % (tp, fc))
    
    # map(print, grant)
    print('\n'.join(grant))

    print('======================================================')

    print('\n'.join(drop))



