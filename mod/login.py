from flask import session, redirect, render_template
from mod.base import post, rf, debug
from mod.MyDB import db

def getUid() -> int:
    id = session.get('ID', 0)
    debug(id)
    return id

def loggedIn():
    return getUid() != 0

def login():
    if post():
        session.pop('ID', None)
        session.pop('USR', None)
        usr = rf('USR')
        id = db().getUsrId(usr, rf('PWD'))
        if id > 0:
            debug(id)
            debug(usr)
            session['ID']  = id
            session['USR'] = usr
            db().reduceEntRecs()
            return redirect('/')
    return render_template('aut_login.htm')

def checkLogin():
    return None if loggedIn() else relogin()

def relogin():
    return redirect('/login')

def pwd():
    c = checkLogin()
    if c: return c
    if post():
        if db().setPwd(session['ID'], rf('PWD1'), rf('PWD2')):
            return redirect('/')
    return render_template('aut_pwd.htm', title='Change Password')

def logout():
    session.pop('ID', None)
    session.pop('USR', None)
    return relogin()

def _loggedIn():
    return 'YES' if loggedIn() else ''    