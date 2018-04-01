# This utility will read in a list of filepaths pointing to MSCOCO-compliant
# JSON files. It will consume the names in the "categories" section for each
# of those files, and produce a histogram of the frequency of each of these
# category strings.
import json
import sys

import numpy as np
import pylab as pl


if len(sys.argv) < 3:
    print("Usage: python visualize-annotation-strings.py input_json_list.txt "
          "output_hist.dat")

json_filepaths = []
with open(sys.argv[1]) as input_json_list_file:
    for line in input_json_list_file:
        # Ignore empty lines
        if line.strip():
            json_filepaths.append(line.strip())

category_name_to_frequency = {}

for json_filepath in json_filepaths:
    category_id_to_name = {}
    with open(json_filepath) as f:
        all_json = json.load(f)
        categories = all_json['categories']
        annotations = all_json['annotations']

    for category in categories:
        category_id_to_name[category['id']] = category['name'].lower()

    # Build up the frequency to name correspondence using the category to ID
    # hash map
    for annotation_dict in annotations:
        category_name = category_id_to_name[annotation_dict['roi_category']]
        try:
            category_name_to_frequency[category_name] += 1
        except KeyError:
            category_name_to_frequency[category_name] = 1

# Plot the histogram
x = np.arange(len(category_name_to_frequency))
pl.bar(x, category_name_to_frequency.values(), align='center', width=0.5)
pl.xticks(x, category_name_to_frequency.keys(), rotation=90, stretch='expanded')
pl.xticks()
ymax = max(category_name_to_frequency.values()) + 1
pl.ylim(0, ymax)

pl.show()

with open(sys.argv[2], 'w') as output_dat:
    for category_name, category_frequency in category_name_to_frequency.items():
        output_dat.write('%s, %s\n' % (category_name, category_frequency))

print('#################### Summary ############################')
print('Number of x-ticks: %d' % len(x))
