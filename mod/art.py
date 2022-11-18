# processing of articles
from flask import render_template, request, redirect
from mod.lang import renderBase, getLangItem, saveLangItem
from mod.MyDB import db
from mod.login import loggedIn, checkLogin 
from mod.base import *

def newArt1():
    return renderBase('aut_new_art_1.htm', objId=db().getNextId(), title='New Article')

def _newArtStdTtl(objId:int):
    debug(objId)
    if not loggedIn(): return ERR_AUTH
    items = db().getStdTtls()
    return render_template('_assign_obj_title.htm', items=items, submit=f'_newArt2/{objId}')

def _newArtTtl(objId:int):
    debug(objId)
    if not loggedIn(): return ERR_AUTH
    ttlId = db().getNextId()
    item  = db().getNewLangItemInfo('OT')
    return render_template('_lang_item.htm', objId=objId, id=ttlId, data=getLangItem(ttlId), item=item, submit=f'_newArt2/{objId}/{ttlId}')

#   save article & title
#   display dimensions form
def _newArt2(objId:int, ttlId:int):
    if not loggedIn(): return ERR_AUTH
    if post():
        db().newObjTtl(ttlId)
        saveLangItem(ttlId)
    else:
        db().addArt(objId, ttlId)
    return render_template('_new_art_2.htm', art={}, objId=objId)

#   save dimensions
#   display image site
def _newArt3(objId:int):
    debug(request.form)
    return redirect('/')

def _objImg(objId:int):
    return db().getObjImgLabel(objId)[0]

def renderObj(objId:int, template:str, what='art', **args):
    objImg, objTitel = db().getObjImgLabel(objId)
    debug(objImg, objTitel)
    return renderBase(template, objId=objId, objImg=objImg, objTitel=objTitel, what=what, **args)
