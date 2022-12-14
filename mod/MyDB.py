
from flask_mysqldb import MySQL
from hashlib import md5 as libmd5
from mod.base import debug
import random
from mod.format import formatDims
from mod import config

from datetime import timedelta, datetime

__mydb__ = None

DIM_FIELDS = [f'DIM{n}' for n in range(1,4)]
USR_RECORDS = 50

class MyDB(MySQL):
    def __init__(self, app, getUidFunc, getUsrIlcFunc, *args):
        self.getUid = getUidFunc
        self.getUsrIlc = getUsrIlcFunc
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

    def getDesc(self, table:str):
        return self.getFirstCol(f'desc {table}')

    def call(self, sql:str, *args, commit=False):
        debug(sql, *args)
        cur = self.cursor()
        cur.execute(sql, args)
        self.commit(commit)
        cur.close()
    
    def callProc(self, proc:str, *args, commit=False):
        debug(proc, *args)
        ret = None
        cur = self.cursor()
        ret = cur.callproc(proc, args)
        self.commit(commit)
        cur.close()

    def md5(self, val:str):
        return libmd5(val.encode('utf-8')).hexdigest()

    def multi(self, tablefields:str, data:list, insert:bool=False):
        if data:
            cl = f"({','.join(['%s' for v in data[0]])})"
            cins = f"{','.join([cl for x in range(len(data))])}"
            vals = [val for l in data for val in l]
            cir = 'insert' if insert else 'replace'
            sql = f'{cir} into {tablefields} values {cins}'
            self.call(sql, *vals) 

    def getNextId(self):
        return self.getNum('select nextId()')

    def getUsrId(self, usr:str, pwd:str):
        res = self.getNum('select getUsrId(%s, %s)', usr, self.md5(pwd))
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

    def getDefIlc(self):
        return self.getOne('select defIlc()')

    # get list of item types
    # list of [tpc, label]
    def getTtps(self):
        return self.get('select * from TTP')

    # get label of given language type
    def getTtpLabel(self, tpc:str):
        return self.getOne('select LABEL from TTP where TPC = %s limit 1', tpc)

    # get titel type of language entry by id
    def getTpc(self, id:int):
        return self.getOne('select TPC from TTL where ID = %s limit 1', id)

    # add new title (head)
    def addTtl(self, id:int, tpc:str):
        debug(id, tpc)
        self.call('insert into TTL(ID, TPC) values (%s, %s)', id, tpc)
 
    # get titles of given type
    def getTtls(self, tpc:str):
        return self.get('select ID, ILC, LABEL from TTL_ORD where TPC = %s order by TST desc, ORD', tpc)

    #   get standard titles
    def getStdTtls(self):
        return self.get('call getStdTtls(%s)', self.getUsrIlc())

    # get elements of a title
    # list of [ilc, label]
    def getTtl(self, id:int):
        return self.get('select ILC, LABEL from TTL_ORD where ID = %s order by ORD', id)

    # get head (info) of title
    def getTtlInfo(self, id:int):
        res = self.getOneDict('select * from TTL_INFO where ID = %s limit 1', id)
        res['TTL'] = res['ID']
        return res

    # get head (info) of for a new title
    def getNewTtlInfo(self, tpc:str):
        return self.getOneDict('select STDABLE, 0 as STD from TTP where TPC = %s limit 1', tpc)

    # set elements of a titel
    def setTtl(self, id:int, data:list):
        debug(id)
        self.multi('TTL_ELEM', [[id, ilc, label] for ilc, label in data])
        self.call('delete from TTL_ELEM where TTL = %s and LABEL = ""', id)
        self.touchTtl(id)
    
    # change titel standard flag
    def setTtlStd(self, id:int, std:int):
        self.callProc('setTtlStd', id, 1 if std else 0)

    #   get listing of standard titles
    def getStdTtlsForSelect(self):
        return self.get('select ID, LABEL from TTL_1ST where STD = 1 and TPC = "OT" order by TST desc')

    #   get label of given title id
    def getTtlLabel(self, id:int):
        return self.getOne('select getTtlLabel(%s, %s)', id, self.getUsrIlc())

    #   get object kind
    def getWhat(self, objId:int):
        return self.getNum('select WHAT from OBJ where ID = %s limit 1', objId)

    #   all object kinds
    def getWhats(self):
        return self.get('call getWhats(%s)', self.getUsrIlc())

    ##  captions
    #   get all captions for production
    def getCapsPro(self, ilc:str):
        return self.get('call getCapsPro(%s)', ilc)

    #   get all captions for editing (forein language / not found displayed)
    def getCaps(self):
        return self.get('call getCaps(%s)', self.getUsrIlc())

    # get CPC of caption
    def getCapCpc(self, capId:int):
        return self.getOne('select CPC from CAP where ID = %s limit 1', capId)

    #  get elements of caption
    def getCap(self, capId:int):
        return self.get('select ILC, LABEL from CAP_ELEM where CAP = %s', capId)

    # set elements of a caption
    def setCap(self, id:int, data:list):
        debug(id)
        self.multi('CAP_ELEM', [[id, ilc, label] for ilc, label in data])
        self.call('delete from CAP_ELEM where CAP = %s and LABEL = ""', id)
    
    ## objects
    @staticmethod
    def dimStrFromDict(res):
        return formatDims([res[k] for k in DIM_FIELDS])

    def touchTbl(self, table, id):
        self.call(f'update {table} set TST = CURRENT_TIMESTAMP where ID = %s', id)

    def touchObj(self, id:int):
        self.touchTbl('OBJ', id)
        self.recObj(id)

    def touchTtl(self, id:int):
        self.touchTbl('TTL', id)
        self.recTtl(id)
 
    def reduceRecWhat(self, what:str, uid:int):
        uid = self.getUid()
        if uid:
            recs = self.getFirstCol(f'select TST from USR_{what} where USR = %s limit %s', uid, USR_RECORDS)
            if len(recs) == USR_RECORDS:
                self.call(f'delete from USR_{what} where USR = %s and TST < %s', uid, recs[-1])

    def reduceRecs(self):
        uid = self.getUid()
        if uid:
            self.reduceRecWhat('OBJ', uid)
            self.reduceRecWhat('TTL', uid)

    def recWhat(self, what:str, id:int):
        uid = self.getUid()
        if uid:
            self.call(f'replace into USR_{what}(USR, {what}, TST) values (%s, %s, CURRENT_TIMESTAMP)', uid, id)

    def recObj(self, objId:int):
        self.recWhat('OBJ', objId)

    def recTtl(self, ttlId:int):
        self.recWhat('TTL', ttlId)

    def getObj(self, objId:int):
        res = self.getOneDict('call getObj(%s, %s)', objId, self.getUsrIlc())
        res['DIMS'] = MyDB.dimStrFromDict(res)
        return res

    #   title ID, STD, STDABLE
    def getObjTtlInfo(self, objId:int):
        debug(id)
        return self.getOneDict('select TTL, STD, STDABLE from OBJ_TTL_INFO where OBJ = %s limit 1', objId)

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
        return self.getTtlLabel(ttlId)

    def addObj(self, objId:int, ttlId:int):
        debug(objId, ttlId)
        self.call('insert into OBJ(ID, TTL) values (%s, %s)', objId, ttlId)
        self.recObj(objId)

    def getObjImg(self, objId:int):
        return self.getOne('select SRC from OBJ_IMG_DEF where OBJ = %s limit 1', objId)

    def updObj(self, objId:int, data:dict):
        self.updTable('OBJ', 'ID', objId, data)

    def updTable(self, table:str, idKey:str, id:int, data):
        keys = self.getDesc(table)
        keys.pop(0)
        sets = []
        vals = []
        for key, val in data.items():
            if key in keys:
                sets.append(f'{key}=%s')
                vals.append(val)
        if sets:
            vals.append(id)
            sql = f'update {table} set ' + ','.join(sets) + f' where {idKey}=%s'
            self.call(sql, *vals)

    #   list of objects [id, img, label]
    #   TODO: call getObjs
    def getObjList(self, limit:int=1000):
        return self.get('select ID, SRC, LABEL, WLABEL from ART_FULL order by TST desc limit %s', limit)

    def getUsrObjs(self):
        return self.get('call getUsrObjs(%s, %s, %s)', self.getUid(), self.getUsrIlc(), config.DB_MAX_USR_ENT)

    def getObj(self, objId:int):
        res = self.getOneDict('call getObj(%s, %s)', objId, self.getUsrIlc())
        res['DIMS'] = MyDB.dimStrFromDict(res)
        return res

    def getObjDims(self, objId:int):
        res = self.getOneDict('select * from OBJ where ID = %s limit 1', objId)
        return MyDB.dimStrFromDict(res)

    def setWhat(self, objId:int, wId:int):
        self.call('update OBJ set WHAT = %s where ID = %s', wId, objId)
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

    # create a lot of objects and titels
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
        self.multi('TTL(ID, TPC, STD)', [[id, 'OT', random.choice(stds)] for id in ids], insert=True)
        self.multi('TTL_ELEM', [[id, ilc, f'LE {id} {label}'] for id in ids for ilc, label in random.sample(langs, random.randrange(1, slen))], insert=True)
        debug('random objects / objects')
        offset = 100000
        sizes = [10.5, 20.7, 50, 300, 400, 1000, 14.7]
        
        data = [[id + offset, id, random.choice(sizes), random.choice(sizes), random.choice(sizes)] for id in ids]
        self.multi('OBJ(ID, TTL, DIM1, DIM2, DIM3)', data, insert=True)
        dtn = datetime.now() - timedelta(days=1)
        self.multi('USR_OBJ(OBJ, USR, TST)', [[id + offset, userIdTest, dtn -  timedelta(minutes=n)] for n, id in enumerate(ids)],insert=True)
        self.callProc('initSeq')

def setDB(app, getUidFunc, getUsrIlcFunc, *args):
    global __mydb__
    if not __mydb__: __mydb__ = MyDB(app, getUidFunc, getUsrIlcFunc, *args)
    return __mydb__

def db() -> MyDB:
    global __mydb__
    return __mydb__
