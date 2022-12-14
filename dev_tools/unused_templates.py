import re
from glob import glob
from os import path, remove
from sys import argv

rxHtm = re.compile('(\w+\.jade)')

usage = {}

def findInFile(fpath:str):
    global usage
    with open(fpath, 'r') as fh:
        cont = fh.read()
        for match in rxHtm.findall(cont):
            usage[match] = usage.get(match, 0) + 1


for fpath in glob('mod/*.py'):
     findInFile(fpath)

for fpath in glob('templates/*.jade'):
     findInFile(fpath)

files = [ file for file in glob('templates/*.jade') if not usage.get(path.basename(file)) ]

for file in sorted(files):
    print(file)

if len(argv) > 1 and argv[1] == '-X':
   for file in files:
        remove(file)
