
from flask import Flask, request, redirect, render_template

from mod.MyDB import setDB
from mod.genTemplates import TEMPLATES_FOLDER, genTemplates
from mod.saveImg import checkImgFolders
from mod.base import *
import mod.img
import mod.login

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
    return render_template('ajax_upload.htm', id=4711)

# login
route('/login', mod.login.login, methods=BOTH)

# image ajax calls
route('/_addimgs/<int:objId>',      mod.img._addObjImgs, methods=POST)
route('/_imgs/<int:objId>',         mod.img._objImgs)
route('/_orderimgs/<int:objId>',    mod.img._orderObjImgs, methods=POST)
route('/_rmimg',                    mod.img._rmObjImg, methods=POST)
route('/_unusedimgs',               mod.img._unusedImgs)


if __name__ == '__main__':
    preStart()
    app.run(host="localhost", port=8001, debug=True)