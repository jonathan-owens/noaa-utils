import sys

from coco_wrangler.coco_api import CocoDataset

json_fpath = sys.argv[1]

d = CocoDataset(json_fpath, autobuild=False)
# noinspection PyProtectedMember
d._run_fixes()
# noinspection PyProtectedMember
d._build_index()
