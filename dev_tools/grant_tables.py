import re
from replGenSql import replGenSql, USR, DB


colsNoUpd = 'ID ILC TPC STDABLE OBJ IMG UID TNT ENT USR'
rxNoUpd = re.compile('^(?:' +  '|'.join(colsNoUpd.split()) + ')$')
rxRoot = re.compile('^\s*--\s+ROOT')

grantAut = 'select, insert, delete'
grantMin = 'select'

noCols = 'primary foreign unique index'
rxNo = re.compile('^(?:' +  '|'.join(noCols.split()) + ')$', re.I )
rxFix = re.compile('-- *FIX\\b')




rxCreate = re.compile('^ *create +table +(\w+)\s*\((.*?)\n\)', re.M | re.S | re.I)

rxCol = re.compile('^ *(\w+)(.*)', re.M)

tblFile = 'sql/01_init_tables.sql'

def procUpdate(table, cont):
    cols = [
        col for col, rem in rxCol.findall(cont)
        if not (rxFix.search(rem) or rxNoUpd.match(col) or rxNo.match(col))
    ]
    if not cols: return None 
    return "grant update (%-40s) on %s.%-20s to %s;" % (', '.join(cols), DB, table, USR)

def procGrant(table, cont):
    grant = grantMin if rxRoot.search(cont) else grantAut
    return "grant %-30s on %s.%-20s to %s;" % (grant, DB, table, USR)

with open(tblFile, 'r') as fh:
    cont = fh.read()
    findings = list(rxCreate.findall(cont))
    updates = [
        update for update in [ procUpdate(table, cont) for table, cont in findings ]
        if update
    ]
    grants = [ procGrant(table, cont) for table, cont in findings ]

    cont = replGenSql('GRANT', grants + updates, cont)

    with open(tblFile, 'w') as fh:
        fh.write(cont)