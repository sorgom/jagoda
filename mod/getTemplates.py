# make full templates of ajax request templates

from glob import glob
import re
from os import path

def genTemplates():
    add_tp = '{% extends \'aut_base.htm\' %}\n{% block content %}'
    add_bt = '{% endblock %}'

    tpath = 'templates'
    pattern = '_*.htm'
    rxNm = re.compile('^_+')
    rxLn = re.compile('[ \t]+$', re.M)

    files = glob(path.join(tpath, pattern))

    for file in files:
        with open(file, 'r') as fh:
            cont = fh.read()
            fh.close()
            newcont = '\n'.join([add_tp, rxLn.sub('', cont.strip()), add_bt])
            outFile = path.join(tpath, rxNm.sub('GEN_', path.basename(file), 1))
            
            print(outFile)

            fh = open(outFile, 'w')
            fh.write(newcont)
            fh.close()

if __name__ == '__main__':
    genTemplates()
