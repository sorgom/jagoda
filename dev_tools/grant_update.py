import re
from replGenSql import replGenSql, USR


fixCols = 'ID ILC TPC STDABLE OBJ IMG PRIMARY FOREIGN UNIQUE'
rxFix = re.compile('^(?:' +  '|'.join(fixCols.split()) + ')$' )
rxRoot = re.compile('^\s*--\s+ROOT')

noCols = 'PRIMARY FOREIGN UNIQUE'
rxNo = re.compile('^(?:' +  '|'.join(noCols.split()) + ')$', re.I )


rxCreate = re.compile('^ *create +table +(\w+)\s*\((.*?)\n\)', re.M | re.S | re.I)

rxCol = re.compile('^ *(\w+)', re.M)

tblFile = 'sql/01_init_tables.sql'

def proc(table, cont:str):
    if rxRoot.search(cont):
        return
    cols = [
        col for col in rxCol.findall(cont)
        if not (rxFix.match(col) or rxNo.match(col))
    ]
    if not cols: return None 
    return "grant update (%-40s) on jagoda.%-10s to %s;" % (', '.join(cols), table, USR)

with open(tblFile, 'r') as fh:
    cont = fh.read()
    data = [
        res for res in [ proc(table, cont) for table, cont in rxCreate.findall(cont) ]
        if res is not None
    ]
    cont = replGenSql('UPDATE', data, cont)

    with open(tblFile, 'w') as fh:
        fh.write(cont)