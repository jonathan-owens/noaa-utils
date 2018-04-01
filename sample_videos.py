import json
import os
import shutil
import sys

from sample_random_images import sample_random_images

sample_percent = 0.10

with open(sys.argv[1]) as input_video_img_seq_file:
    for line in input_video_img_seq_file:
        # Ignore empty lines
        if line.strip():
            images_dir, annot_fp, output_json = line.strip().split(' ')
            output_dir = os.path.join(images_dir, 'sampled_images')
            try:
                os.makedirs(output_dir)
            except OSError:
                # We want a clean start, so if the output images directory
                # already exists, we delete it
                shutil.rmtree(output_dir)
                os.makedirs(output_dir)

            with open(annot_fp) as f:
                mscoco_annot_json = json.load(f)

            sampled_images_json, sampled_image_fps = sample_random_images(
                mscoco_annot_json, sample_percent)
            with open(output_json, 'w') as f:
                json.dump(sampled_images_json, f, indent=4)

            for sampled_image_fp in sampled_image_fps:

                output_fp = os.path.join(output_dir, sampled_image_fp)
                original_fp = os.path.join(images_dir, sampled_image_fp)
                shutil.copy(original_fp, output_fp)
