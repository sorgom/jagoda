
from ctypes.wintypes import CHAR
from flask_mysqldb import MySQL
from hashlib import md5 as libmd5
from mod.utilz import debug

__mydb__ = None


class MyDB(MySQL):

    def getNextId(self):
        return self.getNum('SELECT nextId();')

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

    ##  images
    def addObjectImg(self, objId:int, imgId:int):
        self.call(f'CALL addObjectImg({objId}, {imgId});')

    def addImg(self, imgId:int):
        self.call(f'CALL addImg({imgId});')

    def getObjectImgs(self, id:int):
        return [ 
            { 'id': id, 'ord': ord } for id, ord in self.get(f'CALL getObjectImgs({id});')
        ]

    def getNumObjectImgs(self, id:int):
        return self.getNum(f'SELECT getNumObjectImgs({id});')

    def setObjectImg(self, objId:int, imgId:int, ord:int):
        self.call(f'CALL setObjectImg({objId}, {imgId}, {ord});')

    def rmObjectImg(self, objId:int, imgId:int):
        self.call(f'CALL rmObjectImg({objId}, {imgId});')

    def getUnusedImgs(self):
        return [ 
            { 'id': id, 'ord': -1 } for id in self.getFirstCol(f'CALL getUnusedImgs();')
        ]

    ## subs

    def get(self, sql:str, commit=False):
        # debug('get sql:', sql)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        if commit:
            self.connection.commit() 
        return result

    def getOne(self, sql:str, commit=False):
        res = self.get(sql, commit)
        return res[0][0] if res else None
    
    def getNum(self, sql:str, *args) -> int:
        return int(self.getOne(sql, *args))

    def getFirstCol(self, sql:str, *args):
        return [ r[0] for r in self.get(sql, *args) ]

    def call(self, sql:str):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        cursor.close()
        self.connection.commit()

    def md5(self, val:str):
        return libmd5(val.encode('utf-8')).hexdigest()

    def mask(self, val:str):
        return val.replace('\\', '\\\\').replace('\'', '\\\'')

def setDB(app):
    global __mydb__
    if not __mydb__: __mydb__ = MyDB(app)
    return __mydb__

def db() -> MyDB:
    global __mydb__
    return __mydb__
