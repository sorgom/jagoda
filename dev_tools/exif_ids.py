from PIL import ExifTags
import re


def splitInterCaps(val:str) -> str:
    return re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', re.sub(r'([a-z])([A-Z])', r'\1 \2', val))


res = {
    splitInterCaps(l):k for k, l in ExifTags.TAGS.items()
}

print('RELEVANT_EXIF_TAGS = [')
for l in sorted(res.keys()):
    print(f"    ['{l}', '{res[l]}'],")
print(']')
