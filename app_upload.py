from flask import Flask, flash, request, redirect, url_for, render_template

from mod.saveImg import saveImg, checkImgFolders

# This doesn't work
# counter is 0 with every application restart
IMAGE_NUM = 0

app = Flask(__name__, template_folder='templates')

def preStart():
    checkImgFolders()

def nextID():
    # see init of IMAGE_NUM
    global IMAGE_NUM
    IMAGE_NUM += 1
    return IMAGE_NUM


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('images')
        # return '<br>'.join(file.filename for file in files)
        for file in files:
            saveImg(file, nextID()) 
        return redirect('/')
    return render_template('upload.htm')

if __name__ == '__main__':
    preStart()
    app.run(host="localhost", port=8001, debug=True)