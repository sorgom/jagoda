import re
from glob import glob
from os import path, remove
from sys import argv

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

files = [ file for file in glob('templates/*.htm') if not calls.get(path.basename(file)) ]

for file in sorted(files):
    print(file)

if len(argv) > 1 and argv[1] == '-X':
   for file in files:
        remove(file)
