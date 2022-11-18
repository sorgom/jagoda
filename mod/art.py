# processing of articles
from flask import render_template
from mod.lang import renderBase, getLangItem, saveLangItem
from mod.MyDB import db
from mod.login import loggedIn, checkLogin 
from mod.base import *

def newArt1():
    return renderBase('aut_new_art_1.htm', objId=db().getNextId(), title='New Article')

def _newArtStdTtl(objId:int):
    debug(__name__, objId)
    if not loggedIn(): return ERR_AUTH
    items = db().getStdTtls()
    return render_template('_assign_obj_title.htm', items=items, submit=f'_newArt2/{objId}')

def _newArtTtl(objId:int):
    debug(__name__, objId)
    if not loggedIn(): return ERR_AUTH
    ttlId = db().getNextId()
    item  = db().getNewLangItemInfo('OT')
    return render_template('_lang_item.htm', objId=objId, id=ttlId, data=getLangItem(ttlId), item=item, submit=f'_newArt2/{objId}/{ttlId}')

def _newArt2(objId:int, ttlId:int):
    if not loggedIn(): return ERR_AUTH
    if post():
        db().newObjTtl(ttlId)
        saveLangItem(ttlId)
    else:
        db().addArt(objId, ttlId)
    return 'New Art 2'

def newArt2P():
    pass
