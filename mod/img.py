from flask import render_template
from mod.MyDB import db
from mod.base import *
from mod.saveImg import saveImg, getExif
from mod.login import loggedIn

# TODO: make part of config
MAX_NUM_IMGES = 8

def mkJson(data, withMax:bool=False):
    return json.dumps({ 'data':data, 'max':MAX_NUM_IMGES if withMax else 0})

def _objImgs(objId:int):
    debug(objId)
    res = db().getObjImgs(objId)
    debug('res', res)
    return mkJson(res, True)

def _addObjImgs(objId:int):
    if (loggedIn()):
        debug(objId)
        files = request.files.getlist('files')
        for file in files: saveImg(file, objId)
        return _objImgs(objId)

def _orderObjImgs(objId:int):
    if (loggedIn()):
        debug(objId)
        for imgId, ord in getJson():
            debug(objId, imgId, ord)
            db().setObjImg(objId, imgId, ord)
        db().touchEnt(objId)
        return 'DONE'

def _rmObjImg():
    if (loggedIn()):
        debug()
        db().rmObjImg(rf('objId'), rf('imgId'))
        return 'DONE'

def _unusedImgs():
    debug()
    return mkJson(db().getUnusedImgs())

def _imgInfo(id:int):
    debug()
    src  = db().getImgFileFull(id)
    data = getExif(id)
    if src and data:
        return render_template('_img_info.htm', id=id, src=src, data=data)
    return ERR_DATA
