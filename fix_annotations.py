import json


file_to_fix = ''
file_with_all_annots = ''


with open(file_to_fix) as f:
    annots_to_fix = json.load(f)

with open(file_with_all_annots) as f:
    all_annots = json.load(f)

images_to_get_annots = annots_to_fix['images']

for annot in all_annots['annotations']:
    if
