import sys

from coco_wrangler.coco_api import CocoDataset


input_json_fpath = sys.argv[1]
image_dir = sys.argv[2]
if len(sys.argv) == 4:
    output_json_fpath = sys.argv[3]
else:
    print('[[ WARNING ]] Overwriting the input JSON file. Are you sure?')
    overwrite = input('y/n:').strip().lower()
    if overwrite == 'y':
        output_json_fpath = input_json_fpath
    else:
        print('[[ WARNING ]] Aborting operation.')
        sys.exit()

d = CocoDataset(input_json_fpath, autobuild=False)
# noinspection PyProtectedMember
d._run_fixes()
# noinspection PyProtectedMember
d._build_index()
d.img_root = image_dir
# noinspection PyProtectedMember
d._ensure_imgsize()

d.dump(output_json_fpath)
