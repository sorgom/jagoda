from flask import Flask, request, redirect, render_template

from mod.MyDB import setDB
from mod.genTemplates import TEMPLATES_FOLDER, genTemplates
from mod.saveImg import checkImgFolders
from mod.base import *
import mod.img, mod.login, mod.lang, mod.saveImg
from mod.config import *

app = Flask(__name__, template_folder=TEMPLATES_FOLDER)

# secret string for session cooky
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'aut'
app.config['MYSQL_PASSWORD'] = 'aa'
app.config['MYSQL_DB'] = 'jagoda'

setDB(app)

def route(route:str, meth, **opts):
    app.add_url_rule(route, view_func=meth, **opts)

def preStart():
    genTemplates()
    checkImgFolders()

@app.route('/')
def index():
    return mod.lang.renderBase('aut_obj_imgs.htm', objId=4711, acceptImgTypes=IMG_TYPE_ACCEPTED)

# login
route('/login',                     mod.login.login,        methods=BOTH)
route('/logout',                    mod.login.logout                    )
route('/pwd',                       mod.login.pwd,          methods=BOTH)
route('/_loggedIn',                 mod.login._loggedIn                 )

# language authoring
route('/lang/<tpc>',                mod.lang.langElemTable              )
route('/_langElem/<int:id>',        mod.lang._langElem                  )
route('/_setLang/<int:id>',         mod.lang._setLang,      methods=POST)
route('/_newLangForm/<tpc>',        mod.lang._newLangForm               )
route('/_newLang/<tpc>/<int:id>',   mod.lang._newLang,      methods=POST)

# image ajax calls
route('/_addObjImgs/<int:objId>',   mod.img._addObjImgs,    methods=POST)
route('/_objImgs/<int:objId>',      mod.img._objImgs                    )
route('/_orderObjImgs/<int:objId>', mod.img._orderObjImgs,  methods=POST)
route('/_rmObjImg',                 mod.img._rmObjImg,      methods=POST)
route('/_unusedImgs',               mod.img._unusedImgs                 )
route('/_imgInfo/<int:id>',         mod.img._imgInfo                    )


if __name__ == '__main__':
    preStart()

    app.run(host="localhost", port=8001, debug=True)