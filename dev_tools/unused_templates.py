import re
from glob import glob
from os import path

rxHtm = re.compile('(\w+\.htm)')

calls = {}

def findInFile(fpath:str):
    global calls
    with open(fpath, 'r') as fh:
        cont = fh.read()
        for m in rxHtm.findall(cont):
            calls[m] = calls.get(m, 0) + 1


for fpath in glob('mod/*.py'):
     findInFile(fpath)

print(calls)

files = [ bn for bn in [ path.basename(f) for f in glob('templates/*.htm')] if not calls.get(bn) ]

for file in sorted(files):
    print(file)



