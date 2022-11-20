from flask import render_template
from mod.QRCode64 import QRCode64
from mod.config import WEB_SITE
from mod.base import debug

QRC_INST = None

def qrc():
    global QRC_INST
    if QRC_INST is None:
        QRC_INST = QRCode64(border=0)
    return QRC_INST

def _qrc(id:int, what:str='object'):
    url = '/'.join([WEB_SITE, what, str(id)])
    debug('url:', url)
    b64 = qrc().ascii(url)
    return render_template('_qrcode.htm', id=id, url=url, b64=b64, what=what)    


