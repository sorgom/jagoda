import paths



def intiCaps(file:str, data:list, ilc:str='en', offset:int=0):
    ld = len(data)
    delCap = f'delete from CAP where ID >= {offset} and ID < {offset + ld};'
    caps = ',\n'.join([
        f"({n + offset}, '{cpc}')" for n, [cpc, val] in enumerate(data)
    ])
    insCap = '\n'.join(['insert into CAP(ID, CPC) values', caps, ';'])
    elems = ',\n'.join([
        f"({n + offset}, '{ilc}', '{val}')" for n, [cpc, val] in enumerate(data)
    ])
    insElem = '\n'.join(['insert into CAP_ELEM values', elems, ';'])
    with open(file, 'w') as fh:
        fh.write('\n'.join([delCap, insCap, insElem]))

if __name__ == '__main__':

    intiCaps('sql/06_gen_init_caps.sql', [
            ['CHG PWD', 'change password'],
            ['CR NEW TTL', 'create new title'],
            ['DIMS', 'dimensions'],
            ['ED OBJ', 'edit object'],
            ['IMGS', 'images'],
            ['LBL PWD 1', 'new password'],
            ['LBL PWD 2', 'new password repeated'],
            ['LOGIN', 'login'],
            ['LOGOUT', 'logout'],
            ['NEW OBJ', 'new object'],
            ['OBJ KIND', 'object kind'],
            ['OBJ KINDS', 'object kinds'],
            ['OBJ', 'object'],
            ['OBJS', 'objects'],
            ['PLH PWD 1', 'enter new password'],
            ['PLH PWD 2', 'repeat new password'],
            ['PUB WEB', 'publish on website'],
            ['RE-ORD OBJ IMGS', 're-order object images'],
            ['READY', 'ready'],
            ['STD TTLS', 'standard titles'],
            ['SUBMIT', 'submit'],
            ['TTL', 'title'],
            ['TTLS', 'titles'],
            ['UNUSED IMGS DRAG', 'unused images (drag up to assign)'],
            ['UPLOD OBJ IMGS', 'upload image files (klick or drag here)'],
            ['USE SDT TTL', 'use standard title'],
            ['USR OBJS', 'my recent objects'],
            ['YEAR', 'year'],
        ]
    )
    

