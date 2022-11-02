# Application for Website Authoring

from flask import Flask, session, redirect, url_for, escape, request, render_template, Markup

import hashlib
from random import sample
from glob import glob

from tests.fakeData import fakeIdsWithMinis
from mod.MyDB import MyDB
from mod.getTemplates import genTemplates
from mod.saveImg import checkImgFolders, saveImg

app = Flask(__name__, template_folder='templates')

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
        BABLS = mydb.getBablTpTable()
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

def bablTableRows(tp:str):
    getLangs()
    data = mydb.getBablTable(tp)
    fnd = {}
    for (id, ilc, label) in data:
        fnd.setdefault(id, {})[ilc] = label
    return [ [ id, [ fnd[id].get(ilc, '') for ilc in ILCS ] ] for id in fnd.keys() ]

def bablFormRows(id:int):
    getLangs()
    data = mydb.getBabl(id)
    fnd = { ilc:value for ilc, value in data }
    return [ [ilc, label, fnd.get(ilc, '')] for ilc, label in LANGS ]

@app.route('/')
def index():
    return checkLogin() or renderBase('aut_index.htm', title='Overview')

@app.route('/login', methods=BOTH)
def login():
    if post():
        session.pop('id', None)
        session.pop('usr', None)
        usr = rf('usr')
        id = mydb.getId(usr, rf('pwd'))
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
@app.route('/babl/<tp>')
def bablTable(tp:str):
    c = checkLogin()
    if c: return c
    title = mydb.getBablTpLabel(tp)
    if not title: return redirect('/')
    return renderBase('GEN_babl_table.htm', tp=tp, title=title, rows=bablTableRows(tp))

#   innerHTML of div #content / ajax: language table of given type
@app.route('/_babl/<tp>')
def _bablTable(tp:str):
    if not loggedIn(): return ERR_AUTH
    return renderBase('_babl_table.htm', tp=tp, rows=bablTableRows(tp))

#   ajax post: update exsting single language element
#   return: babl table of element type
@app.route('/_setbabl/<int:id>', methods=POST)
def _setbabl(id:int):
    if not loggedIn(): return ERR_AUTH
    tp = mydb.getBablTp(id)
    if not tp: return ERR_DATA
    getLangs()
    for ilc in ILCS:
        mydb.setBabl(id, ilc, rf(ilc))
    return _bablTable(tp)

#   ajax get: babl entry form
@app.route('/_bablform/<int:id>')
def _bablform(id:int):
    print(f'_bablform({id})')
    if not loggedIn(): return ERR_AUTH
    return render_template('_babl_form.htm', id=id, rows=bablFormRows(id), submit=f'_setbabl/{id}')

#   ajax get: new babl entry form
@app.route('/_newbablform/<tp>')
def _newbablform(tp:str):
    print(f'_newbablform({tp})')
    if not loggedIn(): return ERR_AUTH
    id = mydb.getNextBablId()
    return render_template('_babl_form.htm', id=id, rows=bablFormRows(id), submit=f'_newbabl/{tp}/{id}')

#   ajax post: new single language entry  
#   return: babl table of element type
@app.route('/_newbabl/<tp>/<int:id>', methods=POST)
def _newbabl(tp:str, id:int):
    print(f'_newbabl({tp}, {id})')
    if not loggedIn(): return ERR_AUTH
    mydb.newBabl(id, tp)
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
