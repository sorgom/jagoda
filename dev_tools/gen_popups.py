from glob import glob
from rename_templates import replaceTemplates, tpldir
from os import path
import paths 

text = """
{% extends 'popup.jade' %}
block content
    include <<>>
"""

for fp in glob(path.join(tpldir, '_*.jade')):
    int = path.basename(fp)
    pop = f'popup{int}'
    fpop = path.join(tpldir, pop)
    print(int, pop, fpop)
    with open(fpop, 'w') as fh:
        fh.write(text.replace('<<>>', int))
        replaceTemplates(int, pop, False)
