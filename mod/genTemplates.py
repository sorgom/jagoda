# make full templates of ajax request templates

from glob import glob
import re
from os import path
from mod.utilz import cleanFile
from mod.base import debug

TEMPLATES_FOLDER = 'templates'

def genTemplates(basehtm:str='aut_base.htm'):
    add_tp = "{%% extends '%s' %%}\n{%% block content %%}" % basehtm
    add_bt = '{% endblock %}'

    pattern = '_*.htm'
    rxNm = re.compile('^_+')

    for file in glob(path.join(TEMPLATES_FOLDER, pattern)):
        with open(file, 'r') as fh:
            cont = fh.read()
            fh.close()
            newcont = '\n'.join([add_tp, cont.strip(), add_bt])
            outFile = path.join(TEMPLATES_FOLDER, rxNm.sub('GEN_', path.basename(file), 1))
            debug(outFile)

            fh = open(outFile, 'w')
            fh.write(newcont)
            fh.close()

def cleanTemplates():
    pattern = '*.htm'
    for file in glob(path.join(TEMPLATES_FOLDER, pattern)):
        cleanFile(file)

if __name__ == '__main__':
    genTemplates()
    cleanTemplates()