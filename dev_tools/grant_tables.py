import re
from replGenSql import *
import paths


colsNoUpd = 'ID ILC TPC STDABLE OBJ IMG UID TNT USR CAP'
rxNoUpd = re.compile('^(?:' +  '|'.join(colsNoUpd.split()) + ')$')
rxRoot = re.compile(r'^\s*--\s+ROOT')
rxAdd  = re.compile(r'^\s*--\s+ADD')

grantAut = 'select, insert, delete'
grantMin = 'select'
grantAdd = 'select, insert'

maxGrantLen = max(map(len, (grantAut, grantMin, grantAdd)))

noCols = 'primary foreign unique index'
rxNo = re.compile('^(?:' +  '|'.join(noCols.split()) + ')$', re.I )
rxFix = re.compile('-- *FIX\\b')
rxCreate = re.compile('^ *create +table +(\w+)\s*\((.*?)\n\)', re.M | re.S | re.I)

rxCol = re.compile('^ *(\w+)(.*)', re.M)

class Table(object):
    def __init__(self, name, cont):
        self.name = name
        self.nameLen = len(name)
        self.grant = grantMin if rxRoot.search(cont) else grantAdd if rxAdd.search(cont) else grantAut
        self.updatable = not (rxRoot.search(cont) or rxAdd.search(cont))
        self.updateCols = None
        self.updateStr = ''
        self.updateLen = 0
        if (self.updatable):
            self.updateCols = [
                col for col, rem in rxCol.findall(cont) 
                if not (rxFix.search(rem) or rxNoUpd.match(col) or rxNo.match(col))
            ]
            self.updatable = len(self.updateCols) > 0
        if self.updatable:
            self.updateStr = ', '.join(self.updateCols)
            self.updateLen = len(self.updateStr)


def processFile(tblFile:str, initUsr=False):
    with open(tblFile, 'r') as fh:
        txt = fh.read()
        fh.close()
        tables = [Table(name, cont) for name, cont in rxCreate.findall(txt)]
        maxNameLen   = max(t.nameLen for t in tables)
        maxUpdateLen = max(t.updateLen for t in tables)
        grantStr  = f'grant %-{maxGrantLen}s on %s.%-{maxNameLen}s to %s;'
        updateStr = f'grant update (%-{maxUpdateLen}s) on %s.%-{maxNameLen}s to %s;'

        grants = [ grantStr % (t.grant, DB, t.name, USR) for t in tables]

        if initUsr: grants = iniitUsr() + grants

        updates = [ 
            updateStr % (t.updateStr, DB, t.name, USR) for t in tables
            if t.updatable 
        ]
        txt = replGenSql('GRANT', grants + updates, txt)

        with open(tblFile, 'w') as fh:
            fh.write(txt)


if __name__ == '__main__':

    processFile('sql/01_init_database_and_tables.sql', True)