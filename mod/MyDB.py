
from ctypes.wintypes import CHAR
from flask_mysqldb import MySQL
from hashlib import md5 as libmd5

class MyDB(MySQL):

    def get(self, sql:str, commit=False):
        print('get sql:', sql)
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

    def call(self, sql:str):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        cursor.close()
        self.connection.commit()

    def nextSeq(self, label:str):
        return int(self.getOne("SELECT nextSeq('%s');" % label, True))

    def nextBablId(self):
        return self.nextSeq('BABL')

    def md5(self, val:str):
        return libmd5(val.encode('utf-8')).hexdigest()

    def mask(self, val:str):
        return val.replace('\\', '\\\\').replace('\'', '\\\'')

    def getId(self, usr:str, pwd:str):
        sql = "SELECT autID('%s', '%s');" % (self.mask(usr), self.md5(pwd))
        return int(self.getOne(sql))

    def setPwd(self, id:int, pwd1:str, pwd2:str):
        if pwd1 != pwd2:
            return False
        sql = "CALL setPASS(%d, '%s');" % (id, self.md5(pwd1))
        self.call(sql)
        return True

    # Lanaguage Support        

    # list of [icl, label]
    def getLangTable(self):
        return self.get('CALL getLangTable();')

    # list of [tp, label]
    def getBablTpTable(self):
        return self.get('CALL getBablTpTable();')

    # label of given babl type
    def getBablTpLabel(self, tp:str):
        return self.getOne(f'CALL getBablTpLabel("{tp}");')

    # label of given babl type
    def getBablTpLabel(self, tp:str):
        return self.getOne(f'CALL getBablTpLabel("{tp}");')

    # type of babl entry by id
    def getBablTp(self, id:int):
        return self.getOne(f'CALL getBablTp({id})')

    # list of [id, ilc, label]
    def getBablTable(self, tp:str):
        return self.get(f'CALL getBablTable("{tp}");')

    # list of [ilc, label]
    def getBabl(self, id:int):
        return self.get(f'CALL getBabl({id});')

    def getNextBablId(self):
        return self.nextSeq('BABL')

    def newBabl(self, id:int, tp:str):
        self.call(f'CALL newBabl({id}, "{tp}")')

    def setBabl(self, id:int, ilc:str, label:str):
        self.call("CALL setBabl(%d, '%s', '%s');" % (id, ilc, self.mask(label)))

