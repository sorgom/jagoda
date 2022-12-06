# processing of articles
from flask import render_template, request, redirect, escape
import json
from mod.lang import renderBase, getTtl, saveTtl
from mod.MyDB import db, DIM_FIELDS
from mod.login import loggedIn, checkLogin 
from mod.base import *
from mod.popups import *

def renderArt(objId:int, template:str, what='art', **args):
    art = db().getArt(objId)
    debug('ART:', art)
    # objImg, objTitel = db().getObjImgLabel(objId)
    # debug(objImg, objTitel)
    return renderBase(template, obj=art, objId=objId, what='art', title=f'Object no. {objId}', **args)

def _updArt(objId:int):
    if post():
        db().updArt(objId, formDict('PUB', 'VAL'))

    return toJson(db().getArt(objId))

def newArt():
    return redirect(f'/newArtTtl/{db().getNextId()}')

def newArtTtl(objId:int):
    return renderBase('aut_new_art_1.jade', objId=objId, title='New Article')

def _newArtStdTtl(objId:int):
    debug(objId)
    if not loggedIn(): return ERR_AUTH
    items = db().getStdTtlsForSelect()
    return render_template('popup_title_selector.jade', items=items, submit=f'_newArt2/{objId}', replace=f'/edArt/{objId}', title=f'select standard title for object {objId}')

def _newArtTtl(objId:int):
    debug(objId)
    if not loggedIn(): return ERR_AUTH
    ttlId = db().getNextId()
    info  = db().getNewTtlInfo('OT')
    return render_template('popup_ttl.jade', objId=objId, id=ttlId, data=getTtl(ttlId), info=info, onsubmit=submitPopup(f'/_newArt2/{objId}/{ttlId}', f'/edArt/{objId}'), title=f'title of object {objId}')

#   save article & title
def _newArt2(objId:int, ttlId:int):
    if not loggedIn(): return ERR_AUTH
    if post():
        debug('POST', objId, ttlId)
        db().addObjTtl(ttlId)
        saveTtl(ttlId)
        debug('call addArt', objId, ttlId)
        db().addArt(objId, ttlId)
    else:
        debug('GET', objId, ttlId)
        db().addArt(objId, ttlId)
    return 'DONE'

def _setObjDims(objId:int, data:dict):
    db().updObj(objId, data)

def _objDims(objId:int):
    if post():
        _setObjDims(objId, dict(request.form))
        return db().getObjDims(objId)
    return render_template('popup_obj_dims.jade', obj=db().getObj(objId), submit=f'_objDims/{objId}', field='objDims')

def edArt(objId:int):
    return renderArt(objId, 'out_ed_art.jade')

def _objSelWhat(objId:int):
    items = db().getWhats()
    return render_template('popup_obj_sel_what.jade', submit=f'_objSetWhat/{objId}', field='WLABEL', items=items, title='select kind of article')

def _objSetWhat(objId:int, wId:int):
    db().setWhat(objId, wId)
    ret = db().getTtl1st(wId)
    debug(ret)
    return ret

def _objImg(objId:int):
    return db().getObjImgLabel(objId)[0]

#   article listing for popups
def _edArtList():
    return render_template('popup_obj_selector.jade', items=db().getArtList(), action='edArt', title='recently edited articles')

def _edUsrArtList():
    return render_template('popup_obj_selector.jade', items=db().getUsrArt(), action='edArt', title='recently edited articles')

def _renderObjTtl(objId:int, info:dict, route:str):
    data = getTtl(info['TTL'])
    title = f'title of object {objId}'
    if info['STD'] == 1: title += ' (standard title)' 
    return render_template('popup_ttl.jade', objId=objId, data=data, info=info, onsubmit=usePopupSubmit(f'/{route}/{objId}', 'LABEL'), title=title)

def _objWichTtl(objId:int):
    info = db().getObjTtl(objId)
    if info['STD'] == 1:
        return render_template('popup_obj_which_ttl.jade', objId=objId, title='which title')
    return _renderObjTtl(objId, info, '_objOwnTtl')    

def _objTtl(objId:int, info=None):
    if info is None:
        info = db().getObjTtl(objId)
    debug(info)
    if post():
        saveTtl(info['TTL'])
        db().touchEnt(objId)
        return db().getObjLabel(objId)
    return _renderObjTtl(objId, info, '_objTtl')    

def _objOwnTtl(objId:int):
    if post():
        ttlId = rf('TTL')
        saveTtl(ttlId)
        return db().setObjTtl(objId, ttlId)
    info = db().newObjTtl()
    return _renderObjTtl(objId, info, '_objOwnTtl')

