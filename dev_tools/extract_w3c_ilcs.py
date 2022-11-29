import re, codecs, json
import paths
from mod.google import translate

rxTr = re.compile('<tr>(.*?)</tr>', re.M | re.S)
rxTd = re.compile('<td>([a-z]{2})|([A-Z][a-z].*?)</td>', re.M | re.S)

infile = 'test_data/HTML ISO Language Code Reference.html'
outfile = 'support_data/ilcs.json'

ilcs = []
labels = []
res  = []
src = 'en'
dests = ['fr', 'de', 'hr', 'ko']
res = []

with codecs.open(infile, 'r', 'utf-8') as fh:
    html = fh.read()
    fh.close()
    for tr in rxTr.findall(html):
        # print(tr)
        tds = list(rxTd.findall(tr))
        if len(tds) == 2:
            ilc   = tds[1][0]
            label = tds[0][1]
            if ilc and label:
                res.append({src:label})
                ilcs.append(ilc)
                labels.append(label)

clab = ', '.join(labels)
print(clab)
ko = translate('en', 'fr', clab)
print(ko)

# for item in res:
#     text = item[src]
#     print(text, '...')
#     for dest in dests:
#         print(src, '->', dest)
#         try:
#             item[dest] = translate(src, dest, text)
#         except:
#             pass    
   
# with codecs.open(outfile, 'w', 'utf-8') as fh:
#     json.dump(res, fh)