from flask import Flask, request, redirect, url_for, render_template
from PIL import Image
import qrcode
import base64
import binascii
import io

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('aut_index.htm')


@app.route('/qr/<int:id>')
def qr(id):
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=2,
    )
    qr.add_data(f'https://jagoda.org/item/{id}')
    # qr.add_data(f'http://sorgo.de')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    bios = io.BytesIO()
    img.save(bios, format='PNG')
    c64 = base64.b64encode(bios.getvalue()).decode('ascii')
    return render_template('aut_qrcode.htm', id=id, b64=c64)

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=False)
