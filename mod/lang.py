from flask import redirect, render_template
import json, re
from mod.MyDB import db
from mod.login import loggedIn, getUsrIlc, checkLogin 
from mod.base import *
from mod.google import translate
from mod.popups import *

LANGS = None
ILCS  = None
LANG_LABELS = None
TTPS = None
RX_FOREIGN = None
CAPS = None

def getLangs():
    global LANGS, ILCS, LANG_LABELS, TTPS, RX_FOREIGN
    if not LANGS:
        LANGS = db().getLangs()
        ILCS  = [ l[0] for l in LANGS ]
        LANG_LABELS = { i:l for i, l in LANGS }
        TTPS = [item[0:2] for item in db().getTtps()]
        RX_FOREIGN = re.compile(r'^\((' + '|'.join(ILCS) + r'|\?' + r')\).*')
        loadCaps()

def loadCaps():
    global CAPS
    CAPS = {
        ilc: {
            cpc: label
            for cpc, label in db().getCapsPro(ilc)
        }
        for ilc in ILCS
    }
    debug(type(CAPS))

def getLabelClass(label:str):
    getLangs()
    return 'foreign' if RX_FOREIGN.match(label) else 'OK'

def getLabelDefClass(label:str, defId:int, id:int):
    getLangs()
    cl = getLabelClass(label)
    if (id == defId): cl += ' def'
    return cl

#   expand list of title
def expandTtls(data:list):
    getLangs()
    return [[id, label, getLabelClass(label)] for id, label in data]

#   expand title elements
def expandTtl(data:list):
    getLangs()
    fnd = { ilc:label for ilc, label in data }
    return [ [ilc, label, fnd.get(ilc, '')] for ilc, label in LANGS ]

def getTtls(tpc:str):
    return expandTtls(db().getTtls(tpc))

def getStdTtls():
    return expandTtls(db().getStdTtls())

def getWhats():
    return expandTtls(db().getWhats())

def getCaps():
    getLangs()
    return [[id, cpc, label, getLabelClass(label)] for id, cpc, label in db().getCaps()]

def fndCap(src:dict, cpc:str):
    return src.get(cpc, f'*{cpc}*') if cpc else ''

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

def saveCap(id:int):
    debug(id)
    getLangs()
    db().setCap(id, [[ilc, rf(ilc)] for ilc in ILCS])
    loadCaps()

def getTtl(id:int):
    return expandTtl(db().getTtl(id))
    # getLangs()
    # data = db().getTtl(id)
    # fnd = { ilc:value for ilc, value in data }
    # return [ [ilc, label, fnd.get(ilc, '')] for ilc, label in LANGS ]

def renderLang(template:str, **args):
    getLangs()
    usrIlc=getUsrIlc()
    caps = CAPS.get(usrIlc, {})
    return render_template(
        template, langs=LANGS, ilcs=ILCS, ttps=TTPS, usrIlc=usrIlc, usrLang=LANG_LABELS.get(usrIlc, '??'),
        cap=lambda c : fndCap(caps, c),
        **args
    )
#   ============================================================
#   AJAX
#   ============================================================
#   listing of all lang items of a type
def _ttls(tpc:str):
    if not loggedIn(): return ERR_AUTH
    return renderLang('popup_ttls.jade', tpc=tpc, items=getTtls(tpc))


#   lising of elements of a title
def _ttl(id:int):
    debug(id)
    if not loggedIn(): return ERR_AUTH
    info = db().getTtlInfo(id)
    debug('info:', info)
    return renderLang('popup_ttl.jade', itemId=id, data=getTtl(id), info=info, onsubmit=submitPopup(f'/_setTtl/{id}'))

#   set title element data
#   return language table of element type
def _setTtl(id:int):
    if not loggedIn(): return ERR_AUTH
    tpc = db().getTpc(id)
    if not tpc: return ERR_DATA
    saveTtl(id)
    return _ttls(tpc)

#   ============================================================
##  standard titles
#   ============================================================
#   listing of standard titles (full html)
def stdTtls():
    c = checkLogin()
    if c: return c
    return renderLang('aut_std_ttls.jade', items=getStdTtls(), title='STD TTLS')

#   listing of standard titles (ajax, content)
def _stdTtls():
    if not loggedIn(): return ERR_AUTH
    return renderLang('_std_ttls.jade', items=getStdTtls())

#   display of standard title (ajax, popup)
def _stdTtl(id:int):
    debug(id)
    if not loggedIn(): return ERR_AUTH
    info = db().getTtlInfo(id)
    debug('info:', info)
    return renderLang('popup_ttl.jade', itemId=id, data=getTtl(id), info=info, 
        onsubmit=submitPopup(f'/_setStdTtl/{id}'), title='ED STD TTL')

