from mod.MyDB import db
from mod.base import *
from mod.saveImg import saveImg, getImgMini

# TODO: make part of config
MAX_NUM_IMGES = 8

def mkJson(data, withMax:bool=False):
    return json.dumps({ 'data':data, 'max':MAX_NUM_IMGES if withMax else 0})

def _objImgs(objId:int):
    print('_objImgs:', objId)
    res = []
    for img in db().getObjectImgs(objId):
        src = getImgMini(img['id'])
        if src:
            img['src'] = src
            res.append(img)
    return mkJson(res, True)

def _addObjImgs(objId:int):
    print('_addObjImgs:', objId)
    files = request.files.getlist('files')
    for file in files: saveImg(file, objId)
    return _objImgs(objId)

def _orderObjImgs(objId:int):
    print('_orderObjImgs', objId)
    for imgId, ord in getJson():
        print(objId, imgId, ord)
        db().setObjectImg(objId, imgId, ord)
    return '.'

def _rmObjImg():
    print('_rmObjImg')
    db().rmObjectImg(rf('objId'), rf('imgId'))
    return '.'

def _unusedImgs():
    print('_unusedImgs')
    res = []
    imgs = db().getUnusedImgs()
    for img in imgs:
        src = getImgMini(img['id'])
        if src:
            img['src'] = src
            res.append(img)
    return mkJson(res)
