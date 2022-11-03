from flask import Flask, request, redirect, render_template

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

@app.route('/')
def index():
    return render_template('ajax_upload.htm', id=332332)


@app.route('/upload/<int:id>', methods=['GET', 'POST'])
def upload_file(id:int):
    if request.method == 'POST':
        print('AJAX POST')
        files = request.files.getlist('files')
        for file in files:
            print(file.filename)
            #  saveImg(file, nextID()) 
        return redirect('/')
    return render_template('ajax_upload.htm')

if __name__ == '__main__':
    preStart()
    app.run(host="localhost", port=8001, debug=True)