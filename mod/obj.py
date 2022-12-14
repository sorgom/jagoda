# processing of objects
from flask import request, redirect
import json
from mod.lang import renderLang, getTtl, saveTtl, getLabelClass, getLabelDefClass
from mod.MyDB import db, DIM_FIELDS
from mod.login import loggedIn, checkLogin 
from mod.base import *
from mod.popups import *

def renderObj(objId:int, template:str, what='obj', **args):
    obj = db().getObj(objId)
    debug('OBJ:', obj)
    # objImg, objTitel = db().getObjImg(objId)
    # debug(objImg, objTitel)
    return renderLang(template, obj=obj, objId=objId, what='obj', title=f'OBJ', id=objId, **args)

def expandObjs(data:list):
    return [
        [id, src, label, getLabelClass(label), wlabel, getLabelClass(wlabel)]
        for id, src, label, wlabel in data
    ]  

def _updObj(objId:int):
    if post():
        db().updObj(objId, formDict('PUB', 'VAL'))

    return toJson(db().getObj(objId))

def newObj():
    return redirect(f'/newObjTtl/{db().getNextId()}')

def newObjTtl(objId:int):
    return renderLang('aut_new_art_1.jade', objId=objId, title='New Object')

def _newObjStdTtl(objId:int):
    debug(objId)
    if not loggedIn(): return ERR_AUTH
    items = db().getStdTtlsForSelect()
    return renderLang('popup_title_selector.jade', items=items, submit=f'_newObj2/{objId}', replace=f'/edObj/{objId}', title=f'select standard title for object {objId}')

def _newObjTtl(objId:int):
    debug(objId)
    if not loggedIn(): return ERR_AUTH
    ttlId = db().getNextId()
    info  = db().getNewTtlInfo('OT')
    return renderLang('popup_ttl.jade', objId=objId, id=ttlId, data=getTtl(ttlId), info=info, onsubmit=submitPopup(f'/_newObj2/{objId}/{ttlId}', f'/edObj/{objId}'), title=f'title of object {objId}')

#   save object & title
def _newObj2(objId:int, ttlId:int):
    if not loggedIn(): return ERR_AUTH
    if post():
        debug('POST', objId, ttlId)
        db().addObjTtl(ttlId)
        saveTtl(ttlId)
        debug('call addObj', objId, ttlId)
        db().addObj(objId, ttlId)
    else:
        debug('GET', objId, ttlId)
        db().addObj(objId, ttlId)
    return 'DONE'

def _setObjDims(objId:int, data:dict):
    db().updObj(objId, data)

def _objDims(objId:int):
    if post():
        _setObjDims(objId, dict(request.form))
        return db().getObjDims(objId)
    return renderLang('popup_obj_dims.jade', obj=db().getObj(objId), submit=f'_objDims/{objId}', field='objDims')

def edObj(objId:int):
    return renderObj(objId, 'aut_ed_obj.jade')

def _objSelWhat(objId:int):
    defId = db().getWhat(objId)
    data = [[id, label, getLabelDefClass(label, defId, id)] for id, label in db().getWhats()]
    return renderLang('popup_obj_sel_what.jade', submit=f'_objSetWhat/{objId}', field='WLABEL', data=data, title='select kind of object')

def _objSetWhat(objId:int, wId:int):
    db().setWhat(objId, wId)
    ret = db().getTtlLabel(wId)
    debug(ret)
    return ret

def _objImg(objId:int):
    return db().getObjImg(objId)

#   object listing for popups
def _edObjList():
    return renderLang('popup_obj_selector.jade', items=db().getObjList(), action='edObj', title='recently edited objects')

def _edUsrObjList():
    return renderLang('popup_obj_selector.jade', items=expandObjs(db().getUsrObjs()), action='edObj', title='recently edited objects')

def _renderObjTtl(objId:int, info:dict, route:str):
    data = getTtl(info['TTL'])
    title = f'title of object {objId}'
    if info['STD'] == 1: title += ' (standard title)' 
    return renderLang('popup_ttl.jade', objId=objId, data=data, info=info, onsubmit=usePopupSubmit(f'/{route}/{objId}', 'LABEL'), title=title)

def _objWichTtl(objId:int):
    info = db().getObjTtlInfo(objId)
    if info['STD'] == 1:
        return renderLang('popup_obj_which_ttl.jade', objId=objId, title='which title')
    return _renderObjTtl(objId, info, '_objOwnTtl')    

def _objTtl(objId:int, info=None):
    if info is None:
        info = db().getObjTtlInfo(objId)
    debug(info)
    if post():
        saveTtl(info['TTL'])
        db().touchObj(objId)
        return db().getObjLabel(objId)
    return _renderObjTtl(objId, info, '_objTtl')    

def _objOwnTtl(objId:int):
    if post():
        ttlId = rf('TTL')
        saveTtl(ttlId)
        return db().setObjTtl(objId, ttlId)
    info = db().newObjTtl()
    return _renderObjTtl(objId, info, '_objOwnTtl')

