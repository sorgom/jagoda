
from ctypes.wintypes import CHAR
from flask_mysqldb import MySQL
from hashlib import md5 as libmd5
from mod.base import debug
import random

__mydb__ = None

DIM_FIELDS = [f'dim{n}' for n in range(1,4)]
USR_RECORDS = 50

class MyDB(MySQL):
    def __init__(self, app, getUidFunc, *args):
        self.getUid = getUidFunc
        super().__init__(app, *args)

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

    def newObjTtl(self, id:int):
        return self.newLangItem(id, 'OT')

    # get table fo lang items of given type
    def getLangItems(self, tpc:str):
        return self.get(f'call getLangItems("{tpc}");')

    # get elements of a lang item
    # list of [ilc, label]
    def getLangItem(self, id:int):
        return self.get(f'select ILC, LABEL from LANG_ELEM_ORD where ID = {id} order by ORD;')

    # get head (info) of language item
    def getLangItemInfo(self, id:int):
        res = self.getOneDict(f'select * from LANG_ITEM_STD where ID = {id} limit 1;')
        res['ttl'] = res['id']
        return res

    # get head (info) of for a new language item
    def getNewLangItemInfo(self, tpc:str):
        return self.getOneDict(f'select STDABLE, 0 as STD from LANG_ITEM_TYPE where TPC = "{tpc}" limit 1;')

    # set elements of a lang item
    def setLangItem(self, id:int, data:list):
        self.multi('LANG_ELEM', [f'({id}, \'{ilc}\', \'{self.mask(label)}\')' for ilc, label in data])
        self.call(f"delete from LANG_ELEM where ID = {id} and LABEL = '';")
        self.call(f'update LANG_ITEM set TST = CURRENT_TIMESTAMP where ID = {id};')
    
    # change lang item standard flag
    def setLangItemStd(self, id:int, std:int):
        debug(id, std)
        self.call(f'call setLangItemStd({id}, {1 if std else 0});')

    #   get listing of standard titles
    def getStdTtls(self):
        return self.get('select ID, LABEL from LANG_ITEM_1ST where STD = 1 and TPC = "OT" order by TST desc;')

    #   get first label of given lang item id
    def getFirstLabel(self, id:int):
        return self.getOne(f'select LABEL from LANG_ITEM_1ST where ID = {id} limit 1;')

    def getWhats(self):
        return self.get('select ID, LABEL from LANG_ITEM_1ST where TPC = "TQ" order by TST desc;')

    def getLangElem1st(self, id:int):
        return self.getOne(f'select LABEL from LANG_ITEM_1ST where ID = {id} limit 1;')

    ## objects
    @staticmethod
    def dimStrFromList(vals:list):
        return ' x '.join(map(str, vals))

    @staticmethod
    def dimStrFromDict(res):
        return MyDB.dimStrFromList([res[k] for k in DIM_FIELDS])

    def recObj(self, objId:int):
        uid = self.getUid()
        if uid:
            self.call(f'replace into OBJ_REC(OBJ, UID, TST) values ({objId}, {uid}, CURRENT_TIMESTAMP);')

    def reduceObjRecs(self):
        uid = self.getUid()
        if uid:
            recs = self.getFirstCol(f'select TST from OBJ_REC where UID = {uid} limit {USR_RECORDS};')
            if len(recs) == USR_RECORDS:
                self.call(f'delete from OBJ_REC where UID = {uid} and TST < "{recs[-1]}";')

    def touchObj(self, objId:int):
        self.call(f'update OBJ set TST = CURRENT_TIMESTAMP where ID = {objId};')
        self.recObj(objId)

    # def getObj(self, objId:int):
    #     return self.getOneDict(f'select * from OBJ where ID = {objId} limit 1;')
    def getObj(self, objId:int):
        res = self.getOneDict(f'select * from OBJ_IMG_LABEL where ID = {objId} limit 1;')
        res['dims'] = MyDB.dimStrFromDict(res)
        return res

    #   title ID, STD, STDABLE
    def getObjTtl(self, objId:int):
        return self.getOneDict(f'select TTL, STD, STDABLE from OBJ_IMG_LABEL where ID = {objId} limit 1;')

    def newObjTtl(self):
        id = self.getNextId()
        self.call(f'insert into LANG_ITEM(ID, TPC) values ({id}, "OT");')
        return self.getLangItemInfo(id)

    def setObjTtl(self, objId:int, ttlId:int):
        self.call(f'update OBJ set TTL = {ttlId} where ID = {objId};')
        self.recObj(objId)
        return self.getFirstLabel(ttlId)

    def getObjLabel(self, objId:int):
        return self.getOne(f'select LABEL from OBJ_IMG_LABEL where ID = {objId} limit 1;')

    def addObj(self, objId:int, ttlId:int):
        self.call(f'insert into OBJ(ID, TTL) values ({objId}, {ttlId});')
        self.recObj(objId)

    def addArt(self, objId:int, ttlId:int):
        self.addObj(objId, ttlId)
        self.call(f'insert into ART(OBJ) values ({objId});')

    def getObjImgLabel(self, objId:int):
        return self.getOneRow(f'select SRC, LABEL from OBJ_IMG_LABEL where ID = {objId} limit 1;')

    def setObjDims(self, objId:int, dims:list):
        self.call(f'update OBJ set DIM1 = {dims[0]}, DIM2 = {dims[1]}, DIM3 = {dims[2]} where ID = {objId};')
        self.recObj(objId)

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
        self.touchObj(objId)
    
    ##  images
    def addObjectImg(self, objId:int, imgId:int):
        self.call(f'call addObjectImg({objId}, {imgId});')
        self.touchObj(objId)

    def addImg(self, imgId:int):
        self.call(f'replace into IMG(ID) values ({imgId});')

    def getObjectImgs(self, objId:int):
        return self.getDict(f'select IMG as ID, ORD, imgFileMini(IMG) as SRC from OBJ_IMG where OBJ = {objId} order by ORD;')
    
    def setObjectImg(self, objId:int, imgId:int, ord:int):
        self.call(f'replace into OBJ_IMG values ({objId}, {imgId}, {ord});')
        self.touchObj(objId)

    def rmObjectImg(self, objId:int, imgId:int):
        self.call(f'delete from OBJ_IMG where OBJ = {objId} and IMG = {imgId};')
        self.touchObj(objId)

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
        self.call('delete from LANG_ITEM where TPC = "OT";')
        self.call('delete from OBJ;')
        self.call('delete from OBJ_REC;')
        random.seed()
        debug('random language elements')
        langs = self.getLangTable()
        slen = len(langs)
        ids = list(range(100000, 110000))
        stds = [ 0 for n in range(20) ] + [1]
        self.multi('LANG_ITEM(ID, TPC, STD)', [f'({id}, "OT", {random.choice(stds)})' for id in ids], insert=True)
        self.multi('LANG_ELEM', [f'({id}, "{ilc}", "LE {id} {label}")' for id in ids for ilc, label in random.sample(langs, random.randrange(1, slen))], insert=True)
        debug('random articles / objects')
        offset = 2000
        sizes = [10.5, 20.7, 50, 300, 400, 1000, 14.7]
        ins = [f'({id + offset}, {id}, {random.choice(sizes)}, {random.choice(sizes)}, {random.choice(sizes)})' for id in ids]
        self.multi('OBJ(ID, TTL, DIM1, DIM2, DIM3)', ins, True)
        self.multi('ART(OBJ)', [f'({id + offset})' for id in ids])
        self.multi('OBJ_REC(OBJ, UID, TST)', [f'({id + offset}, {userIdTest}, CURRENT_TIMESTAMP - INTERVAL {n} MINUTE)' for n, id in enumerate(ids)] )
        self.call('call initSeq();')

def setDB(app, getUidFunc, *args):
    global __mydb__
    if not __mydb__: __mydb__ = MyDB(app, getUidFunc, *args)
    return __mydb__

def db() -> MyDB:
    global __mydb__
    return __mydb__
