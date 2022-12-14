import re
from replGenSql import *

rxCreate = re.compile('^ *create +view +(\w+)', re.M | re.I)

class View(object):
    def __init__(self, name):
        self.name = name
        self.nameLen = len(name)

def processFile(vFile:str):
    with open(vFile, 'r') as fh:
        txt = fh.read()
        fh.close()
        views = [View(name) for name in rxCreate.findall(txt)]
        maxNameLen = max(v.nameLen for v in views)
        grantStr = f'grant select on %s.%-{maxNameLen}s to %s;'
        grants = [ grantStr % (DB, t.name, USR) for t in views]
        txt = replGenSql('GRANT', grants, txt)
        with open(vFile, 'w') as fh:
            fh.write(txt)


if __name__ == '__main__':

    processFile('sql/03_init_views.sql')