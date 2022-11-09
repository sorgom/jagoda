from mod.MyDB import db
from mod.base import *
from mod.saveImg import saveImg, getImgMini, getImgFull, getExif
from mod.utilz import debug
from mod.login import loggedIn

# TODO: make part of config
MAX_NUM_IMGES = 8

def mkJson(data, withMax:bool=False):
    return json.dumps({ 'data':data, 'max':MAX_NUM_IMGES if withMax else 0})

def _objImgs(objId:int):
    debug('_objImgs:', objId)
    res = []
    for img in db().getObjectImgs(objId):
        src = getImgMini(img['id'])
        if src:
            img['src'] = src
            res.append(img)
    return mkJson(res, True)

def _addObjImgs(objId:int):
    if (loggedIn()):
        debug('_addObjImgs:', objId)
        files = request.files.getlist('files')
        for file in files: saveImg(file, objId)
        return _objImgs(objId)

def _orderObjImgs(objId:int):
    if (loggedIn()):
        debug('_orderObjImgs', objId)
        for imgId, ord in getJson():
            debug(objId, imgId, ord)
            db().setObjectImg(objId, imgId, ord)
        return 'DONE'

def _rmObjImg():
    if (loggedIn()):
        debug('_rmObjImg')
        db().rmObjectImg(rf('objId'), rf('imgId'))
        return 'DONE'

def _unusedImgs():
    debug('_unusedImgs')
    res = []
    imgs = db().getUnusedImgs()
    for img in imgs:
        src = getImgMini(img['id'])
        if src:
            img['src'] = src
            res.append(img)
    return mkJson(res)

def _imgInfo(id:int):
    debug('_imgInfo')
    src  = getImgFull(id)
    data = getExif(id)
    if src and data:
        return render_template('_img_info.htm', id=id, src=src, data=data)
    return ERR_DATA
