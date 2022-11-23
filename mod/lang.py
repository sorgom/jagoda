from flask import redirect, render_template
from mod.MyDB import db
from mod.login import loggedIn 
from mod.base import *

LANGS = None
ILCS  = None
LANG_ITEMS = None

def getLangs():
    global LANGS, ILCS, LANG_ITEMS
    if not LANGS:
        LANGS = db().getLangTable()
        ILCS  = [ l[0] for l in LANGS ]
        LANG_ITEMS = [item[0:2] for item in db().getLangItemTypeTable()]

def langs():
    getLangs()
    return LANGS

def ilcs():
    getLangs()
    return ILCS

def langItems():
    getLangs()
    return LANG_ITEMS

def getLangItems(tpc:str):
    getLangs()
    data = db().getLangItems(tpc)
    fnd = {}
    for (id, ilc, label) in data:
        fnd.setdefault(id, {})[ilc] = label
    return [ [ id, [ fnd[id].get(ilc, '') for ilc in ILCS ] ] for id in fnd.keys() ]

#   ============================================================
#   CALLS
#   ============================================================
#   listing of all language elements of a type
#   html: language elements listing
def langItems(tpc:str):
    title = db().getLangItemTypeLabel(tpc)
    if not title: return redirect('/')
    return renderBase('GEN_lang_items.htm', tpc=tpc, title=title, items=getLangItems(tpc))

#   ============================================================
#   API
#   ============================================================
#   save lang item elements from form
def saveLangItem(id:int):
    getLangs()
    db().setLangItem(id, [[ilc, rf(ilc)] for ilc in ILCS])
    if rf('stdable'):
        db().setLangItemStd(id, rf('std'))

def getLangItem(id:int):
    getLangs()
    data = db().getLangItem(id)
    fnd = { ilc:value for ilc, value in data }
    return [ [ilc, label, fnd.get(ilc, '')] for ilc, label in LANGS ]

def renderBase(template:str, **args):
    getLangs()
    return render_template(template, langs=LANGS, ilcs=ILCS, langItems=LANG_ITEMS, **args)
#   ============================================================
#   AJAX
#   ============================================================
#   listing of all lang items of a type
def _langItems(tpc:str):
    if not loggedIn(): return ERR_AUTH
    return renderBase('_lang_items.htm', tpc=tpc, items=getLangItems(tpc))

#   lising of elements of a lang item
def _langItem(id:int):
    debug(id)
    if not loggedIn(): return ERR_AUTH
    item = db().getLangItemInfo(id)
    debug('item:', item)
    return render_template('_lang_item.htm', itemId=id, data=getLangItem(id), item=item, submit=f'_setLangItem/{id}')

#   set language item element data
#   return language table of element type
def _setLangItem(id:int):
    if not loggedIn(): return ERR_AUTH
    tpc = db().getLangItemType(id)
    if not tpc: return ERR_DATA
    saveLangItem(id)
    # getLangs()
    # db().setLangItem(id, [[ilc, rf(ilc)] for ilc in ILCS])
    # if rf('stdable'):
    #     db().setLangItemStd(id, rf('std'))
    return _langItems(tpc)

#   ajax get: new language entry form
def _newLangItem(tpc:str):
    debug(tpc)
    if not loggedIn(): return ERR_AUTH
    id = db().getNextId()
    item = db().getNewLangItemInfo(tpc)
    debug('new id:', id)
    return render_template('_lang_item.htm', id=id, data=getLangItem(id), item=item, submit=f'_addLangItem/{tpc}/{id}')

#   ajax post: new language entry
def _addLangItem(tpc:str, id:int):
    debug(tpc, id)
    if not loggedIn(): return ERR_AUTH
    db().newLangItem(id, tpc)
    return _setLangItem(id)

def _label(id:int):
    return db().getFirstLabel(id)