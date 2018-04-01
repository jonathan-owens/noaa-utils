import json
import os
import random


all_clusters_fpath = '/Users/jowens/projects/noaa/data/afsc_dropcam/' \
                     'clusters.txt'
sequestered_clusters_fpath = '/Users/jowens/projects/noaa/data/afsc_dropcam/' \
                             'sequestered_clusters.txt'
phase0_json_fpath = '/Users/jowens/projects/noaa/data/phase-0/' \
                    'phase0-annotations/afsc_seq0.mscoco.json'
full_json_fpath = '/Users/jowens/projects/noaa/data/full-datasets/' \
                  'afsc_full_dataset.mscoco.json'
phase1_json_fpath = '/Users/jowens/projects/noaa/data/phase-1/' \
                    'phase1-annotations/afsc_seq0.mscoco.json'

image_sampling_percent = 0.4

# Each line in this file delineates the start of a new cluster
cluster_files = []
with open(all_clusters_fpath) as f:
    for line in f:
        if not line.strip():
            continue
        cluster_files.append(line.strip())

# Each line in this file delineates the start of a sequestered cluster
sequestered_cluster_files = []
with open(sequestered_clusters_fpath) as f:
    for line in f:
        if not line.strip():
            continue
        sequestered_cluster_files.append(line.strip())

clusters_to_sample_from = sorted(list(set(cluster_files) -
                                      set(sequestered_cluster_files)))

# Read in the images that are already sampled
with open(phase0_json_fpath) as f:
    phase0_json = json.load(f)
sampled_images_nums = [int(os.path.split(image['file_name'])[1].strip('.jpg'))
                       for image in phase0_json['images']]

new_sampled_nums = []

# Go over all the clusters and sample 40% from them
for idx, cluster in enumerate(clusters_to_sample_from):
    # Turn filepath into integer
    file_num = int(os.path.split(cluster)[1].strip('.jpg'))

    if idx == 0:
        prev_file_num = 1
        num_images_in_cluster = file_num - prev_file_num
    else:
        prev_file_num = int(
            os.path.split(clusters_to_sample_from[idx - 1])[1].strip(
                '.jpg'))
        num_images_in_cluster = file_num - prev_file_num

    n_sample_from_cluster = int(num_images_in_cluster * image_sampling_percent)

    # Make a set of all images in this range and subtract the ones that
    already_sampled = set()
    for img_num in sampled_images_nums:
        if img_num < file_num:
            already_sampled.add(img_num)
        # File list is sorted
        else:
            break
    nums_to_sample_from = set(range(prev_file_num, file_num)) - already_sampled

    if n_sample_from_cluster > len(nums_to_sample_from):
        new_sampled_nums.extend(list(nums_to_sample_from))
    else:
        new_sampled_nums.extend(random.sample(nums_to_sample_from,
                                              n_sample_from_cluster))

with open(full_json_fpath) as f:
    full_json = json.load(f)

sampled_json = {
    'categories': full_json['categories'],
    'licenses': full_json['licenses'],
    'info': full_json['info'],
    'images': [],
    'annotations': []
}

image_index = {}
annot_index = {}
# Index mapping the image ID to the image ``dict``.
for image in full_json['images']:
    image_index[image['id']] = image

# Index mapping the image ID to a list of annotation ``dict``s.
for annot in full_json['annotations']:
    try:
        annot_index[annot['image_id']].append(annot)
    except KeyError:
        annot_index[annot['image_id']] = [annot]

for idx in new_sampled_nums:
    sampled_json['images'].append(image_index[idx])

    try:
        sampled_json['annotations'].extend(annot_index[idx])
    except KeyError:
        sampled_json['annotations'] = [annot_index[idx]]

with open(phase1_json_fpath, 'w') as f:
    json.dump(sampled_json, f, indent=4)
