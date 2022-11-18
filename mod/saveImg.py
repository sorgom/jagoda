from PIL import Image, TiffImagePlugin #, ExifTags
from os import path, makedirs
import json
from mod.MyDB import db
from mod.base import *
from mod.config import *

SOURCE_FILE_KEY = 41728
ORIENTATION_KEY = 274
ROTATIONS = { 3: 180, 6: 270, 8: 90 }

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
        checkImgFolders()
        id = db().getNextId()
        fileMini, fileFull, fileExif = db().getImgFiles(id)
        debug('files:', fileMini, fileFull, fileExif)
        data = _getExif(img, file.filename)
        with open(fileExif, 'w') as fh:
            json.dump(data, fh)
        rot = ROTATIONS.get(data.get(ORIENTATION_KEY, 0))
        if rot:
            debug('rotate:', rot)
            img = img.rotate(rot, expand=True)
        _saveImg(img, fileMini, IMG_SIZE_MINI, IMG_QUALITY_MINI)
        _saveImg(img, fileFull, IMG_SIZE_FULL, IMG_QUALITY_FULL)
        if objId is None:
            db().addImg(id)
        else:
            db().addObjectImg(objId, id)
        return id

def checkImgFolders():
    for folder in db().getImgFolders():
        if not path.exists(folder):
            makedirs(folder)    

def getExif(id:int):
    debug('getExif')
    fp = db().getImgFileExif(id)
    debug('fp', fp)
    if not path.exists(fp): return None
    with open(fp, 'r') as fh:
        data = json.load(fh)
        out = [
            [l, v] for l, v in [[l, data.get(k)] for l, k in RELEVANT_EXIF_TAGS]     
            if v is not None
        ]
        out.insert(0, ['Image ID', id])
        return out

