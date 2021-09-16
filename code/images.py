import cv2

from nptyping import NDArray


class Images:

    def __init__(self, paths: list[str]):
        self.images = []
        for path in paths:
            self.images.append(Image(path))
        self.list_size = len(self.images)

    def print(self):
        print("list size:", len(self.images))
        for index, image in enumerate(self.images):
            print("image", index)
            image.print()


class Image:

    def __init__(self, path: str):
        self.path = path
        self.image = image_load(self.path)
        self.image = image_crop(self.image)

        self.size = self.image.shape
        self.width = self.size[0]
        self.height = self.size[1]

        self.subsampled = None
        self.bpp = 24
        self.ssim = 0
        self.pnsr = 0
        self.mse = 0

    def print(self):
        print("path:", self.path)
        print("size: {}x{}".format(self.width, self.height))


def image_load(path: str) -> NDArray:
    return cv2.imread(path)


def image_crop(image: NDArray) -> NDArray:
    size_x = image.shape[0]
    size_y = image.shape[1]
    size_x = size_x - (size_x % 4)
    size_y = size_y - (size_y % 2)
    return image[0:size_y, 0:size_x, :]


def image_crop_16(image: NDArray) -> NDArray:
    size_x = image.shape[0]
    size_y = image.shape[1]
    size_x = size_x - (size_x % 16)
    size_y = size_y - (size_y % 16)
    return image[0:size_y, 0:size_x, :]


def image_show(image: NDArray, name: str):
    cv2.imshow(name, image)


def wait():
    cv2.waitKey(0)
