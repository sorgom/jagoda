from PIL import ExifTags

res = {
    l:k for k, l in ExifTags.TAGS.items()
}



print('RELEVANT_EXIF_TAGS = [')
for l in sorted(res.keys()):
    print(f"    ['{l}', {res[l]}],")
print(']')
