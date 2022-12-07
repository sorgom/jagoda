from flask import redirect, render_template
import json
from mod.MyDB import db
from mod.login import loggedIn 
from mod.base import *
from mod.google import translate
from mod.popups import *

LANGS = None
ILCS  = None
TTPS = None

def getLangs():
    global LANGS, ILCS, TTPS
    if not LANGS:
        LANGS = db().getLangs()
        ILCS  = [ l[0] for l in LANGS ]
        TTPS = [item[0:2] for item in db().getTtps()]

def langs():
    getLangs()
    return LANGS

def ilcs():
    getLangs()
    return ILCS

def ttps():
    getLangs()
    return TTPS

def getTtls(tpc:str):
    return expandTtls(db().getTtls(tpc))

def getStdTtls():
    return expandTtls(db().getStdTtls())

def expandTtls(data:list):
    getLangs()
    fnd = {}
    for (id, ilc, label) in data:
        fnd.setdefault(id, {})[ilc] = label
    return [ [ id, [ fnd[id].get(ilc, '') for ilc in ILCS ] ] for id in fnd.keys() ]

#   ============================================================
#   CALLS
#   ============================================================
#   listing of all title elements of a type
# def ttls(tpc:str):
#     title = db().getTtpLabel(tpc)
#     if not title: return redirect('/')
#     return renderBase('GEN_lang_items.htm', tpc=tpc, title=title, items=getTtls(tpc))

#   ============================================================
#   API
#   ============================================================
#   save title elements from form
def saveTtl(id:int):
    debug(id)
    getLangs()
    db().setTtl(id, [[ilc, rf(ilc)] for ilc in ILCS])
    if rf('STDABLE'):
        db().setTtlStd(id, rf('STD'))

def getTtl(id:int):
    getLangs()
    data = db().getTtl(id)
    fnd = { ilc:value for ilc, value in data }
    return [ [ilc, label, fnd.get(ilc, '')] for ilc, label in LANGS ]

def renderBase(template:str, **args):
    getLangs()
    return render_template(template, langs=LANGS, ilcs=ILCS, ttps=TTPS, **args)
#   ============================================================
#   AJAX
#   ============================================================
#   listing of all lang items of a type
def _ttls(tpc:str):
    if not loggedIn(): return ERR_AUTH
    return renderBase('popup_ttls.jade', tpc=tpc, items=getTtls(tpc))

def _stdTtls():
    if not loggedIn(): return ERR_AUTH
    return renderBase('popup_ttls.jade', tpc='OT', items=db().getStdTtls(), title='standard titles')
    # return debugTemplate('popup_ttls.jade', tpc='OT', items=getStdTtls(), title='standard titles')

#   lising of elements of a title
def _ttl(id:int):
    debug(id)
    if not loggedIn(): return ERR_AUTH
    info = db().getTtlInfo(id)
    debug('info:', info)
    return render_template('popup_ttl.jade', itemId=id, data=getTtl(id), info=info, onsubmit=submitPopup(f'/_setTtl/{id}'))

#   set title element data
#   return language table of element type
def _setTtl(id:int):
    if not loggedIn(): return ERR_AUTH
    tpc = db().getTpc(id)
    if not tpc: return ERR_DATA
    saveTtl(id)
    return _ttls(tpc)

#   ajax get: new language entry form
def _newTtl(tpc:str):
    debug(tpc)
    if not loggedIn(): return ERR_AUTH
    id = db().getNextId()
    info = db().getNewTtlInfo(tpc)
    debug('new id:', id)
    return render_template('popup_ttl.jade', id=id, data=getTtl(id), info=info, onsubmit=submitPopup(f'/_addTtl/{tpc}/{id}'))

#   ajax post: new language entry
def _addTtl(tpc:str, id:int):
    debug(tpc, id)
    if not loggedIn(): return ERR_AUTH
    db().addTtl(id, tpc)
    return _setTtl(id)

def _label(id:int):
    return db().getFirstLabel(id)

def _google():
    res = []
    if post() and loggedIn():
        getLangs()
        data = dict(request.form)
        src = None
        for ilc in ILCS:
            val = data[ilc].strip()
            if val:
                src = ilc
                txt = val
                break
        if src is not None:
            for ilc in ILCS:
                val = data[ilc].strip()
                if ilc != src and not val:
                    res.append([ilc, translate(src, ilc, txt)])
    ret = json.dumps(res)
    debug(ret)
    return ret

