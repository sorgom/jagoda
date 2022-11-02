from PIL import Image, ExifTags, TiffImagePlugin
from shutil import copyfile
from os import path, makedirs
from glob import glob

SOURCE_FILE_KEY = 41728

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'tif', 'tiff'}
FOLDER_MINI  = 'static/img/mini'
FOLDER_FULL  = 'static/img/full'
FOLDER_ORIG  = 'static/img/orig'
FOLDER_UPLOAD = 'static/img/upload'

# TODO: make configureable
SIZE_MINI = 160, 120
SIZE_FULL = 800, 600
QUALY_MINI = 80
QUALY_FULL = 80
EXT_OUT = 'jpg'

def _imgName(id:int, ext:str=EXT_OUT):
    return "%06d.%s" % (id, ext)

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
        for k, v in exif.items():
            v = _corrExif(v)
            if not v:
                del exif[k]
            else: 
                exif[k] = v
        exif[SOURCE_FILE_KEY] = srcFileName
        return exif
    return None

def _saveImg(img, folder, name, size, quality=80, exif=None):
    img2 = img.copy()
    img2.thumbnail(size, resample=Image.Resampling.BICUBIC, reducing_gap=2.0)
    if exif:
        print('exif', type(exif))
        img2.save(path.join(folder, name), quality=quality, exif=exif)
    else:
        img2.save(path.join(folder, name), quality=quality)

def saveImg(file, id):
    ext = _ext(file.filename)
    if ext and _allowedImgExt(ext):
        with Image.open(file) as img:
            print('processing: ', file.filename)
            print(dir(file))
            # img.save(path.join(FOLDER_ORIG, _imgName(id, ext)))
            file.save(path.join(FOLDER_ORIG, _imgName(id, ext)))
            name = _imgName(id)
            exif = _getExif(img, file.filename)
            _saveImg(img, FOLDER_FULL, name, SIZE_FULL, QUALY_FULL, exif)
            _saveImg(img, FOLDER_MINI, name, SIZE_MINI, QUALY_MINI)

def _allJpg(folder):
    return glob(path.join(folder, f'*.{EXT_OUT}'))

def allImgMini():
    return _allJpg(FOLDER_MINI)

def allImgFull():
    return _allJpg(FOLDER_FULL)

def checkImgFolders():
    for folder in [FOLDER_MINI, FOLDER_FULL, FOLDER_ORIG, FOLDER_UPLOAD]:
        if not path.exists(folder):
            makedirs(folder)