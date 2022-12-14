#   module requiring all others
from flask import session, redirect
from mod.login import checkLogin
from mod.base import post, rf
from mod.MyDB import db
from mod.lang import renderLang

def pwd():
    c = checkLogin()
    if c: return c
    if post():
        if db().setPwd(session['ID'], rf('PWD1'), rf('PWD2')):
            return redirect('/')
    return renderLang('aut_pwd.jade', title='CHG PWD')