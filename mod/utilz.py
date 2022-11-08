import re

RX_LN = re.compile('[ \t]+$', re.M)

def grep(pattern, names:list, *opts):
    if isinstance(pattern, re.Pattern):
        return [elem for elem in names if pattern.search(elem)]
    if isinstance(pattern, str):
        rx = re.compile(pattern, *opts)
        return grep(re.compile(pattern, *opts), names)
    return ['hello']

def cleanTxt(txt:str):
    return RX_LN.sub('', txt.strip()) + '\n'

def cleanFile(filename:str):
    with open(filename, 'r') as fh:
        cont = fh.read()
        fh.close()
        with open(filename, 'w') as fh:
            fh.write(cleanTxt(cont))
            fh.close()

def debug(*args):
    print(*args)

if __name__ == '__main__':
    names = ['Zardoz', 'Wumpel',' Wumpel', 'lola', 'Rumpel', 'FileDate']
    
    print(grep('^.*date', names, re.I))

    rx = re.compile('^.umpel')
    print(grep(rx, names))
