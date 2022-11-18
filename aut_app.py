from flask import Flask, request, redirect, render_template

from mod.MyDB import setDB, db
from mod.genTemplates import TEMPLATES_FOLDER, genTemplates
from mod.base import *
from mod import img, login, lang, saveImg, art, qrc
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

@app.route('/')
def index():
    return lang.renderBase('aut_obj_imgs.htm', objId=102003, acceptImgTypes=IMG_TYPE_ACCEPTED)

@app.route('/t')
def testData():
    db().testData()
    return redirect('/')

# login
route('/login',                     login.login,        methods=BOTH)
route('/logout',                    login.logout                    )
route('/pwd',                       login.pwd,          methods=BOTH)
route('/_loggedIn',                 login._loggedIn                 )

# language authoring
route('/langItems/<tpc>',               lang.langItems                  )
route('/_langItem/<int:id>',            lang._langItem                  )
route('/_setLangItem/<int:id>',         lang._setLangItem,  methods=POST)
route('/_newLangItem/<tpc>',            lang._newLangItem               )
route('/_addLangItem/<tpc>/<int:id>',   lang._addLangItem,  methods=POST)
route('/_label/<int:id>',               lang._label                     )

# image ajax calls
route('/_addObjImgs/<int:objId>',   img._addObjImgs,    methods=POST)
route('/_objImgs/<int:objId>',      img._objImgs                    )
route('/_orderObjImgs/<int:objId>', img._orderObjImgs,  methods=POST)
route('/_rmObjImg',                 img._rmObjImg,      methods=POST)
route('/_unusedImgs',               img._unusedImgs                 )
route('/_imgInfo/<int:id>',         img._imgInfo                    )

# articles
route('/newArt',                            art.newArt1)
route('/_newArtStdTtl/<int:objId>',         art._newArtStdTtl)
route('/_newArtTtl/<int:objId>',            art._newArtTtl)
route('/_newArt2/<int:objId>/<int:ttlId>',  art._newArt2, methods=BOTH)

# general
route('/_qrc/<int:id>/<what>',           qrc._qrc)

if __name__ == '__main__':
    preStart()

    app.run(host="localhost", port=8001, debug=True)