from flask import Flask, render_template
from mod.QRCode64 import QRCode64

app = Flask(__name__, template_folder='templates')

QRC = QRCode64()
SITE = 'https://jagoda.org'

@app.route('/')
def index():
    return render_template('aut_base.htm')


@app.route('/qr/<int:id>')
def qr(id):
    url = f'{SITE}/item/{id}'
    return render_template('aut_qrcode.htm', id=id, b64=QRC.ascii(url))

if __name__ == '__main__':
    app.run(host="localhost", port=8001, debug=False)
