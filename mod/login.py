from flask import session, redirect, render_template
from mod.base import post, rf
from mod.MyDB import db

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