import json
import os
import shutil
import sys


json_fpath = sys.argv[1]
prefix = sys.argv[2]
output_dir = sys.argv[3]

with open(json_fpath) as annot_json_file:
    annot_json = json.load(annot_json_file)

filepaths = [image['file_name'] for image in annot_json['images']]

for filepath in filepaths:
    full_fpath = os.path.join(prefix, filepath)
    output_fpath = os.path.join(output_dir, filepath)
    shutil.copyfile(full_fpath, output_fpath)
