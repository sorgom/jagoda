# processing of articles
from flask import render_template, redirect
from mod.lang import renderBase, getLangItem
from mod.MyDB import db
from mod.utilz import debug
from mod.login import loggedIn 
from mod.base import ERR_DATA, ERR_AUTH, rf, post

def newArt1():
    return renderBase('aut_new_art_1.htm', objId=db().getNextId())

def _newArtStdTtl(objId:int):
    debug(__name__, objId)
    if not loggedIn(): return ERR_AUTH
    items = db().getStdTtls()
    return render_template('_assign_obj_title.htm', objId=objId, items=items, action='/newArt2')

def _newArtTtl(objId:int):
    debug(__name__, objId)
    if not loggedIn(): return ERR_AUTH
    ttlId = db().getNextId()
    item  = db().getNewLangItemInfo('OT')
    return render_template('_lang_item.htm', objId=objId, id=ttlId, data=getLangItem(ttlId), item=item, action=f'/newArt2/{objId}/{ttlId}')

def newArt2G(objId:int, ttlId:int):
    db().addArt(objId, ttlId)
    return redirect('/')

def newArt2P():

