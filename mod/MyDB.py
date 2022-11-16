
from ctypes.wintypes import CHAR
from flask_mysqldb import MySQL
from hashlib import md5 as libmd5
from mod.utilz import debug
import random

__mydb__ = None

class MyDB(MySQL):

    def getNextId(self):
        return self.getNum('select nextId();', commit=True)

    def getUsrId(self, usr:str, pwd:str):
        sql = "select getUsrId('%s', '%s');" % (self.mask(usr), self.md5(pwd))
        return self.getNum(sql)

    def setPwd(self, id:int, pwd1:str, pwd2:str):
        if pwd1 != pwd2:
            return False
        self.call(f'update USR set PASS = "{self.md5(pwd1)}" where ID = {id};')
        return True

    ## lanaguage support        

    # get list of current languages
    # list of [icl, label]
    def getLangTable(self):
        return self.get('select ILC, LABEL from LANG order by ORD;')

    # get list of item types
    # list of [tpc, label]
    def getLangItemTypeTable(self):
        return self.get('select * from LANG_ITEM_TYPE;')

    # get label of given language type
    def getLangItemTypeLabel(self, tpc:str):
        return self.getOne(f'select LABEL from LANG_ITEM_TYPE where TPC = "{tpc}" limit 1;')

    # get lang item type of language entry by id
    def getLangItemType(self, id:int):
        return self.getOne(f'select TPC from LANG_ITEM where ID = {id} limit 1;')

    # create new language item (head)
    def newLangItem(self, id:int, tpc:str):
        self.call(f'insert into LANG_ITEM(ID, TPC) values ({id}, "{tpc}")')

    # get table fo lang items of given type
    def getLangItems(self, tpc:str):
        return self.get(f'call getLangElemTable("{tpc}");')

    # get elements of a lang item
    # list of [ilc, label]
    def getLangItem(self, id:int):
        return self.get(f'select ILC, LABEL from LANG_ELEM_ORD where ID = {id} order by ORD;')

    # get head (info) of language item
    def getLangItemInfo(self, id:int):
        return self.getDict(f'select * from LANG_ITEM_STD where ID = {id} limit 1;')[0]

    # get head (info) of for a new language item
    def getNewLangItemInfo(self, tpc:str):
        return self.getDict(f'select STDABLE, 0 as STD from LANG_ITEM_TYPE where TPC = "{tpc}" limit 1;')[0]

    # set elements of a lang item
    def setLangItem(self, id:int, data:list):
        self.multi('LANG_ELEM', [f'({id}, \'{ilc}\', \'{self.mask(label)}\')' for ilc, label in data])
        self.call(f"delete from LANG_ELEM where ID = {id} and LABEL = '';")
        self.call(f'update LANG_ITEM set TST = CURRENT_TIMESTAMP where ID = {id};')
    
    # change lang item standard flag
    def setLangItemStd(self, id:int, std:int):
        debug(f'setLangItemStd({id}, {std});')
        self.call(f'call setLangItemStd({id}, {1 if std else 0});')

    ## objects

    def getObject(self, id:int):
        return self.getDict('select * FROM ')

    ##  images
    def addObjectImg(self, objId:int, imgId:int):
        self.call(f'call addObjectImg({objId}, {imgId});')

    def addImg(self, imgId:int):
        self.call(f'replace into IMG(ID) values ({imgId});')

    def getObjectImgs(self, objId:int):
        return self.getDict(f'select IMG as ID, ORD, imgFileMini(IMG) as SRC from OBJ_IMG where OBJ = {objId} order by ORD;')
    
    def setObjectImg(self, objId:int, imgId:int, ord:int):
        self.call(f'replace into OBJ_IMG values ({objId}, {imgId}, {ord});')

    def rmObjectImg(self, objId:int, imgId:int):
        self.call(f'delete from OBJ_IMG where OBJ = {objId} and IMG = {imgId};')

    def getUnusedImgs(self):
        return self.getDict('call getUnusedImgs();')

    def getImgFileMini(self, id:int):
        return self.getOne(f'select imgFileMini({id});')
    def getImgFileFull(self, id:int):
        return self.getOne(f'select imgFileFull({id});')
    def getImgFileExif(self, id:int):
        return self.getOne(f'select imgFileExif({id});')
    def getImgFiles(self, id:int):
        return self.getOneRow(f'call imgFiles({id});')
    def getImgFolders(self):
        return self.getOneRow('call imgFolders();')

    def procCursor(self, sql:str, func, commit=False):
        debug('SQL:', sql)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        res = func(cursor)
        cursor.close()
        if commit:
            self.connection.commit() 
        return res

    def getOneRow(self, sql:str, **args):
        return self.procCursor(sql, lambda c : c.fetchone(), **args)

    def mkDict(self, cur):
        desc = [ d[0].lower() for d in cur.description ]
        return list(map(lambda a : dict(zip(desc, a)), cur.fetchall()))

    def getDict(self, sql:str, **args):
        return self.procCursor(sql, self.mkDict, **args)

    def get(self, sql:str, **args):
        return self.procCursor(sql, lambda c : c.fetchall(), **args)

    def getOne(self, sql:str, **args):
        res = self.getOneRow(sql, **args)
        return res[0] if res else None
    
    def getNum(self, sql:str, **args) -> int:
        return int(self.getOne(sql, **args))

    def getFirstCol(self, sql:str, **args):
        return [ r[0] for r in self.get(sql, **args) ]

    def call(self, sql:str):
        debug('call:', sql)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        cursor.close()
        self.connection.commit()

    def md5(self, val:str):
        return libmd5(val.encode('utf-8')).hexdigest()

    def mask(self, val:str):
        return val.replace('\\', '\\\\').replace('\'', '\\\'')

    def multi(self, tablefields:str, ins:list, insert:bool=False):
        cir = 'insert' if insert else 'replace'
        head = f'{cir} into {tablefields} values'
        sql  = '\n'.join([head, ','.join(ins), ';'])
        self.call(sql) 

    # create a lot of articles and titels
    def testData(self):
        self.call('delete from LANG_ITEM where TPC = "OT";')
        self.call('delete from OBJ;')
        # random language elements
        langs = self.getLangTable()
        slen = len(langs)
        ids = list(range(100000, 110000))
        self.multi('LANG_ITEM(ID, TPC)', [f'({id}, "OT")' for id in ids], insert=True)
        self.multi('LANG_ELEM', [f'({id}, "{ilc}", "LE {id} {label}")' for id in ids for ilc, label in random.sample(langs, random.randrange(1, slen))], insert=True)
        # random articles / objects
        offset = 2000
        sizes = [10.5, 20.7, 50, 300, 400, 1000, 14.7]
        ins = [f'({id + offset}, {id}, {random.choice(sizes)}, {random.choice(sizes)}, {random.choice(sizes)})' for id in ids]
        self.multi('OBJ(ID, TITLE, DIM1, DIM2, DIM3)', ins, True)
        self.multi('ARTICLE(ID)', [f'({id + offset})' for id in ids])
        self.call('call initSeq();')

def setDB(app):
    global __mydb__
    if not __mydb__: __mydb__ = MyDB(app)
    return __mydb__

def db() -> MyDB:
    global __mydb__
    return __mydb__
