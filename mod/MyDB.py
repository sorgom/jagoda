
from ctypes.wintypes import CHAR
from flask_mysqldb import MySQL
from hashlib import md5 as libmd5

class MyDB(MySQL):

    def nextLangId(self):
        return self.nextSeq('LANG')

    def getId(self, usr:str, pwd:str):
        sql = "SELECT autID('%s', '%s');" % (self.mask(usr), self.md5(pwd))
        return int(self.getOne(sql))

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
        self.call(f'CALL newLang({id}, "{tpc}")')

    # list of [id, ilc, label]
    def getLangElemTable(self, tpc:str):
        return self.get(f'CALL getLangElemTable("{tpc}");')

    # list of [ilc, label]
    def getLangElem(self, id:int):
        return self.get(f'CALL getLangElem({id});')

    def getNextLangId(self) -> int:
        return self.nextSeq('LANG')

    def setLangElem(self, id:int, ilc:str, label:str):
        self.call("CALL setLangElem(%d, '%s', '%s');" % (id, ilc, self.mask(label)))

    ## objects

    def isObject(self, id:int) -> bool:
        res = self.getNum(f'SELECT isObject({id});')
        return res > 0

    ##  images
    def getNextImgId(self) -> int:
        return self.nextSeq('IMG')

    ## subs

    def get(self, sql:str, commit=False):
        # print('get sql:', sql)
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

    def call(self, sql:str):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        cursor.close()
        self.connection.commit()

    def nextSeq(self, label:str) -> int:
        return self.getNum("SELECT nextSeq('%s');" % label, True)

    def md5(self, val:str):
        return libmd5(val.encode('utf-8')).hexdigest()

    def mask(self, val:str):
        return val.replace('\\', '\\\\').replace('\'', '\\\'')

