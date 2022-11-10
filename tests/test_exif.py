from statistics import quantiles
from PIL import Image, ExifTags, TiffImagePlugin
from os import path
import json
import re

SOURCE_FILE_KEY = 41728

for k, l in ExifTags.TAGS.items():
    print(l, k)

# print(type(ExifTags.TAGS))

# def grep(pattern, names):
#     expr = re.compile(pattern, re.I)
#     return [elem for elem in names if expr.match(elem)]

# # print(ExifTags.TAGS.values())

# # print(grep('file|name|original', ExifTags.TAGS.values()))

# rev = { n:k for k, n in ExifTags.TAGS.items() }
# res = grep('file|name|original|source', ExifTags.TAGS.values())

# lst = [ [r, rev[r]] for r in res ]

# print(lst)

# exit()

# ['FileSource', 41728]

# print(type(ExifTags.TAGS))
# print(ExifTags.TAGS.keys())

# src = 'img/orig/IMG_7680.JPG'

src = "/mnt/k/photo/inbox/174___10/IMG_7677.JPG"

# src = 'img/orig/IMG_20220320_052252925.JPG'
tdir = 'static/img/test'
size = 1000, 1000
qualities = range(10,101,10)

rxJson = re.compile('"(\d+)"')

def corr(val):
    # type error object of type ifdrational is not json serializable
    if isinstance(val, TiffImagePlugin.IFDRational):
        return float(val)
    if type(val) == str:
        return val.strip() 
    return val

with Image.open(src) as img:
    print('## TYPE:', type(img))
    exif = img.getexif()
    if exif:
        out = {
            # ExifTags.TAGS[k]: v
            k: v
            # int(k): float(v) if isinstance(v, TiffImagePlugin.IFDRational) else v
            for k, v in exif.items()
            if v and k in ExifTags.TAGS
        }

        print(f'before: {len(exif)}')
        print(exif)

        for k, v in exif.items():
            v = corr(v)
            if not v:
                del exif[k]
            else: 
                exif[k] = v

        exif[SOURCE_FILE_KEY] = path.basename(src)

        print(f'after : {len(exif)}')
        print(exif)

        data = [
            [l, v] for l, v in 
            [ [ExifTags.TAGS.get(k, 'NN'), v] for  k, v in exif.items() ]
        ]
        for l, v in data:
            print(l, ':', v)

    # print(out)
        # js = json.dumps(out)

        # # js = rxJson.sub(r'\1', js)

        # print(js)

        # y = json.loads(js)
        # print(y)

        # trans = [ ExifTags.TAGS[int(k)] for k in y.keys() ]

        # print(trans)

        # for key, val in exif.items():
        #     label = ExifTags.TAGS.get(key)
        #     print('key', type(key))
        #     print('val', type(val), val)
        #     print(type(label))
        #     if val and label:
        #         out[label] = val
        #         # print(f'{ExifTags.TAGS[key]}:{val}')

        # print('out', type(out))

        # js = json.dumps(out)


    img.thumbnail(size, resample=Image.Resampling.BICUBIC, reducing_gap=2.0)
    for q in qualities:
#        img.save(os.path.join(tdir, "test_quality_%03d.jpg" % q), quality=q)
        img.save(path.join(tdir, "test_quality_%03d.jpg" % q), quality=q, exif=exif)
    
