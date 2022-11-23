from os import path
import sys, re

# MY_DIR = path.dirname(__file__)

# TEST_REL_DIRS = ['..']

# mydir = path.dirname(__file__)
# for reldir in TEST_REL_DIRS:
#     addPath = path.abspath(path.join(mydir, reldir))
#     if not addPath in sys.path:
#         sys.path.append(addPath)

absp = '/static/img/mini/0000000.jpg'

paths = [
    '/static/img/mini/0000000.jpg',
    '/static/img/mini/0000001.jpg',
    '\\static/img/mini/0000002.jpg'
]

rxRel = re.compile('^[/\\\\]')

def relp(absp:str):
    return rxRel.sub('', absp)

print(relp(absp))

print(list(map(relp, paths)))

f1, f2, f3 = tuple(map(relp, paths))


print(f1, f2, f3)

data = [ rp for rp in map(relp, paths)]

print(data)