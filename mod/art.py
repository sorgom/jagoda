# processing of articles
from flask import render_template, request, redirect
from mod.lang import renderBase, getLangItem, saveLangItem
from mod.MyDB import db
from mod.login import loggedIn, checkLogin 
from mod.base import *

DIM_FIELDS = [f'dim{n}' for n in range(1,4)]

def renderArt(objId:int, template:str, what='art', **args):
    art = db().getArt(objId)
    debug(art)
    # objImg, objTitel = db().getObjImgLabel(objId)
    # debug(objImg, objTitel)
    return renderBase(template, obj=art, objId=objId, what='art', **args)

def newArt():
    return redirect(f'/newArtTtl/{db().getNextId()}')

def newArtTtl(objId:int):
    return renderBase('aut_new_art_1.htm', objId=objId, title='New Article')

def _newArtStdTtl(objId:int):
    debug(objId)
    if not loggedIn(): return ERR_AUTH
    items = db().getStdTtls()
    return render_template('_title_selector.htm', items=items, submit=f'_newArt2/{objId}', replace=f'/objDims/{objId}')

def _newArtTtl(objId:int):
    debug(objId)
    if not loggedIn(): return ERR_AUTH
    ttlId = db().getNextId()
    item  = db().getNewLangItemInfo('OT')
    return render_template('_lang_item.htm', objId=objId, id=ttlId, data=getLangItem(ttlId), item=item, submit=f'_newArt2/{objId}/{ttlId}', replace=f'/objDims/{objId}')

#   save article & title
#   display dimensions form
def _newArt2(objId:int, ttlId:int):
    if not loggedIn(): return ERR_AUTH
    if post():
        debug('POST', objId, ttlId)
        db().newObjTtl(ttlId)
        saveLangItem(ttlId)
        db().addArt(objId, ttlId)
    else:
        debug('GET', objId, ttlId)
        db().addArt(objId, ttlId)
    return 'DONE'


def _objDims(objId:int):
    if post():
        data = dict(request.form)
        factor = 2.54 if data['unit'] == 'inch' else 1.0
        rdims = [
            float((data[d] or '0').replace(',', '.')) * factor
            for d in DIM_FIELDS
        ]
        debug('rdims', rdims)
        db().setObjDims(objId, rdims)
        return db().getObjDims(objId)
    
    return render_template('_obj_dims.htm', obj=db().getObj(objId))



def objDims(objId:int):
    if post():
        data = dict(request.form)
        factor = 2.54 if data['unit'] == 'inch' else 1.0
        rdims = [
            float((data[d] or '0').replace(',', '.')) * factor
            for d in DIM_FIELDS
        ]
        debug('rdims', rdims)
        db().setObjDims(objId, rdims)
        return redirect(f'/edArt/{objId}')
    
    return renderArt(objId, 'aut_obj_dims.htm')

def edArt(objId:int):
    return renderArt(objId, 'aut_obj_base.htm')

def objImgs(objId:int):
    return renderArt(objId, 'aut_obj_imgs.htm')

def _objSelWhat(objId:int):
    items = db().getWhats()
    return render_template('_obj_sel_what.htm', submit=f'_objSetWhat/{objId}', field='objWhat', items=items)

def _objSetWhat(objId:int, wId:int):
    db().setWhat(objId, wId)
    ret = db().getLangElem1st(wId)
    debug(ret)
    return ret

def _objImg(objId:int):
    return db().getObjImgLabel(objId)[0]

#   article listing for popups
def _edArtList():
    return render_template('_obj_selector.htm', items=db().getArtList(), action='edArt')
