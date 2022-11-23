from flask import session, redirect, render_template
from mod.base import post, rf
from mod.MyDB import db

def getUid() -> int:
    return session.get('id', 0)

def loggedIn():
    return getUid() != 0

def login():
    if post():
        session.pop('id', None)
        session.pop('usr', None)
        usr = rf('usr')
        id = db().getUsrId(usr, rf('pwd'))
        if id > 0:
            session['id']  = id
            session['usr'] = usr
            db().reduceObjRecs()
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
        if db().setPwd(session['id'], rf('pwd1'), rf('pwd2')):
            return redirect('/')
    return render_template('aut_pwd.htm', title='Change Password')

def logout():
    session.pop('id', None)
    session.pop('usr', None)
    return relogin()

def _loggedIn():
    return 'YES' if loggedIn() else 'NO'    