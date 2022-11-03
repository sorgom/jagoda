from PIL import Image, ExifTags, TiffImagePlugin
from shutil import copyfile
from os import path, makedirs
from glob import glob

SOURCE_FILE_KEY = 41728

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'tif', 'tiff'}
FOLDER_BASE  = 'static/img/'
FOLDER_MINI  = path.join(FOLDER_BASE, 'mini')
FOLDER_FULL  = path.join(FOLDER_BASE, 'full')
FOLDER_ORIG  = path.join(FOLDER_BASE, 'orig')

# TODO: make configureable
SIZE_MINI = 160, 120
SIZE_FULL = 800, 600
QUALY_MINI = 80
QUALY_FULL = 80
EXT_OUT = 'jpg'

def _imgName(id:int, ext:str=EXT_OUT):
    return "%06d.%s" % (id, ext)

def _pathMini(id:int):
    return path.join(FOLDER_MINI, _imgName(id))

def _pathFull(id:int):
    return path.join(FOLDER_FULL, _imgName(id))

def _pathSaveOrig(id:int, ext:str):
    return path.join(FOLDER_ORIG, _imgName(id, ext))  

def _ext(filename:str):
    return filename.rsplit('.', 1)[1] if '.' in filename else None

def _allowedImgExt(ext:str):
    return ext.lower() in ALLOWED_EXTENSIONS

def _corrExif(val):
    if isinstance(val, TiffImagePlugin.IFDRational):
        return float(val)
    if type(val) == str:
        return val.strip() 
    return val
    
def _getExif(img, srcFileName:str):
    exif = img.getexif()
    if exif:
        print('exif:', type(exif))
        for k, v in exif.items():
            v = _corrExif(v)
            if not v:
                del exif[k]
            else: 
                exif[k] = v
    else:
        exif = Image.Exif()
    exif[SOURCE_FILE_KEY] = srcFileName
    return exif

def _saveImg(img, fpath, size, quality, exif):
    img.thumbnail(size, resample=Image.Resampling.BICUBIC, reducing_gap=2.0)
    img.save(fpath, quality=quality, exif=exif)

def saveImg(file, id) -> str:
    ext = _ext(file.filename)
    if ext and _allowedImgExt(ext):
        with Image.open(file) as img1:
            print('processing: ', file.filename)
            print(dir(file))
            file.save(_pathSaveOrig(id, ext))
            exif = _getExif(img1, file.filename)
            img2 = img1.copy()
            _saveImg(img1, _pathFull(id), SIZE_FULL, QUALY_FULL, exif)
            _saveImg(img2, _pathMini(id), SIZE_MINI, QUALY_MINI, exif)
            return True
    return False

def _allImg(folder):
    return glob(path.join(folder, f'*.{EXT_OUT}'))

def allImgMini():
    return _allImg(FOLDER_MINI)

def allImgFull():
    return _allImg(FOLDER_FULL)

def getImgMini(id:int):
    fp = _pathMini(id)
    return fp if path.exists(fp) else None

def getImgFull(id:int):
    fp = _pathFull(id)
    return fp if path.exists(fp) else None

def checkImgFolders():
    for folder in [FOLDER_MINI, FOLDER_FULL, FOLDER_ORIG]:
        if not path.exists(folder):
            makedirs(folder)