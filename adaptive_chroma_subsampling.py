from code.parser import *
from code.images import *
from code.subsampler import *


paths, ratios, average, show = parser()
images = Images(paths)

print("Average sampling:", average)

for image in images.images:
    image.image = image_crop_16(image.image)
    image.size = image.image.shape
    image.width = image.size[0]
    image.height = image.size[1]

    name = image.path.split("\\")[-1]
    print(name)

    if show:
        image_show(image.image, "{} original".format(name))

    adaptive_chroma_subsampling(image, ratios, average=average)

    if show:
        image_show(image.subsampled, "{} {}".format(name, image.text))
        wait()