def _newStdTtl():
    debug()
    if not loggedIn(): return ERR_AUTH
    id = db().getNextId()
    info = db().getNewTtlInfo('OT')
    info['STD'] = 1
    return renderLang('popup_ttl.jade', id=id, data=getTtl(id), info=info, 
        onsubmit=submitPopupScrollDown(f'/_addStdTtl/{id}'), title='NEW STD TTL')

#   ajax post: new language entry
def _addStdTtl(id:int):
    debug(id)
    if not loggedIn(): return ERR_AUTH
    db().addTtl(id, 'OT')
    return _setStdTtl(id)

def _setStdTtl(id:int):
    if not loggedIn(): return ERR_AUTH
    saveTtl(id)
    return _stdTtls()

#   ============================================================
##  object kinds (what)
#   ============================================================
#   listing of whats (full html)
def whats():
    c = checkLogin()
    if c: return c
    return renderLang('aut_whats.jade', data=getWhats(), title='WHATS')

#   listing of whats (ajax, content)
def _whats():
    if not loggedIn(): return ERR_AUTH
    return renderLang('_whats.jade', data=getWhats())

#   display of an object kind (ajax, popup)
def _what(id:int):
    debug(id)
    if not loggedIn(): return ERR_AUTH
    info = db().getTtlInfo(id)
    debug('info:', info)
    return renderLang('popup_ttl.jade', itemId=id, data=getTtl(id), info=info,
        onsubmit=submitPopup(f'/_setWhat/{id}'), title='ED WHAT')

def _newWhat():
    debug()
    if not loggedIn(): return ERR_AUTH
    id = db().getNextId()
    info = db().getNewTtlInfo('TQ')
    return renderLang('popup_ttl.jade', id=id, data=getTtl(id), info=info, 
        onsubmit=submitPopupScrollDown(f'/_addWhat/{id}'), title='NEW WHAT')

#   ajax post: new what
def _addWhat(id:int):
    debug(id)
    if not loggedIn(): return ERR_AUTH
    db().addTtl(id, 'TQ')
    return _setWhat(id)

def _setWhat(id:int):
    if not loggedIn(): return ERR_AUTH
    saveTtl(id)
    return _whats()

#   ============================================================
##  captions (cap)
#   ============================================================
#   listing of caps (full html)
def caps():
    c = checkLogin()
    if c: return c
    return renderLang('aut_caps.jade', data=getCaps(), title='CAPS')

#   listing of caps (ajax, content)
def _caps():
    if not loggedIn(): return ERR_AUTH
    return renderLang('_caps.jade', data=getCaps())

#   display of a caption (ajax, popup)
def _cap(id:int):
    debug(id)
    if not loggedIn(): return ERR_AUTH
    cpc = db().getCapCpc(id)
    if not cpc: return ERR_DATA
    data = expandTtl(db().getCap(id))
    return renderLang('popup_cap_ed.jade', cpc=cpc, data=data,
        onsubmit=submitPopup(f'/_setCap/{id}'), title='ED CAP')

# def _newWhat():
#     debug()
#     if not loggedIn(): return ERR_AUTH
#     id = db().getNextId()
#     info = db().getNewTtlInfo('TQ')
#     return renderLang('popup_ttl.jade', id=id, data=getTtl(id), info=info, 
#         onsubmit=submitPopupScrollDown(f'/_addWhat/{id}'), title='NEW WHAT')

# #   ajax post: new language entry
# def _addWhat(id:int):
#     debug(id)
#     if not loggedIn(): return ERR_AUTH
#     db().addTtl(id, 'TQ')
#     return _setWhat(id)

def _setCap(id:int):
    if not loggedIn(): return ERR_AUTH
    saveCap(id)
    return _caps()


#   ============================================================
##  object titles
#   ============================================================
#   ajax get: new language entry form
def _newTtl(tpc:str):
    debug(tpc)
    if not loggedIn(): return ERR_AUTH
    id = db().getNextId()
    info = db().getNewTtlInfo(tpc)
    debug('new id:', id)
    return renderLang('popup_ttl.jade', id=id, data=getTtl(id), info=info, 
        onsubmit=submitPopup(f'/_addTtl/{tpc}/{id}'), title='NEW TTL')

#   ajax post: new language entry
def _addTtl(tpc:str, id:int):
    debug(tpc, id)
    if not loggedIn(): return ERR_AUTH
    db().addTtl(id, tpc)
    return _setTtl(id)

def _label(id:int):
    return db().getTtlLabel(id)

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

