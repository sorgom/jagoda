from os import path, rename
import subprocess, re
from sys import argv
from glob import glob

tpldir = 'templates'
moddir = 'mod'

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

def _bnames(pOld, pNew):
    return list(map(path.basename, [pOld, pNew]))

def _replaceTemplates(old, new, inTempales=True):
    rx = re.compile(r'\b' + re.escape(old) + r'\b')
    for fpath in glob(f'{moddir}/*.py'):
        substSrc(fpath, rx, new)
    if inTempales:    
        for fpath in glob(f'{tpldir}/*.jade'):
            substSrc(fpath, rx, new)

def replaceTemplates(pOld, pNew):
    _replaceTemplates(*_bnames(pOld, pNew))

def renameTemplates(pOld, pNew):
    old, new = list(map(path.basename, [pOld, pNew]))
    oldp = path.join(tpldir, old)
    newp = path.join(tpldir, new)

    if path.exists(oldp) or path.exists(newp):
        _replaceTemplates(old, new)
        if not path.exists(newp):
            renGit(oldp, newp)

if __name__ == '__main__' and len(argv) > 2:
    renameTemplates(argv[1:3])