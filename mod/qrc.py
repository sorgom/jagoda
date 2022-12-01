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

def _renderQrc(template:str, id:int, what:str):
    url = '/'.join([WEB_SITE, what, str(id)])
    b64 = qrc().ascii(url)
    return render_template(template, id=id, what=what, url=url, b64=b64)

def _qrc_view(id:int, what:str='art'):
    return _renderQrc('popup_qrcode_view.jade', id, what)

def _qrc_print(id:int, what:str='art'):
    return _renderQrc('popup_qrcode_print.jade', id, what)
