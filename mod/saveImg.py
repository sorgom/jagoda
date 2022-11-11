from PIL import Image, ExifTags, TiffImagePlugin
from os import path, makedirs
import json
from glob import glob
from mod.MyDB import db
from mod.base import *
from mod.config import *
from mod.utilz import debug

SOURCE_FILE_KEY = 41728
ORIENTATION_KEY = 274
ROTATIONS = { 3: 180, 6: 270, 8: 90 }

FOLDER_BASE  = 'static/img/'
FOLDER_MINI  = path.join(FOLDER_BASE, 'mini')
FOLDER_FULL  = path.join(FOLDER_BASE, 'full')
FOLDER_EXIF  = path.join(FOLDER_BASE, 'exif')

EXT_OUT  = 'jpg'
EXT_EXIF = 'json'

RELEVANT_EXIF_TAGS = [
    ['Date Time', '306'],
    ['Artist', '315'],
    ['Copyright', '33432'],
    ['File Source', '41728'],
    ['Make', '271'],
    ['Model', '272']
]

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
    data = {}
    exif = img.getexif()
    if exif:
        for k, v in exif.items():
            v = _corrExif(v)
            if v is not None:
                data[k] = v
    data[SOURCE_FILE_KEY] = srcFileName
    return data

def _saveImg(img, fpath, size, quality):
    cpy = img.copy()
    cpy.thumbnail((size, size), resample=Image.Resampling.BICUBIC, reducing_gap=2.0)
    cpy.save(fpath, quality=quality)

def saveImg(file, objId=None):
    with Image.open(file) as img:
        id = db().getNextId()
        data = _getExif(img, file.filename)
        with open(_pathExif(id), 'w') as fh:
            json.dump(data, fh)
        rot = ROTATIONS.get(data.get(ORIENTATION_KEY, 0))
        if rot:
            debug('rotate:', rot)
            img = img.rotate(rot, expand=True)
        _saveImg(img, _pathFull(id), IMG_SIZE_FULL, IMG_QUALITY_FULL)
        _saveImg(img, _pathMini(id), IMG_SIZE_MINI, IMG_QUALITY_MINI)
        if objId is None:
            db().addImg(id)
        else:
            db().addObjectImg(objId, id)
        return id

def getImgMini(id:int):
    fp = _pathMini(id)
    return fp if path.exists(fp) else None

def getImgFull(id:int):
    fp = _pathFull(id)
    return fp if path.exists(fp) else None

def getExif(id:int):
    debug('getExif')
    fp = _pathExif(id)
    if not path.exists(fp): return None
    with open(fp, 'r') as fh:
        data = json.load(fh)
        debug('data', data)
        out = [
            [l, v] for l, v in [[l, data.get(k)] for l, k in RELEVANT_EXIF_TAGS]     
            if v is not None
        ]
        out.insert(0, ['Image ID', id])
        debug('out', out)
        return out

def checkImgFolders():
    for folder in [FOLDER_MINI, FOLDER_FULL, FOLDER_EXIF]:
        if not path.exists(folder):
            makedirs(folder)