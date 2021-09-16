from code.parser import *
from code.images import *
from code.subsampler import *

paths, ratios, average, show = parser()
images = Images(paths)

print("Average sampling:", average)

for image in images.images:

    name = image.path.split("\\")[-1]
    print(name)

    if show:
        image_show(image.image, "{} original".format(name))

    for count_ratio, ratio in enumerate(ratios):
        chroma_subsampling(image, ratio, average=average)

        if show:
            image_show(image.subsampled, "{} {}".format(name, image.text))

    if show:
        wait()
