#   encapsulation of google translator

from googletrans import Translator

GOOGLE_TRANSLATOR = None;

def getTr():
    global GOOGLE_TRANSLATOR
    if GOOGLE_TRANSLATOR is None:
        GOOGLE_TRANSLATOR = Translator()
    return GOOGLE_TRANSLATOR

def translate(src:str, dest:str, text:str) -> str:
    res = getTr().translate(text, src=src, dest=dest)
    if res:
        return res.txt
    return ''


