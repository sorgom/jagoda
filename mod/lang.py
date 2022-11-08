from flask import redirect, render_template
from mod.MyDB import db
from mod.utilz import debug
from mod.login import loggedIn 
from mod.base import ERR_DATA, ERR_AUTH, rf, post

LANGS = None
ILCS  = None
LANG_ITEMS = None

def getLangs():
    global LANGS, ILCS, LANG_ITEMS
    if not LANGS:
        LANGS = db().getLangTable()
        ILCS  = [ l[0] for l in LANGS ]
        LANG_ITEMS = db().getLangItemTypeTable()

def langs():
    getLangs()
    return LANGS

def ilcs():
    getLangs()
    return ILCS

def langItems():
    getLangs()
    return LANG_ITEMS

def renderBase(template:str, **args):
    getLangs()
    return render_template(template, langs=LANGS, ilcs=ILCS, langItems=LANG_ITEMS, **args)

def getLangElemTable(tpc:str):
    getLangs()
    data = db().getLangElemTable(tpc)
    fnd = {}
    for (id, ilc, label) in data:
        fnd.setdefault(id, {})[ilc] = label
    return [ [ id, [ fnd[id].get(ilc, '') for ilc in ILCS ] ] for id in fnd.keys() ]

def getLangElem(id:int):
    getLangs()
    data = db().getLangElem(id)
    fnd = { ilc:value for ilc, value in data }
    return [ [ilc, label, fnd.get(ilc, '')] for ilc, label in LANGS ]

#   listing of all language elements of a type
#   html: language elements listing
def langElemTable(tpc:str):
    title = db().getLangItemTypeLabel(tpc)
    if not title: return redirect('/')
    return renderBase('GEN_lang_table.htm', tpc=tpc, title=title, rows=getLangElemTable(tpc))

def _langElem(id:int):
    debug(f'_langElem({id})')
    if not loggedIn(): return ERR_AUTH
    # res = render_template('_lang_elem.htm', id=id, rows=getLangElem(id), submit=f'_setbabl/{id}')
    # debug(res)
    # return res
    return render_template('_lang_elem.htm', id=id, rows=getLangElem(id), submit=f'_setlang/{id}')


def _langElemTable(tpc:str):
    if not loggedIn(): return ERR_AUTH
    return renderBase('_lang_table.htm', tpc=tpc, rows=getLangElemTable(tpc))

#   set language element data
#   return language table of element type
def _setlang(id:int):
    if not loggedIn(): return ERR_AUTH
    tpc = db().getLangItemType(id)
    if not tpc: return ERR_DATA
    getLangs()
    for ilc in ILCS:
        db().setLangElem(id, ilc, rf(ilc))
    return _langElemTable(tpc)

#   ajax get: new babl entry form
def _newLangForm(tpc:str):
    debug(f'_newLangForm({tpc})')
    if not loggedIn(): return ERR_AUTH
    id = db().getNextLangId()
    return render_template('_lang_elem.htm', id=id, rows=getLangElem(id), submit=f'_newlang/{tpc}/{id}')

#   ajax post: new language entry
def _newLang(tpc:str, id:int):
    debug(f'_newlang({tpc}, {id})')
    if not loggedIn(): return ERR_AUTH
    db().newLangItem(id, tpc)
    return _setlang(id)