# ============================================================
# database
# ============================================================
DB_CONFIG = {
  'user': 'aut',
  'password': 'aa',
  'host': '127.0.0.1',
  'database': 'jagoda'
}

# ============================================================
# Imaging
# ============================================================
# maximum number of images per object
MAX_NUM_ENT_IMGS = 8

# image max dimension (px) & quality: full
IMG_SIZE_FULL = 800
IMG_QUALITY_FULL = 80

# mage max dimension (px) & quality: miniature
IMG_SIZE_MINI = 160
IMG_QUALITY_MINI = 80

# accepted image types (input accept)
IMG_TYPE_ACCEPTED = 'image/jpeg'

# exif tags to extract
RELEVANT_EXIF_TAGS = [
    ['Date Time', '306'],
    ['Artist', '315'],
    ['Copyright', '33432'],
    ['File Source', '41728'],
    ['Make', '271'],
    ['Model', '272']
]

# ============================================================
# web site
# ============================================================
WEB_SITE = 'https://jagoda.org'

