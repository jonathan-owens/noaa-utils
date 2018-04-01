import json
import os
import sys

json_fp = sys.argv[1]
imagery_dir = sys.argv[2]
output_json = sys.argv[3]

with open(json_fp) as f:
    annot_json = json.load(f)

num_missing_files = 0
for image_file_name in annot_json['images']:
    image_fp = os.path.join(imagery_dir, image_file_name['file_name'])
    if not os.path.exists(image_fp):
        # annot_json['images'].remove(image_file_name)
        annot_json['images'][:] = [x for x in annot_json['images'] if x != image_file_name]
        num_missing_files += 1

with open(output_json, 'w') as f:
    json.dump(annot_json, f, indent=4)

print("Removed %s images" % num_missing_files)
