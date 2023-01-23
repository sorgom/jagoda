import pymysql.cursors

from mod.base import debug

__mydb__ = None

class MyPyDB(object):
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self, **args):
        debug('..')
        self.connection = pymysql.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database,
            **args
        )
        debug('done')
        return self.connection.cursor()

    def connectDict(self):
        self.connect(cursorclass=pymysql.cursors.DictCursor)

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def commit(self, commit=True):
        if commit: self.connection.commit()

    def procCursor(self, func, sql:str, args, commit=False, **opts):
        debug(sql, *args)
        res = None
        cur = self.connect(**opts)
        cur.execute(sql, args)
        res = func(cur)
        self.commit(commit)
        cur.close()
        self.disconnect()
        return res

    # def procCursorDict(self, func, sql:str, args, commit=False):
    #     return self.procCursor(func, sql, args, commit, cursorclass=pymysql.cursors.DictCursor)

    def get(self, sql:str, *args, **opts):
        return self.procCursor(lambda c : c.fetchall(), sql, args, **opts)

    def getDict(self, sql:str, *args, **opts):
        return self.get(sql, *args, **opts, cursorclass=pymysql.cursors.DictCursor)

    def test1(self):
        data = self.get('call getObjsNoWhat(%s)', ('fr',))
        debug(len(data))

    def test2(self):
        data = self.getDict('select ILC, LABEL from LANG order by ORD')
        debug(data)


def setDB(*args):
    global __mydb__
    if not __mydb__: __mydb__ = MyPyDB(*args)
    return __mydb__

def db() -> MyPyDB:
    global __mydb__
    return __mydb__

if __name__ == '__main__':
    setDB('127.0.0.1', 'aut', '** yes: i am an author **', 'jagoda')
    data = db().get('call getObjsNoWhat(%s)', ('fr',))
    debug(len(data))        