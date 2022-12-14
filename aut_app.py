from flask import Flask, request, redirect, render_template

from mod.MyDB import setDB, db
from mod.base import *
from mod import img, login, lang, saveImg, obj, qrc, test, meta
from mod.config import *

from flask_compress import Compress


#   industrial run:
# from gevent.pywsgi import WSGIServer


app = Flask(__name__, template_folder=TEMPLATES_FOLDER)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

# secret string for session cooky
app.secret_key = 'ein Hund kam in die Kueche'

app.config['MYSQL_HOST']        = DB_CONFIG['host']
app.config['MYSQL_USER']        = DB_CONFIG['user']
app.config['MYSQL_PASSWORD']    = DB_CONFIG['password']
app.config['MYSQL_DB']          = DB_CONFIG['database']
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
        return lang.renderLang('aut_base.jade')
    else:
        return redirect('/login')

@app.route('/t')
def testData():
    db().testData()
    return redirect('/')

@app.route('/d')
def d():
    return render_template('test_dropdown.htm')


route('/test', test.test)

# login
route('/login',                         login.login,        methods=BOTH)
route('/logout',                        login.logout                    )
route('/pwd',                           meta.pwd,          methods=BOTH)
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
# standard titles
route('/stdTtls',                       lang.stdTtls               )
route('/_stdTtls',                      lang._stdTtls              )
route('/_stdTtl/<int:id>',              lang._stdTtl                )
route('/_setStdTtl/<int:id>',           lang._setStdTtl, methods=POST)
route('/_newStdTtl',                    lang._newStdTtl             )
route('/_addStdTtl/<int:id>',           lang._addStdTtl, methods=POST)
# object kinds
route('/whats',                         lang.whats                   )
route('/_whats',                        lang._whats                  )
route('/_what/<int:id>',                lang._what                   )
route('/_setWhat/<int:id>',             lang._setWhat,   methods=POST)
route('/_newWhat',                      lang._newWhat                )
route('/_addWhat/<int:id>',             lang._addWhat,   methods=POST)


# image ajax calls
route('/_addObjImgs/<int:objId>',   img._addObjImgs,    methods=POST)
route('/_objImgs/<int:objId>',      img._objImgs                    )
route('/_orderObjImgs/<int:objId>', img._orderObjImgs,  methods=POST)
route('/_rmObjImg',                 img._rmObjImg,      methods=POST)
route('/_unusedImgs',               img._unusedImgs                 )
route('/_imgInfo/<int:id>',         img._imgInfo                    )

# articles / objects
route('/newObj',                            obj.newObj)
route('/_newObjStdTtl/<int:objId>',         obj._newObjStdTtl)
route('/_newObjTtl/<int:objId>',            obj._newObjTtl)
route('/newObjTtl/<int:objId>',             obj.newObjTtl)
route('/_newObj2/<int:objId>/<int:ttlId>',  obj._newObj2, methods=BOTH)
route('/edObj/<int:objId>',                 obj.edObj)

route('/_edObjList',                        obj._edObjList)
route('/_edUsrObjList',                     obj._edUsrObjList)

route('/_objSelWhat/<int:objId>',           obj._objSelWhat)
route('/_objSetWhat/<int:objId>/<int:wId>', obj._objSetWhat)

route('/_objImg/<int:objId>',               obj._objImg)
route('/_objDims/<int:objId>',              obj._objDims,   methods=BOTH)
route('/_objTtl/<int:objId>',               obj._objTtl,    methods=BOTH)
route('/_objOwnTtl/<int:objId>',            obj._objOwnTtl, methods=BOTH)
route('/_objWhichTtl/<int:objId>',          obj._objWichTtl)

route('/_updObj/<int:objId>',               obj._updObj,    methods=BOTH)

# general
route('/_qrc_view/<int:id>/<what>',         qrc._qrc_view)
route('/_qrc_print/<int:id>/<what>',        qrc._qrc_print)

if __name__ == '__main__':
    preStart()

    app.run(host="localhost", port=8001, debug=True)

#   industrial run:
    # http_server = WSGIServer(('', 8001), app)
    # http_server.serve_forever()