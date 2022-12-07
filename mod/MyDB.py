
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

    def multi_old(self, tablefields:str, ins:list, insert:bool=False):
        cir = 'insert' if insert else 'replace'
        head = f'{cir} into {tablefields} values'
        sql  = '\n'.join([head, ','.join(ins)])
        self.call(sql) 

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
        return self.getOne('call defIlc()')

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

    # create new language item (head)
    def addTtl(self, id:int, tpc:str):
        debug(id, tpc)
        # self.call('insert into ENT(X) values (%s)', id)
        # self.call('insert into TTL(ID, TPC) values (%s, %s)', id, tpc)
        self.callProc('addTtl', id, tpc)

    # get titles of given type
    def getTtls(self, tpc:str):
        return self.get('select TTL as ID, ILC, LABEL from TTL_ELEM_ORD where TPC = %s order by TST desc, ORD', tpc)

    def getStdTtls(self):
        return self.get('select TTL as ID, ILC, LABEL from TTL_ELEM_ORD where TPC = "OT" and STD = 1 order by ID, ORD')

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

    # set elements of a titel
    def setTtl(self, id:int, data:list):
        debug(id)
        self.multi('TTL_ELEM', [[id, ilc, label] for ilc, label in data])
        self.call('delete from TTL_ELEM where TTL = %s and LABEL = ""', id)
        # self.touchEnt(id)
    
    # change titel standard flag
    def setTtlStd(self, id:int, std:int):
        self.callProc('setTtlStd', id, 1 if std else 0)

    #   get listing of standard titles
    def getStdTtlsForSelect(self):
        return self.get('select ID, LABEL from TTL_1ST where STD = 1 and TPC = "OT" order by TST desc')

    #   get first label of given title id
    def getFirstLabel(self, id:int):
        return self.getOne('select LABEL from TTL_1ST where ID = %s limit 1', id)

    def getWhats(self):
        return self.get('select ID, LABEL from TTL_X where TPC = "TQ" and ILC = %s', self.getUsrIlc())

    def getTtl1st(self, id:int):
        return self.getOne('select LABEL from TTL_1ST where ID = %s limit 1', id)

    ## objects
    @staticmethod
    def dimStrFromDict(res):
        return formatDims([res[k] for k in DIM_FIELDS])

    def touchEnt(self, id:int):
        self.call('update ENT set TST = CURRENT_TIMESTAMP where ID = %s', id)
        self.recEnt(id)

    def reduceEntRecs(self):
        uid = self.getUid()
        if uid:
            recs = self.getFirstCol('select TST from USR_ENT where USR = %s limit %s', uid, USR_RECORDS)
            if len(recs) == USR_RECORDS:
                self.call('delete from USR_ENT where USR = %s and TST < %s', uid, recs[-1])

    def recEnt(self, id:int):
        uid = self.getUid()
        if uid:
            self.call('replace into USR_ENT(USR, ENT, TST) values (%s, %s, CURRENT_TIMESTAMP)', uid, id)

    def getObj(self, objId:int):
        res = self.getOneDict('select * from OBJ_IMG_TTL where ID = %s limit 1', objId)
        res['DIMS'] = MyDB.dimStrFromDict(res)
        return res

    #   title ID, STD, STDABLE
    def getObjTtl(self, objId:int):
        debug(id)
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
        self.recEnt(objId)
        return self.getFirstLabel(ttlId)

    def getObjLabel(self, objId:int):
        return self.getOne('select LABEL from OBJ_IMG_TTL where ID = %s limit 1', objId)

    def addObj(self, objId:int, ttlId:int):
        debug(objId, ttlId)
        self.callProc('addObj', objId, ttlId)
        self.recEnt(objId)

    def addArt(self, objId:int, ttlId:int):
        debug(objId, ttlId)
        self.addObj(objId, ttlId)
        self.call('insert into ART(OBJ) values (%s)', objId)

    def getObjImgLabel(self, objId:int):
        return self.getOneRow('select SRC, LABEL from OBJ_IMG_TTL where ID = %s limit 1', objId)

    def setObjDims(self, objId:int, dims:list):
        self.call('update OBJ set DIM1 = %s, DIM2 = %s, DIM3 = %s where ID = %s', dims[0], dims[1], dims[2], objId)
        self.recEnt(objId)

    def updObj(self, objId:int, data:dict):
        self.updTable('OBJ', 'ID', objId, data)

    def updArt(self, objId:int, data:dict, withObj=True):
        self.updTable('ART', 'OBJ', objId, data)
        if withObj: self.updObj(objId, data)
 
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

    #   list of articles [id, img, label]
    #   TODO: reasonable limitation
    def getArtList(self, limit:int=1000):
        return self.get('select ID, SRC, LABEL, WLABEL from ART_FULL order by TST desc limit %s', limit)

    def getUsrArts(self):
        return self.get('call getUsrArts(%s, %s, %s)', self.getUid(), self.getUsrIlc(), config.DB_MAX_USR_ENT)

    def getArt(self, objId:int):
        res = self.getOneDict('select * from ART_X where ID = %s and ILC = %s limit 1', objId, self.getUsrIlc())
        res['DIMS'] = MyDB.dimStrFromDict(res)
        return res

    def getObjDims(self, objId:int):
        res = self.getOneDict('select * from OBJ where ID = %s limit 1', objId)
        return MyDB.dimStrFromDict(res)

    def setWhat(self, objId:int, wId:int):
        self.call('update ART set WHAT = %s where OBJ = %s', wId, objId)
        self.touchEnt(objId)
    
    ##  images
    def addEntImg(self, objId:int, imgId:int):
        self.callProc('addEntImg', objId, imgId)
        self.touchEnt(objId)

    def addImg(self, imgId:int):
        self.call('replace into IMG(ID) values (%s)', imgId)

    def getObjImgs(self, objId:int):
        return self.getDict('select IMG as ID, ORD, imgFileMini(IMG) as SRC from ENT_IMG where ENT = %s order by ORD', objId)
    
    def setObjImg(self, objId:int, imgId:int, ord:int):
        self.call('replace into ENT_IMG values (%s, %s, %s)', objId, imgId, ord)
        self.touchEnt(objId)

    def rmObjImg(self, objId:int, imgId:int):
        self.call('delete from ENT_IMG where ENT = %s and IMG = %s', objId, imgId)
        self.touchEnt(objId)

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
        self.call('delete from ENT where ID > 10000')
        self.call('delete from TTL where TPC = "OT"')
        self.call('delete from OBJ')
        self.call('delete from USR_ENT')
        random.seed()
        debug('random language elements')
        langs = self.getLangs()
        slen = len(langs)
        ids = list(range(100000, 110000))
        stds = [ 0 for n in range(20) ] + [1]
        self.multi('ENT(ID)', [[id] for id in ids], insert=True)
        self.multi('TTL(ID, TPC, STD)', [[id, 'OT', random.choice(stds)] for id in ids], insert=True)
        self.multi('TTL_ELEM', [[id, ilc, f'LE {id} {label}'] for id in ids for ilc, label in random.sample(langs, random.randrange(1, slen))], insert=True)
        debug('random articles / objects')
        offset = 100000
        sizes = [10.5, 20.7, 50, 300, 400, 1000, 14.7]
        
        self.multi('ENT(ID)', [[id + offset] for id in ids], insert=True)
        data = [[id + offset, id, random.choice(sizes), random.choice(sizes), random.choice(sizes)] for id in ids]
        self.multi('OBJ(ID, TTL, DIM1, DIM2, DIM3)', data, insert=True)
        self.multi('ART(OBJ)', [[id + offset] for id in ids])
        dtn = datetime.now()
        self.multi('USR_ENT(ENT, USR, TST)', [[id + offset, userIdTest, dtn -  timedelta(minutes=n)] for n, id in enumerate(ids)],insert=True)
        self.callProc('initSeq')

def setDB(app, getUidFunc, getUsrIlcFunc, *args):
    global __mydb__
    if not __mydb__: __mydb__ = MyDB(app, getUidFunc, getUsrIlcFunc, *args)
    return __mydb__

def db() -> MyDB:
    global __mydb__
    return __mydb__
