import json

test_data_file = 'test_data/das_oertlche.json'


with open(test_data_file) as fh:
    mxlen = 0
    data = json.load(fh)
    for item in data:
        addr = item['addr']
        if addr: mxlen = max(mxlen, len(addr))

    print(mxlen)