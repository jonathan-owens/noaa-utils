import json
import os
import sys


def add_images_in_dir_to_json(json_fpath, image_dir):
    """
    Traverses the directory of images and adds them to the JSON image block
    if they are not already in it.

    :param json_fpath: The filepath of the JSON to update
    :type json_fpath: str

    :param image_dir: The directory of images to traverse
    :type image_dir: str

    :return:
    """
    n_images_added = 0
    # Build the list of full image filepaths
    image_fpaths = [f for f in os.listdir(image_dir) if os.path.isfile(
        os.path.join(image_dir, f))]

    # Load the annotation JSON
    with open(json_fpath) as json_file:
        annot_json = json.load(json_file)

    image_filenames = [image['file_name'] for image in annot_json['images']]

    for image_fpath in image_fpaths:
        image_fname = os.path.split(image_fpath)[1]
        if image_fname not in image_filenames:
            annot_json['images'].append({
                'id': len(annot_json['images']) + 1,
                'file_name': image_fname
            })
            n_images_added += 1

    # Output the new annotation JSON
    with open(json_fpath, 'w') as json_file:
        json.dump(annot_json, json_file, indent=4)

    print('[[ INFO ]] Added %s new images' % n_images_added)


def main():
    json_fpath = sys.argv[1]
    image_dir = sys.argv[2]

    add_images_in_dir_to_json(json_fpath, image_dir)


if __name__ == '__main__':
    main()
