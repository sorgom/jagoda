from os import path, rename
import subprocess, re
from sys import argv
from glob import glob
tpldir = 'templates'

def isGit(fpath:str):
    return True if subprocess.run(f'git ls-files {fpath}', capture_output=True).stdout else False

def renGit(oldpath:str, newpath:str):
    if isGit(oldpath):
        subprocess.run(f'git mv {oldpath} {newpath}')
    else:
        rename(oldpath, newpath)

def substSrc(fpath:str, rx:re.Pattern, new:str) -> bool:
    with open(fpath) as fh:
        cont = fh.read()
        if (rx.search(cont)):
            res = rx.sub(r'\1' + new, cont)
            print('####', fpath)
            fh.close()
            with open(fpath, 'w') as fh:
                fh.write(res)
            return True
    return False

if len(argv) > 2:
    old, new = list(map(path.basename, argv[1:3]))

    oldp = path.join(tpldir, old)
    newp = path.join(tpldir, new)

    if path.exists(oldp) and not path.exists(newp):
        rx = re.compile('\\b(GEN)?' + re.escape(old) + '\\b')
        for fpath in glob('mod/*.py'):
            substSrc(fpath, rx, new)

        renGit(oldp, newp)
