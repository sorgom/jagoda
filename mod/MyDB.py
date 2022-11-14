
from ctypes.wintypes import CHAR
from flask_mysqldb import MySQL
from hashlib import md5 as libmd5
from mod.utilz import debug
import random

__mydb__ = None


class MyDB(MySQL):

    def getNextId(self):
        return self.getNum('SELECT nextId();', commit=True)

    def getUsrId(self, usr:str, pwd:str):
        sql = "SELECT getUsrId('%s', '%s');" % (self.mask(usr), self.md5(pwd))
        return self.getNum(sql)

    def setPwd(self, id:int, pwd1:str, pwd2:str):
        if pwd1 != pwd2:
            return False
        sql = "CALL setPASS(%d, '%s');" % (id, self.md5(pwd1))
        self.call(sql)
        return True

    ## lanaguage support        

    # list of [icl, label]
    def getLangTable(self):
        return self.get('CALL getLangTable();')

    # list of [tpc, label]
    def getLangItemTypeTable(self):
        return self.get('CALL getLangItemTypeTable();')

    # label of given language type
    def getLangItemTypeLabel(self, tpc:str):
        return self.getOne(f'CALL getLangItemTypeLabel("{tpc}");')

    # type of language entry by id
    def getLangItemType(self, id:int):
        return self.getOne(f'CALL getLangItemType({id})')

    # create new language item
    def newLangItem(self, id:int, tpc:str):
        self.call(f'CALL newLangItem({id}, "{tpc}")')

    # list of [id, ilc, label]
    def getLangElemTable(self, tpc:str):
        return self.get(f'CALL getLangElemTable("{tpc}");')

    # list of [ilc, label]
    def getLangElem(self, id:int):
        return self.get(f'CALL getLangElem({id});')

    def setLangElem(self, id:int, ilc:str, label:str):
        self.call("CALL setLangElem(%d, '%s', '%s');" % (id, ilc, self.mask(label)))

    ## objects

    def isObject(self, id:int) -> bool:
        res = self.getNum(f'SELECT isObject({id});')
        return res > 0

    def getObject(self, id:int):
        return self.getDict('SELECT * FROM ')

    ##  images
    def addObjectImg(self, objId:int, imgId:int):
        self.call(f'CALL addObjectImg({objId}, {imgId});')

    def addImg(self, imgId:int):
        self.call(f'CALL addImg({imgId});')

    def getObjectImgs(self, id:int):
        return self.getDict(f'CALL getObjectImgs({id});')

    def getNumObjectImgs(self, id:int):
        return self.getNum(f'SELECT getNumObjectImgs({id});')

    def setObjectImg(self, objId:int, imgId:int, ord:int):
        self.call(f'CALL setObjectImg({objId}, {imgId}, {ord});')

    def rmObjectImg(self, objId:int, imgId:int):
        self.call(f'CALL rmObjectImg({objId}, {imgId});')

    def getUnusedImgs(self):
        return self.getDict('CALL getUnusedImgs();')

    def getImgFileMini(self, id:int):
        return self.getOne(f'SELECT imgFileMini({id});')
    def getImgFileFull(self, id:int):
        return self.getOne(f'SELECT imgFileFull({id});')
    def getImgFileExif(self, id:int):
        return self.getOne(f'SELECT imgFileExif({id});')
    def getImgFiles(self, id:int):
        return self.getOneRow(f'CALL imgFiles({id});')
    def getImgFolders(self):
        return self.getOneRow('CALL imgFolders();')

    def procCursor(self, sql:str, func, commit=False):
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
        cursor = self.connection.cursor()
        cursor.execute(sql)
        cursor.close()
        self.connection.commit()

    def md5(self, val:str):
        return libmd5(val.encode('utf-8')).hexdigest()

    def mask(self, val:str):
        return val.replace('\\', '\\\\').replace('\'', '\\\'')


    # create a lot of articles and titels
    def testData(self):
        self.call('delete from LANG_ITEM where TPC = "OT";')
        self.call('delete from OBJ;')
        # random language elements
        langs = self.getLangTable()
        slen = len(langs)
        ids = list(range(100000, 110000))
        ins = [f'({id}, "OT")' for id in ids]
        sql = ' '.join(['insert into LANG_ITEM(ID, TPC) values', ','.join(ins), ';'])
        self.call(sql)
        ins = [f'({id}, "{ilc}", "LE {id} {label}")' for id in ids for ilc, label in random.sample(langs, random.randrange(1, slen))]
        sql = ' '.join(['insert into LANG_ELEM values', ','.join(ins), ';'])
        self.call(sql)
        # random articles / objects
        offset = 2000
        sizes = [10, 20, 50, 300, 400, 1000]
        ins = [f'({id + offset}, {id}, {random.choice(sizes)}, {random.choice(sizes)}, {random.choice(sizes)})' for id in ids]
        sql = ' '.join(['insert into OBJ(ID, TITLE, DIM1, DIM2, DIM3) values', ','.join(ins), ';'])
        self.call(sql)
        ins = [f'({id + offset})' for id in ids]
        sql = ' '.join(['insert into ARTICLE(ID) values', ','.join(ins), ';'])
        self.call(sql)

def setDB(app):
    global __mydb__
    if not __mydb__: __mydb__ = MyDB(app)
    return __mydb__

def db() -> MyDB:
    global __mydb__
    return __mydb__
