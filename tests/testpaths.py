from os import path
import sys

MY_DIR = path.dirname(__file__)

TEST_REL_DIRS = ['..']

mydir = path.dirname(__file__)
for reldir in TEST_REL_DIRS:
    addPath = path.abspath(path.join(mydir, reldir))
    if not addPath in sys.path:
        sys.path.append(addPath)

        

