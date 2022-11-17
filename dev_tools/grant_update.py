import re
from replGenSql import replGenSql, USR, DB


fixCols = 'ID ILC TPC STDABLE OBJ IMG'
rxFix = re.compile('^(?:' +  '|'.join(fixCols.split()) + ')$')
rxRoot = re.compile('^\s*--\s+ROOT')

grantAut = 'select, insert, delete'
grantMin = 'select'

noCols = 'primary foreign unique'
rxNo = re.compile('^(?:' +  '|'.join(noCols.split()) + ')$', re.I )


rxCreate = re.compile('^ *create +table +(\w+)\s*\((.*?)\n\)', re.M | re.S | re.I)

rxCol = re.compile('^ *(\w+)', re.M)

tblFile = 'sql/01_init_tables.sql'

def procUpdate(table, cont):
    if rxRoot.search(cont):
        return None
    cols = [
        col for col in rxCol.findall(cont)
        if not (rxFix.match(col) or rxNo.match(col))
    ]
    if not cols: return None 
    return "grant update (%-40s) on %s.%-20s to %s;" % (', '.join(cols), DB, table, USR)

def procGrant(table, cont):
    return None if rxRoot.search(cont) else "grant %-30s on %s.%-20s to %s;" % (grantAut, DB, table, USR)

with open(tblFile, 'r') as fh:
    cont = fh.read()
    findings = list(rxCreate.findall(cont))
    updates = [
        update for update in [ procUpdate(table, cont) for table, cont in findings ]
        if update
    ]
    grants = [ 
        grant for grant in [ procGrant(table, cont) for table, cont in findings ] 
        if grant
    ]

    cont = replGenSql('UPDATE', updates, cont)
    cont = replGenSql('GRANT', grants, cont)

    with open(tblFile, 'w') as fh:
        fh.write(cont)