from flask import Flask, request, redirect, render_template

from mod.MyDB import setDB, db
from mod.base import *
from mod import img, login, lang, saveImg, art, qrc
from mod.config import *

from flask_compress import Compress


#   industrial run:
# from gevent.pywsgi import WSGIServer


app = Flask(__name__, template_folder=TEMPLATES_FOLDER)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

# secret string for session cooky
app.secret_key = 'ein Hund kam in die Kueche'

app.config['MYSQL_HOST']        = '127.0.0.1'
app.config['MYSQL_USER']        = 'aut'
app.config['MYSQL_PASSWORD']    = 'aa'
app.config['MYSQL_DB']          = 'jagoda'
app.config['MYSQL_AUTOCOMMIT']  = 1

setDB(app, login.getUid, login.getUsrIlc)

Compress(app)

def route(route:str, meth, **opts):
    app.add_url_rule(route, view_func=meth, **opts)

def preStart():
    pass

@app.route('/')
def index():
    if login.loggedIn():
        return lang.renderBase('aut_base.jade')
    else:
        return redirect('/login')

@app.route('/t')
def testData():
    db().testData()
    return redirect('/')

@app.route('/d')
def d():
    return render_template('test_dropdown.htm')

# login
route('/login',                         login.login,        methods=BOTH)
route('/logout',                        login.logout                    )
route('/pwd',                           login.pwd,          methods=BOTH)
route('/_loggedIn',                     login._loggedIn                 )
route('/_setUsrIlc/<ilc>',              login._setUsrIlc                )

# language authoring
# route('/ttls/<tpc>',                    lang.ttls                  )
route('/_ttl/<int:id>',                 lang._ttl                  )
route('/_setTtl/<int:id>',              lang._setTtl,  methods=POST)
route('/_newTtl/<tpc>',                 lang._newTtl               )
route('/_addTtl/<tpc>/<int:id>',        lang._addTtl,  methods=POST)
route('/_label/<int:id>',               lang._label                )
route('/_google',                       lang._google,  methods=POST)
route('/_stdTtls',                      lang._stdTtls              )

# image ajax calls
route('/_addObjImgs/<int:objId>',   img._addObjImgs,    methods=POST)
route('/_objImgs/<int:objId>',      img._objImgs                    )
route('/_orderObjImgs/<int:objId>', img._orderObjImgs,  methods=POST)
route('/_rmObjImg',                 img._rmObjImg,      methods=POST)
route('/_unusedImgs',               img._unusedImgs                 )
route('/_imgInfo/<int:id>',         img._imgInfo                    )

# articles / objects
route('/newArt',                            art.newArt)
route('/_newArtStdTtl/<int:objId>',         art._newArtStdTtl)
route('/_newArtTtl/<int:objId>',            art._newArtTtl)
route('/newArtTtl/<int:objId>',             art.newArtTtl)
route('/_newArt2/<int:objId>/<int:ttlId>',  art._newArt2, methods=BOTH)
route('/edArt/<int:objId>',                 art.edArt)

route('/_edArtList',                        art._edArtList)
route('/_edUsrArtList',                     art._edUsrArtList)

route('/_objSelWhat/<int:objId>',           art._objSelWhat)
route('/_objSetWhat/<int:objId>/<int:wId>', art._objSetWhat)

route('/_objImg/<int:objId>',               art._objImg)
route('/_objDims/<int:objId>',              art._objDims,   methods=BOTH)
route('/_objTtl/<int:objId>',               art._objTtl,    methods=BOTH)
route('/_objOwnTtl/<int:objId>',            art._objOwnTtl, methods=BOTH)
route('/_objWhichTtl/<int:objId>',          art._objWichTtl)

route('/_updArt/<int:objId>',               art._updArt,    methods=BOTH)

# general
route('/_qrc_view/<int:id>/<what>',         qrc._qrc_view)
route('/_qrc_print/<int:id>/<what>',        qrc._qrc_print)

if __name__ == '__main__':
    preStart()

    app.run(host="localhost", port=8001, debug=True)

#   industrial run:
    # http_server = WSGIServer(('', 8001), app)
    # http_server.serve_forever()