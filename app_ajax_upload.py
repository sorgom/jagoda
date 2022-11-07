#!python3

from flask import Flask, request, redirect, render_template
import json

from mod.MyDB import MyDB
from mod.genTemplates import TEMPLATES_FOLDER, genTemplates
from mod.saveImg import checkImgFolders, validImageName, saveImg, getImgMini

app = Flask(__name__, template_folder=TEMPLATES_FOLDER)

# secret string for session cooky
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'aut'
app.config['MYSQL_PASSWORD'] = 'aa'
app.config['MYSQL_DB'] = 'jagoda'

# TODO: make part of config
MAX_NUM_IMGES = 8

mydb = MyDB(app)

def preStart():
    checkImgFolders()

def getJson():
    return json.loads(request.form.get('json'))


def mkJson(data, withMax:bool=False):
    return json.dumps({ 'data':data, 'max':MAX_NUM_IMGES if withMax else 0})

@app.route('/')
def index():
    return render_template('ajax_upload.htm', id=4711)


@app.route('/_imgs/<int:id>')
def _objImgs(id:int):
    print('_objImgs:', id)
    res = []
    imgs = mydb.getObjectImgs(id)
    for img in imgs:
        src = getImgMini(img['id'])
        if src:
            img['src'] = src
            res.append(img)
    ret = mkJson(res, True)
    print('ret:', ret)
    return ret

@app.route('/_addimgs/<int:id>', methods=['POST'])
def _addImgs(id:int):
    print('_addimgs:', id)
    files = request.files.getlist('files')
    for file in files:
        imgId = mydb.getNextImgId()
        src = saveImg(file, imgId)
        if src:
            mydb.addObjectImg(id, imgId)
    return _objImgs(id)

@app.route('/_orderimgs/<int:id>', methods=['POST'])
def _orderImgs(id:int):
    print('_orderImgs', id)
    for imgId, ord in getJson():
        print(id, imgId, ord)
        mydb.setObjectImg(id, imgId, ord)
    return 'done.'

@app.route('/_rmimg', methods=['POST'])
def _rmImg():
    print('_rmImg')
    mydb.rmObjectImg(request.form.get('objId'), request.form.get('imgId'))
    return 'done.'

@app.route('/_unusedimgs')
def _unusedimgs():
    res = []
    imgs = mydb.getUnusedImgs()
    for img in imgs:
        src = getImgMini(img['id'])
        if src:
            img['src'] = src
            res.append(img)
    ret = mkJson(res, False)
    print('ret:', ret)
    return ret


if __name__ == '__main__':
    preStart()
    app.run(host="localhost", port=8001, debug=True)