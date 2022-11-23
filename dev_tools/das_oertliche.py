# A simple extractor of addresses from dasoertliche.de

import urllib.request
import re, json

rxClean = re.compile('^ *| *$|\r', re.M)
rxLines = re.compile('^\s*', re.M)
rxEntry = re.compile('^<!--  Eintrag  -->(.*?)<!--  end Eintrag  -->', re.M | re.S)
rxName  = re.compile('^<a.*\n(\w.*)', re.M)
rxAddr  = re.compile('^<address>(.*?)</address>', re.M | re.S)
rxTel   = re.compile('^<span class="hitlnk_call"> *(?:Tel\.|Fax|Tel/Fax)? *(.*?)</span>', re.M | re.S)

outfile = 'test_data/das_oertlche.json'

res = []

def procEntry(entry:str):
    global res
    mo1 = rxName.search(entry)
    mo2 = rxAddr.search(entry)
    mo3 = rxTel.search(entry)
    if mo1 and mo2 and mo3:
        name, addr, tel = mo1.group(1), mo2.group(1).strip(), mo3.group(1)
        if name and addr and tel:
            res.append({'name':name, 'addr': addr, 'tel':tel })
            print(name)
            print(addr)
            print(tel)

def procUrl(url):
    try:
        with urllib.request.urlopen(url) as fh:
            cont = rxLines.sub('', rxClean.sub('', fh.read().decode('utf8').replace('\t', ' ').replace('<br>', '')))
            for entry in rxEntry.findall(cont):
                procEntry(entry)
    except:
        pass

for offset in range(1,3368,25):
    url = f'https://www.dasoertliche.de/?zvo_ok=4&buc=&plz=8....&quarter=&district=&ciid=5140&fn=Peter&kw=&ci=M%C3%BCnchen&st=&radius=0&kgs=09162000000&buab=&zbuab=&form_name=search_nat_ext&recFrom={offset}'
    procUrl(url)

for offset in range(1,1383,25):
    url = f'https://www.dasoertliche.de/?zvo_ok=&buc=&plz=&quarter=&district=&ciid=&fn=Anne&kw=&ci=Berlin&st=&radius=0&kgs=&buab=&zbuab=&form_name=search_nat_ext&recFrom={offset}'
    procUrl(url)

with open(outfile, 'w') as fh:
    json.dump(res, fh)
