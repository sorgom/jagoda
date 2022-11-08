from flask import session, redirect, render_template
from mod.base import post, rf
from mod.MyDB import db

def loggedIn():
    return session.get('id')

def login():
    if post():
        session.pop('id', None)
        session.pop('usr', None)
        usr = rf('usr')
        id = db().getId(usr, rf('pwd'))
        if id > 0:
            session['id']  = id
            session['usr'] = usr
            return redirect('/')
    return render_template('aut_login.htm')

def checkLogin():
    return False if loggedIn() else relogin()

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