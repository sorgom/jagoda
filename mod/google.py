#   encapsulation of google translator

from googletrans import Translator
from mod.base import debug

GOOGLE_TRANSLATOR = None;

def getTr():
    global GOOGLE_TRANSLATOR
    if GOOGLE_TRANSLATOR is None:
        GOOGLE_TRANSLATOR = Translator()
    return GOOGLE_TRANSLATOR

def translate(src:str, dest:str, text:str) -> str:
    debug(src, dest, text)
    res = getTr().translate(text, src=src, dest=dest)
    debug('done')
    if res:
        return res.text
    return ''


