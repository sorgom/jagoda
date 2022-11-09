# Application for Website Authoring

from flask import Flask, session, redirect, request, render_template

import hashlib
from random import sample
from glob import glob

from tests.fakeData import fakeIdsWithMinis
from mod.MyDB import MyDB
from mod.genTemplates import TEMPLATES_FOLDER, genTemplates
from mod.saveImg import checkImgFolders, saveImg

app = Flask(__name__, template_folder=TEMPLATES_FOLDER)

# secret string for session cooky
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'aut'
app.config['MYSQL_PASSWORD'] = 'aa'
app.config['MYSQL_DB'] = 'jagoda'

mydb = MyDB(app)

LANGS = None
ILCS  = None
BABLS = None

BOTH = ['GET', 'POST']
GET  = ['GET']
POST = ['POST']

ERR_DATA = 'DATA ERROR'
ERR_AUTH = 'NOT AUTHORIZED'

def rf(field:str):
    return request.form.get(field, '')

def post():
    return request.method == 'POST'

def getLangs():
    global LANGS, ILCS, BABLS
    if not LANGS:
        LANGS = mydb.getLangTable()
        ILCS  = [ l[0] for l in LANGS ]
        BABLS = mydb.getLangItemTypeTable()
    return LANGS

def relogin():
    return redirect('/login')

def checkLogin():
    if loggedIn():
        getLangs()
        return False
    return relogin()

def loggedIn():
    return 'id' in session

def renderBase(template:str, **args):
    getLangs()
    return render_template(template, langs=LANGS, ilcs=ILCS, babls=BABLS, **args)

def bablTableRows(tpc:str):
    getLangs()
    data = mydb.getLangElemTable(tpc)
    fnd = {}
    for (id, ilc, label) in data:
        fnd.setdefault(id, {})[ilc] = label
    return [ [ id, [ fnd[id].get(ilc, '') for ilc in ILCS ] ] for id in fnd.keys() ]

def bablFormRows(id:int):
    getLangs()
    data = mydb.getLangElem(id)
    fnd = { ilc:value for ilc, value in data }
    return [ [ilc, label, fnd.get(ilc, '')] for ilc, label in LANGS ]

@app.route('/')
def index():
    return checkLogin() or renderBase('aut_base.htm', title='Overview')

@app.route('/login', methods=BOTH)
def login():
    if post():
        session.pop('id', None)
        session.pop('usr', None)
        usr = rf('usr')
        id = mydb.getUsrId(usr, rf('pwd'))
        if id > 0:
            session['id']  = id
            session['usr'] = usr
            return redirect('/')
    return render_template('aut_login.htm')

@app.route('/pwd', methods=BOTH)
def pwd():
    c = checkLogin()
    if c: return c
    if post():
        if mydb.setPwd(session['id'], rf('pwd1'), rf('pwd2')):
            return redirect('/')
    return render_template('aut_pwd.htm', title='Change Password')

@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('usr', None)
    return relogin()

#   listing of all language elements of a type
#   html: language elements listing
@app.route('/babl/<tpc>')
def bablTable(tpc:str):
    c = checkLogin()
    if c: return c
    title = mydb.getLangItemTypeLabel(tpc)
    if not title: return redirect('/')
    return renderBase('GEN_babl_table.htm', tpc=tpc, title=title, rows=bablTableRows(tpc))

#   innerHTML of div #content / ajax: language table of given type
@app.route('/_babl/<tpc>')
def _bablTable(tpc:str):
    if not loggedIn(): return ERR_AUTH
    return renderBase('_babl_table.htm', tpc=tpc, rows=bablTableRows(tpc))

#   ajax post: update exsting single language element
#   return: babl table of element type
@app.route('/_setbabl/<int:id>', methods=POST)
def _setbabl(id:int):
    if not loggedIn(): return ERR_AUTH
    tpc = mydb.getLangItemType(id)
    if not tpc: return ERR_DATA
    getLangs()
    for ilc in ILCS:
        mydb.setLangElem(id, ilc, rf(ilc))
    return _bablTable(tpc)

#   ajax get: babl entry form
@app.route('/_bablform/<int:id>')
def _bablform(id:int):
    print(f'_bablform({id})')
    if not loggedIn(): return ERR_AUTH
    return render_template('_babl_form.htm', id=id, rows=bablFormRows(id), submit=f'_setbabl/{id}')

#   ajax get: new babl entry form
@app.route('/_newbablform/<tpc>')
def _newbablform(tpc:str):
    print(f'_newbablform({tpc})')
    if not loggedIn(): return ERR_AUTH
    id = mydb.getNextLangId()
    return render_template('_babl_form.htm', id=id, rows=bablFormRows(id), submit=f'_newbabl/{tpc}/{id}')

#   ajax post: new single language entry  
#   return: babl table of element type
@app.route('/_newbabl/<tpc>/<int:id>', methods=POST)
def _newbabl(tpc:str, id:int):
    print(f'_newbabl({tpc}, {id})')
    if not loggedIn(): return ERR_AUTH
    mydb.newLangItem(id, tpc)
    return _setbabl(id)

def preStart():
    genTemplates()
    checkImgFolders()

if __name__ == '__main__':
    preStart()

    # local
    app.run(host="localhost", port=8001, debug=True)
    # app.run(host="localhost", port=8001, debug=False)


    # real http acces
    # app.run(host='0.0.0.0', port=80, debug=False)
