import json
import os
import random
import shutil
import sys


def sample_random_images(mscoco_annot_json, sample_percent):
    sampled_images_json = {}

    images = mscoco_annot_json['images']
    annotations = mscoco_annot_json['annotations']
    # Copy the categories, info, and licenses because they aren't randomly
    # sampled.
    sampled_images_json['categories'] = mscoco_annot_json['categories']
    sampled_images_json['licenses'] = mscoco_annot_json['licenses']
    sampled_images_json['info'] = mscoco_annot_json['info']

    n_images = len(images)
    n_images_to_sample = int(sample_percent * n_images)
    print("Sampling %d of %d images" % (n_images_to_sample, n_images))

    image_id_to_file_name = {}
    for i in images:
        image_id_to_file_name[i['id']] = i['file_name']

    from collections import OrderedDict
    image_id_to_file_name = OrderedDict(sorted(image_id_to_file_name.items()))

    image_ids = [i['file_name'] for i in images]

    rng = random.Random(0)
    sampled_images = rng.sample(images, n_images_to_sample)
    sampled_images_json['images'] = sorted(sampled_images, key=lambda k: k[
        'id'])
    sampled_image_ids = sorted([int(image['id']) for image in sampled_images])
    # noinspection PyShadowingNames

    # Get the relevant annotations for the sampled images.
    sampled_annotations = []
    for annotation in annotations:
        if int(annotation['image_id']) in sampled_image_ids:
            sampled_annotations.append(annotation)
    sampled_images_json['annotations'] = sampled_annotations

    sampled_image_fps = [image['file_name'] for image in sampled_images]
    return sampled_images_json, sampled_image_fps





def main():
    input_json_fp = sys.argv[1]
    percent_to_sample = float(sys.argv[2])
    output_json_fp = sys.argv[3]
    image_copy_dir = sys.argv[4]
    exclude_image = None

    with open(input_json_fp) as json_file_to_sample:
        mscoco_annot = json.load(json_file_to_sample)

    sampled_images_mscoco, sampled_image_fps = sample_random_images(
        mscoco_annot, percent_to_sample)

    with open(output_json_fp, 'w') as output_json:
        json.dump(sampled_images_mscoco, output_json, indent=4)
        print('[[ INFO ]] Wrote sampled JSON to %s.' % output_json_fp)

    # Make a copy of the sampled images
    try:
        os.mkdir(image_copy_dir)
    except OSError:
        overwrite_dir = input('[[ WARNING ]] Directory %s already exists, '
                              'overwrite? [y/n]' % image_copy_dir)
        if overwrite_dir.strip().lower() == 'y':
            print('[[ INFO ]] Emptying directory %s.' % image_copy_dir)
            shutil.rmtree(image_copy_dir)
            os.makedirs(image_copy_dir)
        else:
            print('[[ INFO ]] Not overwriting directory, so images will not '
                  'be copied.')
    # for sampled_image_fp in sampled_image_fps:
    #     shutil.copy(os.path.join(sys.argv[5], sampled_image_fp), sys.argv[4])

    # Copy from aretha
    # for sampled_image_fp in sampled_image_fps:
    #     full_image_fp = os.path.join(image_copy_dir, sampled_image_fp + '.png')
    #     os.system('touch %s' % full_image_fp)
        # os.system('scp jonathan.owens@aretha.kitware.com:/data/dawkins/'
        #           'habcam_data/2015_Habcam_photos/%s.png %s'
        #           % (sampled_image_fp, sys.argv[4]))


if __name__ == '__main__':
    main()
