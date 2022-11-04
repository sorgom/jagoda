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


@app.route('/upload/<int:id>', methods=['GET', 'POST'])
def upload_file(id:int):
    if request.method == 'POST':
        print('AJAX POST')
        res = []
        files = request.files.getlist('files')
        for file in files:
            print(file.filename)
            if validImageName(file.filename):
                imgId = mydb.getNextImgId()
                print('imgId:', imgId)
                if saveImg(file, imgId):
                    res.append(getImgMini(imgId))

        ret = json.dumps(res)
        print('ret:', ret)
        return ret
    return render_template('ajax_upload.htm')

if __name__ == '__main__':
    preStart()
    app.run(host="localhost", port=8001, debug=True)