import json
import os
import sys


image_dir = sys.argv[1]
full_annot_fpath = sys.argv[2]
output_json_fpath = sys.argv[3]

# Get this list of all the image files in the directory
image_fpaths = [f for f in os.listdir(image_dir) if os.path.isfile(
    os.path.join(image_dir, f))]

# Load the annotation JSON
with open(full_annot_fpath) as full_annot_file:
    annot_json = json.load(full_annot_file)

# Build an index from name to file ID
filename_to_image = {}
for image in annot_json['images']:
    filename_to_image[image['file_name']] = image

# Build an index from image_id to annotations
file_id_to_annots = {}
for annotation in annot_json['annotations']:
    if annotation['image_id'] in file_id_to_annots.keys():
        file_id_to_annots[annotation['image_id']].append(annotation)
    else:
        file_id_to_annots[annotation['image_id']] = [annotation]


sampled_json = {
    'images': [],
    'annotations': [],
    'categories': annot_json['categories'],
    'licenses': annot_json['licenses'],
    'info': annot_json['info']
}

# Add these images to the JSON
for image_fpath in image_fpaths:
    sampled_json['images'].append(filename_to_image[image_fpath])

# Get all of the annotations for these images
n_empty_annotations = 0
for idx, image_fpath in enumerate(image_fpaths):
    print(idx)
    try:
        sampled_json['annotations'].extend(
            file_id_to_annots[filename_to_image[image_fpath]['id']])
    except KeyError:
        n_empty_annotations += 1

with open(output_json_fpath, 'w') as output_json_file:
    json.dump(sampled_json, output_json_file, indent=4)

print(n_empty_annotations)
