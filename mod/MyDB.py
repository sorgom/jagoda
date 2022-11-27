
import mysql.connector
from hashlib import md5 as libmd5
from mod.base import debug
from mod.config import DB_CONFIG
import random

__mydb__ = None

DIM_FIELDS = [f'dim{n}' for n in range(1,4)]
USR_RECORDS = 50

class MyDB(object):
    def __init__(self, getUidFunc, config):
        self.getUid = getUidFunc
        self.cnx = mysql.connector.connect(**config)

    def __del__(self):
        self.cnx.close()

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
    def getLangs(self):
        return self.get('select ILC, LABEL from LANG order by ORD;')

    # get list of item types
    # list of [tpc, label]
    def getTtps(self):
        return self.get('select * from TTP;')

    # get label of given language type
    def getTtpLabel(self, tpc:str):
        return self.getOne(f'select LABEL from TTP where TPC = "{tpc}" limit 1;')

    # get lang item type of language entry by id
    def getTpc(self, id:int):
        return self.getOne(f'select TPC from TTL where ID = {id} limit 1;')

    # create new language item (head)
    def addTtl(self, id:int, tpc:str):
        debug(id, tpc)
        self.callProc('addTtl', id, tpc)

    # get titles of given type
    def getTtls(self, tpc:str):
        return self.get(f'select TTL as ID, ILC, LABEL from TTL_ELEM_ORD where TPC = "{tpc}" order by TST desc, ORD;')

    # get elements of a title
    # list of [ilc, label]
    def getTtl(self, id:int):
        return self.get(f'select ILC, LABEL from TTL_ELEM_ORD where ID = {id} order by ORD;')

    # get head (info) of language item
    def getTtlInfo(self, id:int):
        res = self.getOneDict(f'select * from TTL_INFO where ID = {id} limit 1;')
        res['ttl'] = res['id']
        return res

    # get head (info) of for a new language item
    def getNewTtlInfo(self, tpc:str):
        return self.getOneDict(f'select STDABLE, 0 as STD from TTP where TPC = "{tpc}" limit 1;')

    # set elements of a lang item
    def setTtl(self, id:int, data:list):
        debug(id)
        self.multi('TTL_ELEM', [f'({id}, \'{ilc}\', \'{self.mask(label)}\')' for ilc, label in data])
        self.call(f'delete from TTL_ELEM where TTL = {id} and LABEL = "";')
        self.touchEnt(id)
    
    # change lang item standard flag
    def setTtlStd(self, id:int, std:int):
        self.call(f'call setTtlStd({id}, {1 if std else 0});')

    #   get listing of standard titles
    def getStdTtls(self):
        return self.get('select ID, LABEL from TTL_1ST where STD = 1 and TPC = "OT" order by TST desc;')

    #   get first label of given title id
    def getFirstLabel(self, id:int):
        return self.getOne(f'select LABEL from TTL_1ST where ID = {id} limit 1;')

    def getWhats(self):
        return self.get('select ID, LABEL from TTL_1ST where TPC = "TQ" order by TST desc;')

    def getTtl1st(self, id:int):
        return self.getOne(f'select LABEL from TTL_1ST where ID = {id} limit 1;')

    ## objects
    @staticmethod
    def dimStrFromList(vals:list):
        return ' x '.join(map(str, vals))

    @staticmethod
    def dimStrFromDict(res):
        return MyDB.dimStrFromList([res[k] for k in DIM_FIELDS])

    def touchEnt(self, id:int):
        self.call(f'replace into ENT values ({id}, CURRENT_TIMESTAMP);')
        self.recEnt(id)

    def reduceObjRecs(self):
        uid = self.getUid()
        if uid:
            recs = self.getFirstCol(f'select TST from USR_ENT where USR = {uid} limit {USR_RECORDS};')
            if len(recs) == USR_RECORDS:
                self.call(f'delete from USR_ENT where USR = {uid} and TST < "{recs[-1]}";')

    def recEnt(self, id:int):
        uid = self.getUid()
        if uid:
            self.call(f'replace into USR_ENT(USR, ENT, TST) values ({uid}, {id}, CURRENT_TIMESTAMP);')

    # def getObj(self, objId:int):
    #     return self.getOneDict(f'select * from OBJ where ID = {objId} limit 1;')
    def getObj(self, objId:int):
        res = self.getOneDict(f'select * from ENT_IMG_LABEL where ID = {objId} limit 1;')
        res['dims'] = MyDB.dimStrFromDict(res)
        return res

    #   title ID, STD, STDABLE
    def getObjTtl(self, objId:int):
        return self.getOneDict(f'select TTL, STD, STDABLE from ENT_IMG_LABEL where ID = {objId} limit 1;')

    def addObjTtl(self, id:int):
        debug(id)
        self.addTtl(id, 'OT')

    def newObjTtl(self):
        id = self.getNextId()
        self.addObjTtl(id)
        return self.getTtlInfo(id)

    def setObjTtl(self, objId:int, ttlId:int):
        self.call(f'update OBJ set TTL = {ttlId} where ID = {objId};')
        self.recEnt(objId)
        return self.getFirstLabel(ttlId)

    def getObjLabel(self, objId:int):
        return self.getOne(f'select LABEL from ENT_IMG_LABEL where ID = {objId} limit 1;')

    def addObj(self, objId:int, ttlId:int):
        debug(objId, ttlId)
        self.callProc('addObj', objId, ttlId)
        self.recEnt(objId)

    def addArt(self, objId:int, ttlId:int):
        debug(objId, ttlId)
        self.addObj(objId, ttlId)
        self.call(f'insert into ART(OBJ) values ({objId});')

    def getObjImgLabel(self, objId:int):
        return self.getOneRow(f'select SRC, LABEL from ENT_IMG_LABEL where ID = {objId} limit 1;')

    def setObjDims(self, objId:int, dims:list):
        self.call(f'update OBJ set DIM1 = {dims[0]}, DIM2 = {dims[1]}, DIM3 = {dims[2]} where ID = {objId};')
        self.recEnt(objId)

    #   list of articles [id, img, label]
    #   TODO: reasonable limitation
    def getArtList(self):
        return self.get('select ID, SRC, LABEL, WLABEL from ART_FULL order by TST desc limit 100;')

    def getUsrArtList(self):
        return self.get(f'call getUsrArticles({self.getUid()});')

    def getArt(self, objId:int):
        res = self.getOneDict(f'select * from ART_FULL where ID = {objId} limit 1;')
        res['dims'] = MyDB.dimStrFromDict(res)
        return res

    def getObjDims(self, objId:int):
        res = self.getOneDict(f'select * from OBJ where ID = {objId} limit 1;')
        return MyDB.dimStrFromDict(res)

    def setWhat(self, objId:int, wId:int):
        self.call(f'update ART set WHAT = {wId} where OBJ = {objId};')
        self.touchEnt(objId)
    
    ##  images
    def addEntImg(self, objId:int, imgId:int):
        self.call(f'call addEntImg({objId}, {imgId});')
        self.touchEnt(objId)

    def addImg(self, imgId:int):
        self.call(f'replace into IMG(ID) values ({imgId});')

    def getObjImgs(self, objId:int):
        return self.getDict(f'select IMG as ID, ORD, imgFileMini(IMG) as SRC from ENT_IMG where ENT = {objId} order by ORD;')
    
    def setObjImg(self, objId:int, imgId:int, ord:int):
        self.call(f'replace into ENT_IMG values ({objId}, {imgId}, {ord});')
        self.touchEnt(objId)

    def rmObjImg(self, objId:int, imgId:int):
        self.call(f'delete from ENT_IMG where OBJ = {objId} and IMG = {imgId};')
        self.touchEnt(objId)

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
        debug(sql)
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

    def mkOneDict(self, cur):
        desc = [ d[0].lower() for d in cur.description ]
        return dict(zip(desc, cur.fetchone()))

    def getDict(self, sql:str, **args):
        return self.procCursor(sql, self.mkDict, **args)

    def getOneDict(self, sql:str, **args):
        return self.procCursor(sql, self.mkOneDict, **args)

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
        debug(sql)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        cursor.close()
        self.connection.commit()
    
    def callProc(self, proc:str, *args):
        debug(proc, *args)
        cursor = self.connection.cursor()
        cursor.callproc(proc, args)
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
        userIdTest = 3
        self.call('delete from TTL where TPC = "OT";')
        self.call('delete from OBJ;')
        self.call('delete from USR_ENT;')
        random.seed()
        debug('random language elements')
        langs = self.getLangs()
        slen = len(langs)
        ids = list(range(100000, 110000))
        stds = [ 0 for n in range(20) ] + [1]
        self.multi('TTL(ID, TPC, STD)', [f'({id}, "OT", {random.choice(stds)})' for id in ids], insert=True)
        self.multi('TTL_ELEM', [f'({id}, "{ilc}", "LE {id} {label}")' for id in ids for ilc, label in random.sample(langs, random.randrange(1, slen))], insert=True)
        debug('random articles / objects')
        offset = 2000
        sizes = [10.5, 20.7, 50, 300, 400, 1000, 14.7]
        ins = [f'({id + offset}, {id}, {random.choice(sizes)}, {random.choice(sizes)}, {random.choice(sizes)})' for id in ids]
        self.multi('OBJ(ID, TTL, DIM1, DIM2, DIM3)', ins, True)
        self.multi('ART(OBJ)', [f'({id + offset})' for id in ids])
        self.multi('USR_ENT(OBJ, UID, TST)', [f'({id + offset}, {userIdTest}, CURRENT_TIMESTAMP - INTERVAL {n} MINUTE)' for n, id in enumerate(ids)] )
        self.call('call initSeq();')

def setDB(app, getUidFunc, *args):
    global __mydb__
    if not __mydb__: __mydb__ = MyDB(app, getUidFunc, *args)
    return __mydb__

def db() -> MyDB:
    global __mydb__
    return __mydb__
