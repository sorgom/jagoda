from PIL import Image, ExifTags, TiffImagePlugin
from os import path, makedirs
import json
from glob import glob
from mod.MyDB import db
from mod.base import *
from mod.utilz import debug

# TODO: make part of config
MAX_NUM_IMGES = 8

SOURCE_FILE_KEY = 41728

FOLDER_BASE  = 'static/img/'
FOLDER_MINI  = path.join(FOLDER_BASE, 'mini')
FOLDER_FULL  = path.join(FOLDER_BASE, 'full')
FOLDER_EXIF  = path.join(FOLDER_BASE, 'exif')

# TODO: make configureable
SIZE_MINI = 160, 120
SIZE_FULL = 800, 600
QUALY_MINI = 80
QUALY_FULL = 80
EXT_OUT  = 'jpg'
EXT_EXIF = 'json'

def _fName(id:int, ext:str=EXT_OUT):
    return "%07d.%s" % (id, ext)

def _pathMini(id:int):
    return path.join(FOLDER_MINI, _fName(id))

def _pathFull(id:int):
    return path.join(FOLDER_FULL, _fName(id))

def _pathExif(id:int):
    return path.join(FOLDER_EXIF, _fName(id, EXT_EXIF))

def _corrExif(val):
    if isinstance(val, TiffImagePlugin.IFDRational):
        return float(val)
    if type(val) == str:
        val = val.strip()
        return val if val else None 
    return val
    
def _getExif(img, srcFileName:str):
    res = {}
    exif = img.getexif()
    if exif:
        for k, v in exif.items():
            v = _corrExif(v)
            if v is not None:
                res[k] = v
    res[SOURCE_FILE_KEY] = srcFileName
    return [[k, v] for k, v in res.items()]

def _saveImg(img, fpath, size, quality):
    img.thumbnail(size, resample=Image.Resampling.BICUBIC, reducing_gap=2.0)
    img.save(fpath, quality=quality)

def getAcceptImgTypes():
    return 'image/jpeg'

def saveImg(file, objId=None):
    with Image.open(file) as img1:
        id = db().getNextId()
        exif = _getExif(img1, file.filename)
        with open(_pathExif(id), 'w') as fh:
            json.dump(exif, fh)
        img2 = img1.copy()
        _saveImg(img1, _pathFull(id), SIZE_FULL, QUALY_FULL)
        _saveImg(img2, _pathMini(id), SIZE_MINI, QUALY_MINI)
        if objId is None:
            db().addImg(id)
        else:
            db().addObjectImg(objId, id)
        return id

# def _allImg(folder):
#     return glob(path.join(folder, f'*.{EXT_OUT}'))

# def allImgMini():
#     return _allImg(FOLDER_MINI)

# def allImgFull():
#     return _allImg(FOLDER_FULL)

def getImgMini(id:int):
    fp = _pathMini(id)
    return fp if path.exists(fp) else None

def getImgFull(id:int):
    fp = _pathFull(id)
    return fp if path.exists(fp) else None

def getExif(id:int):
    fp = _pathExif(id)
    if not path.exists(fp): return None
    with open(fp, 'r') as fh:
        data = json.load(fh)
        out = [
            [l, v] for l, v in [ [ExifTags.TAGS.get(k), v] for k, v in data]
            if l is not None
        ]
        return out

def checkImgFolders():
    for folder in [FOLDER_MINI, FOLDER_FULL, FOLDER_EXIF]:
        if not path.exists(folder):
            makedirs(folder)