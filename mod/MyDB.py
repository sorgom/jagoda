
from flask_mysqldb import MySQL
from hashlib import md5 as libmd5
from mod.base import debug
import random

__mydb__ = None

DIM_FIELDS = [f'DIM{n}' for n in range(1,4)]
USR_RECORDS = 50

class MyDB(MySQL):
    def __init__(self, app, getUidFunc, *args):
        self.getUid = getUidFunc
        super().__init__(app, *args)

    def cursor(self):
        return self.connection.cursor()
    
    def commit(self, commit=True):
        if commit: self.connection.commit()

    def procCursor(self, func, sql:str, args, commit=False):
        debug(sql, *args)
        res = None
        cur = self.cursor()
        cur.execute(sql, args)
        res = func(cur)
        self.commit(commit)
        cur.close()
        return res

    def get(self, sql:str, *args, **opts):
        return self.procCursor(lambda c : c.fetchall(), sql, args, **opts)

    def getOneRow(self, sql:str, *args):
        return self.procCursor(lambda c : c.fetchone(), sql, args)

    def mkDict(self, cur):
        desc = [ d[0] for d in cur.description ]
        return list(map(lambda a : dict(zip(desc, a)), cur.fetchall()))

    def mkOneDict(self, cur):
        desc = [ d[0] for d in cur.description ]
        return dict(zip(desc, cur.fetchone()))

    def getDict(self, sql:str, *args):
        return self.procCursor(self.mkDict, sql, args)

    def getOneDict(self, sql:str, *args):
        return self.procCursor(self.mkOneDict, sql, args)

    def getOne(self, sql:str, *args, **opts):
        res = self.getOneRow(sql, *args, **opts)
        return res[0] if res else None
    
    def getNum(self, sql:str, *args) -> int:
        return int(self.getOne(sql, *args) or '0')

    def getFirstCol(self, sql:str, *args):
        return [ r[0] for r in self.get(sql, *args)]

    def call(self, sql:str, *args, commit=False):
        debug(sql, *args)
        cur = self.cursor()
        cur.execute(sql, args)
        self.commit(commit)
    
    def callProc(self, proc:str, *args, commit=False):
        debug(proc, *args)
        ret = None
        cur = self.cursor()
        ret = cur.callproc(proc, args)
        self.commit(commit)
        cur.close()

    def md5(self, val:str):
        return libmd5(val.encode('utf-8')).hexdigest()

    def mask(self, val:str):
        return val.replace('\\', '\\\\').replace('\'', '\\\'')

    def multi(self, tablefields:str, ins:list, insert:bool=False):
        cir = 'insert' if insert else 'replace'
        head = f'{cir} into {tablefields} values'
        sql  = '\n'.join([head, ','.join(ins)])
        self.call(sql) 

    def getNextId(self):
        return self.getNum('select nextId()')

    def getUsrId(self, usr:str, pwd:str):
        res = self.getNum('select getUsrId(%s, %s)', self.mask(usr), self.md5(pwd))
        debug(res)
        return res

    def setPwd(self, id:int, pwd1:str, pwd2:str):
        if pwd1 != pwd2:
            return False
        self.call('update USR set PASS = %s  where ID = %s', self.md5(pwd1), id)
        return True

    ## lanaguage support        

    # get list of current languages
    # list of [icl, label]
    def getLangs(self):
        return self.get('select ILC, LABEL from LANG order by ORD')

    # get list of item types
    # list of [tpc, label]
    def getTtps(self):
        return self.get('select * from TTP')

    # get label of given language type
    def getTtpLabel(self, tpc:str):
        return self.getOne('select LABEL from TTP where TPC = %s limit 1', tpc)

    # get lang item type of language entry by id
    def getTpc(self, id:int):
        return self.getOne('select TPC from TTL where ID = %s limit 1', id)

    # create new language item (head)
    def addTtl(self, id:int, tpc:str):
        debug(id, tpc)
        # self.call('insert into ENT(X) values (%s)', id)
        # self.call('insert into TTL(ID, TPC) values (%s, %s)', id, tpc)
        self.callProc('addTtl', id, tpc)

    # get titles of given type
    def getTtls(self, tpc:str):
        return self.get('select TTL as ID, ILC, LABEL from TTL_ELEM_ORD where TPC = %s order by TST desc, ORD', tpc)

    # get elements of a title
    # list of [ilc, label]
    def getTtl(self, id:int):
        return self.get('select ILC, LABEL from TTL_ELEM_ORD where ID = %s order by ORD', id)

    # get head (info) of language item
    def getTtlInfo(self, id:int):
        res = self.getOneDict('select * from TTL_INFO where ID = %s limit 1', id)
        res['TTL'] = res['ID']
        return res

    # get head (info) of for a new language item
    def getNewTtlInfo(self, tpc:str):
        return self.getOneDict('select STDABLE, 0 as STD from TTP where TPC = %s limit 1', tpc)

    # set elements of a lang item
    def setTtl(self, id:int, data:list):
        debug(id)
        self.multi('TTL_ELEM', [f'({id}, \'{ilc}\', \'{self.mask(label)}\')' for ilc, label in data])
        self.call('delete from TTL_ELEM where TTL = %s and LABEL = ""', id)
        # self.touchObj(id)
    
    # change lang item standard flag
    def setTtlStd(self, id:int, std:int):
        self.callProc('setTtlStd', id, 1 if std else 0)

    #   get listing of standard titles
    def getStdTtls(self):
        return self.get('select ID, LABEL from TTL_1ST where STD = 1 and TPC = "OT" order by TST desc')

    #   get first label of given title id
    def getFirstLabel(self, id:int):
        return self.getOne('select LABEL from TTL_1ST where ID = %s limit 1', id)

    def getWhats(self):
        return self.get('select ID, LABEL from TTL_1ST where TPC = "TQ" order by TST desc')

    def getTtl1st(self, id:int):
        return self.getOne('select LABEL from TTL_1ST where ID = %s limit 1', id)

    ## objects
    @staticmethod
    def dimStrFromList(vals:list):
        return ' x '.join(map(str, vals))

    @staticmethod
    def dimStrFromDict(res):
        print(res)
        return MyDB.dimStrFromList([res[k] for k in DIM_FIELDS])

    def touchObj(self, id:int):
        self.call('update OBJ set TST = CURRENT_TIMESTAMP where ID = %s', id)
        self.recObj(id)

    def reduceObjRecs(self):
        uid = self.getUid()
        if uid:
            recs = self.getFirstCol('select TST from USR_OBJ where USR = %s limit %s', uid, USR_RECORDS)
            if len(recs) == USR_RECORDS:
                self.call('delete from USR_OBJ where USR = %s and TST < %s', uid, recs[-1])

    def recObj(self, id:int):
        uid = self.getUid()
        if uid:
            self.call('replace into USR_OBJ(USR, OBJ, TST) values (%s, %s, CURRENT_TIMESTAMP)', uid, id)

    def getObj(self, objId:int):
        res = self.getOneDict('select * from OBJ_IMG_TTL where ID = %s limit 1', objId)
        res['DIMS'] = MyDB.dimStrFromDict(res)
        return res

    #   title ID, STD, STDABLE
    def getObjTtl(self, objId:int):
        return self.getOneDict('select TTL, STD, STDABLE from OBJ_IMG_TTL where ID = %s limit 1', objId)

    def addObjTtl(self, id:int):
        debug(id)
        self.addTtl(id, 'OT')

    def newObjTtl(self):
        id = self.getNextId()
        self.addObjTtl(id)
        return self.getTtlInfo(id)

    def setObjTtl(self, objId:int, ttlId:int):
        self.call('update OBJ set TTL = %s where ID = %s', ttlId, objId)
        self.recObj(objId)
        return self.getFirstLabel(ttlId)

    def getObjLabel(self, objId:int):
        return self.getOne('select LABEL from OBJ_IMG_TTL where ID = %s limit 1', objId)

    def addObj(self, objId:int, ttlId:int):
        debug(objId, ttlId)
        self.callProc('addObj', objId, ttlId)
        self.recObj(objId)

    def addArt(self, objId:int, ttlId:int):
        debug(objId, ttlId)
        self.addObj(objId, ttlId)
        self.call('insert into ART(OBJ) values (%s)', objId)

    def getObjImgLabel(self, objId:int):
        return self.getOneRow('select SRC, LABEL from OBJ_IMG_TTL where ID = %s limit 1', objId)

    def setObjDims(self, objId:int, dims:list):
        self.call('update OBJ set DIM1 = %s, DIM2 = %s, DIM3 = %s where ID = %s', dims[0], dims[1], dims[2], objId)
        self.recObj(objId)

    #   list of articles [id, img, label]
    #   TODO: reasonable limitation
    def getArtList(self, limit:int=1000):
        return self.get('select ID, SRC, LABEL, WLABEL from ART_FULL order by TST desc limit %s', limit)

    def getUsrArtList(self):
        return self.get('call getUsrArticles(%s)', self.getUid())

    def getArt(self, objId:int):
        res = self.getOneDict('select * from ART_FULL where ID = %s limit 1', objId)
        res['DIMS'] = MyDB.dimStrFromDict(res)
        return res

    def getObjDims(self, objId:int):
        res = self.getOneDict('select * from OBJ where ID = %s limit 1', objId)
        return MyDB.dimStrFromDict(res)

    def setWhat(self, objId:int, wId:int):
        self.call('update ART set WHAT = %s where OBJ = %s', wId, objId)
        self.touchObj(objId)
    
    ##  images
    def addObjImg(self, objId:int, imgId:int):
        self.callProc('addObjImg', objId, imgId)
        self.touchObj(objId)

    def addImg(self, imgId:int):
        self.call('replace into IMG(ID) values (%s)', imgId)

    def getObjImgs(self, objId:int):
        return self.getDict('select IMG as ID, ORD, imgFileMini(IMG) as SRC from OBJ_IMG where OBJ = %s order by ORD', objId)
    
    def setObjImg(self, objId:int, imgId:int, ord:int):
        self.call('replace into OBJ_IMG values (%s, %s, %s)', objId, imgId, ord)
        self.touchObj(objId)

    def rmObjImg(self, objId:int, imgId:int):
        self.call('delete from OBJ_IMG where OBJ = %s and IMG = %s', objId, imgId)
        self.touchObj(objId)

    def getUnusedImgs(self):
        return self.getDict('select * from UNUSED_IMGS')

    def getImgFileMini(self, id:int):
        return self.getOne('select imgFileMini(%s)', id)
    def getImgFileFull(self, id:int):
        return self.getOne('select imgFileFull(%s)', id)
    def getImgFileExif(self, id:int):
        return self.getOne('select imgFileExif(%s)', id)
    def getImgFiles(self, id:int):
        return self.getOneRow('call imgFiles(%s)', id)
    def getImgFolders(self):
        return self.getOneRow('call imgFolders()')

    # create a lot of articles and titels
    def testData(self):
        userIdTest = 3
        self.call('delete from TTL where TPC = "OT"')
        self.call('delete from OBJ')
        self.call('delete from USR_OBJ')
        random.seed()
        debug('random language elements')
        langs = self.getLangs()
        slen = len(langs)
        ids = list(range(100000, 110000))
        stds = [ 0 for n in range(20) ] + [1]
        self.multi('ENT(X)', [f'({id})' for id in ids], insert=True)
        self.multi('TTL(ID, TPC, STD)', [f'({id}, "OT", {random.choice(stds)})' for id in ids], insert=True)
        self.multi('TTL_ELEM', [f'({id}, "{ilc}", "LE {id} {label}")' for id in ids for ilc, label in random.sample(langs, random.randrange(1, slen))], insert=True)
        debug('random articles / objects')
        offset = 2000
        sizes = [10.5, 20.7, 50, 300, 400, 1000, 14.7]
        
        self.multi('ENT(X)', [f'(id + offset)' for id in ids], insert=True)
        ins = [f'({id + offset}, {id}, {random.choice(sizes)}, {random.choice(sizes)}, {random.choice(sizes)})' for id in ids]
        self.multi('OBJ(ID, TTL, DIM1, DIM2, DIM3)', ins, True)
        self.multi('ART(OBJ)', [f'({id + offset})' for id in ids])
        self.multi('USR_OBJ(ENT, USR, TST)', [f'({id + offset}, {userIdTest}, CURRENT_TIMESTAMP - INTERVAL {n} MINUTE)' for n, id in enumerate(ids)] )
        self.callProc('initSeq')

def setDB(app, getUidFunc, *args):
    global __mydb__
    if not __mydb__: __mydb__ = MyDB(app, getUidFunc, *args)
    return __mydb__

def db() -> MyDB:
    global __mydb__
    return __mydb__
