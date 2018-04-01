import json
import sys


def validate_annotations(json_to_validate):
    """
    Ensures that all annotations in ``json_to_validate`` are valid,
    which consists of checking:

    1. That each annotation category is in ``json_to_validate['categories']``
    2. That each image ID in the annotations is in
       ``json_to_validate['images']``
    3. That there are no duplicate annotation IDs in
       ``json_to_validate['annotations']``

    :param json_to_validate: MSCOCO-compliant JSON to validate
    :type json_to_validate: dict

    :return: A list of the invalid annotation IDs, or [] if everything is valid.
    :rtype: [int]
    """
    annotations = json_to_validate['annotations']
    images = json_to_validate['images']
    image_ids = [image['id'] for image in images]
    categories = json_to_validate['categories']
    category_ids = [category['id'] for category in categories]

    invalid_annotation_ids = []
    for annotation in annotations:
        if annotation['image_id'] not in image_ids:
            invalid_annotation_ids.append(annotation['id'])
            print(' [[ ERROR ]] Annotation with ID %s corresponds to an '
                  'invalid image with ID %s.' % (annotation['id'],
                                                 annotation['image_id']))
        elif annotation['category_id'] not in category_ids:
            invalid_annotation_ids.append(annotation['id'])
            print(' [[ ERROR ]] Annotation with ID %s corresponds to an '
                  'invalid annotation category with ID %s.'
                  % (annotation['id'], annotation['category_id']))

    return invalid_annotation_ids


def main():
    json_fpath_to_validate = sys.argv[1]

    with open(json_fpath_to_validate) as json_file_to_validate:
        json_to_validate = json.load(json_file_to_validate)

    invalid_annotations = validate_annotations(json_to_validate)

    if not invalid_annotations:
        print('JSON file %s validated and no errors found!'
              % json_fpath_to_validate)


if __name__ == '__main__':
    main()
