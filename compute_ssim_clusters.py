# We want to take the directory of images and compare the images in the
# sequence with that of the previous to determine how similar the two are.
# The metric we use for this is the structural similarity index (SSIM).
import glob
import sys

from skimage import io
from skimage.measure import compare_ssim


if len(sys.argv) < 2:
    print("Usage: python sample_random_images.py path_to_images")

similarity_threshold = 0.7
if len(sys.argv) == 3:
    similarity_threshold = float(sys.argv[2])

image_files = glob.glob(sys.argv[1] + "/*.jpg")
image_transition_fps = sys.argv[1] + "/out.txt"

f = open(image_transition_fps, 'w')
image_transitions = []
idx = 1
for i in range(1, len(image_files)):
    im_a = io.imread(image_files[i])
    im_b = io.imread(image_files[i-1])
    try:
        ssim = compare_ssim(im_a, im_b, multichannel=True)
        print("compare_ssim(%s, %s) = %f" % (image_files[i], image_files[
            i-1], ssim))
        if ssim < 0.6:
            image_transitions.append(image_files[i])
            f.write(image_files[i] + "\n")
    except ValueError:
        print("Continuing...")
        continue
