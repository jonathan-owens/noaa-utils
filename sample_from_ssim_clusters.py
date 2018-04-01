import json
import os
import random
import shutil


input_clusters_fp = '/Users/jowens/projects/noaa/data/AFSC_dropcam_images/' \
                    'clusters.txt'
img_dir = '/Users/jowens/projects/noaa/data/AFSC_dropcam_images'
sequestered_clusters_fp = \
    '/Users/jowens/projects/noaa/data/AFSC_dropcam_images' \
    '/sequestered_clusters.txt'
mscoco_annot_fp = '/Users/jowens/projects/noaa/data/AFSC_dropcam_images' \
                  '/target_data.mscoco.json'
sampled_output_json_fp = \
    '/Users/jowens/projects/noaa/data/AFSC_dropcam_images' \
    '/afsc_seq0/afsc_seq0.mscoco.json'
sampled_images_dir = '/Users/jowens/projects/noaa/data/AFSC_dropcam_images' \
                     '/afsc_seq0'

image_sampling_percent = 0.1
cluster_sequestering_percent = 0.05

# Read in the annotations
with open(mscoco_annot_fp) as mscoco_annot_file:
    mscoco_annot_json = json.load(mscoco_annot_file)

images = mscoco_annot_json['images']
n_images = len(images)
annotations = mscoco_annot_json['annotations']

# Initialize the known values of the sampled images
sampled_images_json = {
    'categories': mscoco_annot_json['categories'],
    'licenses': mscoco_annot_json['licenses'],
    'info': mscoco_annot_json['info'],
    'images': [],
    'annotations': []
}

# List contains the files which delineate the clusters. Each entry is the
# start of a new cluster.
cluster_files = []
with open(input_clusters_fp, 'r') as cluster_input_file:
    for line in cluster_input_file:
        if not line.strip():
            continue
        cluster_files.append(line.strip())

# Sequester random clusters.
n_sequestered_clusters = int(len(cluster_files) * cluster_sequestering_percent)
sequestered_clusters = random.sample(cluster_files, n_sequestered_clusters)

# Write which clusters have been sequestered
with open(sequestered_clusters_fp, 'w') as f:
    for sequestered_cluster in sequestered_clusters:
        f.write(sequestered_cluster + '\n')

# Identify the non-sequestered clusters.
print("[[ INFO ]] Identifying non-sequestered clusters...")
non_sequestered_clusters = sorted(list(set(cluster_files) - set(
    sequestered_clusters)))

# Figure out how many images we need to sample to get the specified percentage
n_images_to_sample = int(image_sampling_percent * n_images)
# Ensures that there are enough images remaining after the sequestration of
# clusters to sample the required number.
assert(n_images_to_sample < len(non_sequestered_clusters))

# Pick the clusters from which we will sample
sampled_clusters = sorted(random.sample(non_sequestered_clusters,
                          int(n_images_to_sample)))

# And sample the images from the clusters
img_numbers = []
sampled_img_numbers = []
for sampled_cluster in sampled_clusters:
    _, img_number = os.path.split(sampled_cluster)
    img_number = img_number.strip('.jpg')
    img_numbers.append(int(img_number))

for idx in range(1, len(img_numbers)):
    # Just take the sole image in that cluster if there is only one
    if abs(img_numbers[idx] - img_numbers[idx - 1]) == 1:
        sampled_img_numbers.append(img_numbers[idx - 1])
    else:
        sampled_img_numbers.append(random.sample(range(img_numbers[idx - 1],
                                                 img_numbers[idx]), 1)[0])

# Add the sampled images JSON to the return object
sampled_img_fps = []
for sampled_img_number in sampled_img_numbers:
    sampled_img_filename = str(sampled_img_number).zfill(6) + '.jpg'
    sampled_img_fp = os.path.join(img_dir, sampled_img_filename)
    sampled_img_fps.append(sampled_img_fp)

    for image in images:
        if sampled_img_filename == image['file_name']:
            sampled_images_json['images'].append(image)

# Pick out the relevant annotations for these sampled images
for sampled_image in sampled_images_json['images']:
    for annotation in annotations:
        if annotation['image_id'] == sampled_image['id']:
            sampled_images_json['annotations'].append(annotation)

try:
    os.mkdir(sampled_images_dir)
except OSError:
    print('[[ WARNING ]] Directory %s already exists, overwriting.')
    shutil.rmtree(sampled_images_dir)
    os.makedirs(sampled_images_dir)
with open(sampled_output_json_fp, 'w') as sampled_output_json_file:
    json.dump(sampled_images_json, sampled_output_json_file, indent=4)

# Write copies of the sampled images to the specified location

for sampled_image_fp in sampled_img_fps:
    shutil.copy(sampled_image_fp, sampled_images_dir)
