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

mydb = MyDB(app)

def preStart():
    checkImgFolders()

@app.route('/')
def index():
    return render_template('ajax_upload.htm', id=4711)

@app.route('/_imgs/<int:id>')
def _objImgs(id:int):
    res = []
    imgs = mydb.getObjectImgs(id)
    for img in imgs:
        src = getImgMini(img['id'])
        if src:
            img['src'] = src
            res.append(img)
    ret = json.dumps(res)
    print('ret:', ret)
    return ret

@app.route('/_addimgs/<int:id>', methods=['POST'])
def _addImgs(id:int):
    print('_addimgs')
    res = []
    files = request.files.getlist('files')
    for file in files:
        print(file.filename)
        if validImageName(file.filename):
            imgId = mydb.getNextImgId()
            src = saveImg(file, imgId)
            if src:
                mydb.addObjectImg(id, imgId)
                res.append({ 'id': imgId, 'src':src })
    ret = json.dumps(res)
    print('ret:', ret)
    return ret

@app.route('/_orderimgs/<int:id>', methods=['POST'])
def _orderImgs(id:int):
    print('_orderImgs', id)
    for imgId, ord in json.loads(request.form.get('json')):
        print(id, imgId, ord)
        mydb.setObjImg(id, imgId, ord)
    return 'done.'


if __name__ == '__main__':
    preStart()
    app.run(host="localhost", port=8001, debug=True)