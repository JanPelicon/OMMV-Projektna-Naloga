import numpy as np
import math

from code.conversion import *
from code.images import *
from code.metrics import *

from nptyping import NDArray

RATIOS = ["4:4:2", "4:4:1", "4:4:0", "4:2:2", "4:2:1", "4:2:0", "4:1:1", "4:1:0", "3:1:1"]
ADAPTIVE_THRESHOLD = 6.0

def chroma_subsampling(image: Image, ratio: str, average: bool):

    image.subsampled = np.copy(image.image)

    if ratio not in RATIOS:
        print("Invalid ratio:", ratio)
        return

    image.subsampled = convert_RGB_YCbCr(image.subsampled)

    for py in range(0, image.height, 2):
        for px in range(0, image.width, 4):
            subsample(image.subsampled[py:py+2, px:px+4, :], ratio, average)

    image.subsampled = convert_YCbCr_RGB(image.subsampled)

    image.bpp = bpp(ratio)
    image.mse = mse(image.image, image.subsampled)
    image.psnr = psnr(image.mse)
    image.ssim = ss_ssim(image.image, image.subsampled)
    image.text = "{} bpp={} mse={:0.2f} psnr={:0.2f} ssim={:0.2f}".format(
        ratio,
        image.bpp,
        image.mse,
        image.psnr,
        image.ssim)
    print(image.text)


def adaptive_chroma_subsampling(image: Image, ratios: list[str], average: bool):

    image.subsampled = np.copy(image.image)

    for ratio in ratios:
        if ratio not in RATIOS:
            print("Invalid ratio:", ratio)
            return

    image.subsampled = convert_RGB_YCbCr(image.subsampled)

    ratio_1, ratio_2 = 0, 0
    temp_ratio = ""

    for ry in range(0, image.height, 16):
        for rx in range(0, image.width, 16):

            std = np.std(image.image[ry:ry+16, rx:rx+16, 1:2])

            if std > ADAPTIVE_THRESHOLD:
                ratio_1 += 1
                temp_ratio = ratios[0]
            else:
                ratio_2 += 1
                temp_ratio = ratios[1]

            for py in range(ry, ry+16, 2):
                for px in range(rx, rx+16, 4):
                    subsample(image.subsampled[py:py+2, px:px+4, :], temp_ratio, average)

    image.subsampled = convert_YCbCr_RGB(image.subsampled)

    image.bpp = (ratio_1 * bpp(ratios[0]) + ratio_2 * bpp(ratios[1])) / (ratio_1 + ratio_2)
    image.mse = mse(image.image, image.subsampled)
    image.psnr = psnr(image.mse)
    image.ssim = ss_ssim(image.image, image.subsampled)
    image.text = "{} bpp={:0.2f} mse={:0.2f} psnr={:0.2f} ssim={:0.2f}".format(
        ratios[0]+","+ratios[1],
        image.bpp,
        image.mse,
        image.psnr,
        image.ssim)
    print(image.text)


def subsample(sample: NDArray, ratio: str, average: bool):
    if average:
        subsample_average(sample, ratio)
    else:
        subsample_first_value(sample, ratio)


def subsample_average(sample: NDArray, ratio: str):

    y = sample[:, :, 0]
    cb = sample[:, :, 1]
    cr = sample[:, :, 2]

    if ratio == "4:4:2":
        cb[1, 0:2] = np.uint8((int(cb[1, 0]) + int(cb[1, 1])) // 2)
        cb[1, 2:4] = np.uint8((int(cb[1, 2]) + int(cb[1, 3])) // 2)
        cr[1, 0:2] = np.uint8((int(cr[1, 0]) + int(cr[1, 1])) // 2)
        cr[1, 2:4] = np.uint8((int(cr[1, 2]) + int(cr[1, 3])) // 2)

    elif ratio == "4:4:1":
        cb[1, :] = np.uint8((int(cb[1, 0]) + int(cb[1, 1]) + int(cb[1, 2]) + int(cb[1, 3])) // 4)
        cr[1, :] = np.uint8((int(cr[1, 0]) + int(cr[1, 1]) + int(cr[1, 2]) + int(cr[1, 3])) // 4)

    elif ratio == "4:4:0":
        cb[:, 0] = np.uint8((int(cb[0, 0]) + int(cb[1, 0])) // 2)
        cb[:, 1] = np.uint8((int(cb[0, 1]) + int(cb[1, 1])) // 2)
        cb[:, 2] = np.uint8((int(cb[0, 2]) + int(cb[1, 2])) // 2)
        cb[:, 3] = np.uint8((int(cb[0, 3]) + int(cb[1, 3])) // 2)
        cr[:, 0] = np.uint8((int(cr[0, 0]) + int(cr[1, 0])) // 2)
        cr[:, 1] = np.uint8((int(cr[0, 1]) + int(cr[1, 1])) // 2)
        cr[:, 2] = np.uint8((int(cr[0, 2]) + int(cr[1, 2])) // 2)
        cr[:, 3] = np.uint8((int(cr[0, 3]) + int(cr[1, 3])) // 2)

    elif ratio == "4:2:2":
        cb[0, 0:2] = np.uint8((int(cb[0, 0]) + int(cb[0, 1])) // 2)
        cb[0, 2:4] = np.uint8((int(cb[0, 2]) + int(cb[0, 3])) // 2)
        cb[1, 0:2] = np.uint8((int(cb[1, 0]) + int(cb[1, 1])) // 2)
        cb[1, 2:4] = np.uint8((int(cb[1, 2]) + int(cb[1, 3])) // 2)
        cr[0, 0:2] = np.uint8((int(cr[0, 0]) + int(cr[0, 1])) // 2)
        cr[0, 2:4] = np.uint8((int(cr[0, 2]) + int(cr[0, 3])) // 2)
        cr[1, 0:2] = np.uint8((int(cr[1, 0]) + int(cr[1, 1])) // 2)
        cr[1, 2:4] = np.uint8((int(cr[1, 2]) + int(cr[1, 3])) // 2)

    elif ratio == "4:2:1":
        cb[0, :] = np.uint8((int(cb[0, 0]) + int(cb[0, 1]) + int(cb[0, 2]) + int(cb[0, 3])) // 4)
        cb[1, :] = np.uint8((int(cb[1, 0]) + int(cb[1, 1]) + int(cb[1, 2]) + int(cb[1, 3])) // 4)
        cr[0, 0:2] = np.uint8((int(cr[0, 0]) + int(cr[0, 1])) // 2)
        cr[0, 2:4] = np.uint8((int(cr[0, 2]) + int(cr[0, 3])) // 2)
        cr[1, 0:2] = np.uint8((int(cr[1, 0]) + int(cr[1, 1])) // 2)
        cr[1, 2:4] = np.uint8((int(cr[1, 2]) + int(cr[1, 3])) // 2)

    elif ratio == "4:2:0":
        cb[:, 0:2] = np.uint8((int(cb[0, 0]) + int(cb[0, 1]) + int(cb[1, 0]) + int(cb[1, 1])) // 4)
        cb[:, 2:4] = np.uint8((int(cb[0, 2]) + int(cb[0, 3]) + int(cb[1, 2]) + int(cb[1, 3])) // 4)
        cr[:, 0:2] = np.uint8((int(cr[0, 0]) + int(cr[0, 1]) + int(cr[1, 0]) + int(cr[1, 1])) // 4)
        cr[:, 2:4] = np.uint8((int(cr[0, 2]) + int(cr[0, 3]) + int(cr[1, 2]) + int(cr[1, 3])) // 4)

    elif ratio == "4:1:1":
        cb[0, :] = np.uint8((int(cb[0, 0]) + int(cb[0, 1]) + int(cb[0, 2]) + int(cb[0, 3])) // 4)
        cb[1, :] = np.uint8((int(cb[1, 0]) + int(cb[1, 1]) + int(cb[1, 2]) + int(cb[1, 3])) // 4)
        cr[0, :] = np.uint8((int(cr[0, 0]) + int(cr[0, 1]) + int(cr[0, 2]) + int(cr[0, 3])) // 4)
        cr[1, :] = np.uint8((int(cr[1, 0]) + int(cr[1, 1]) + int(cr[1, 2]) + int(cr[1, 3])) // 4)

    elif ratio == "4:1:0":
        cb[:, :] = np.uint8((int(cb[0, 0]) + int(cb[0, 1]) + int(cb[0, 2]) + int(cb[0, 3]) + int(cb[1, 0]) + int(
            cb[1, 1]) + int(cb[1, 2]) + int(cb[1, 3])) // 8)
        cr[:, :] = np.uint8((int(cr[0, 0]) + int(cr[0, 1]) + int(cr[0, 2]) + int(cr[0, 3]) + int(cr[1, 0]) + int(
            cr[1, 1]) + int(cr[1, 2]) + int(cr[1, 3])) // 8)

    elif ratio == "3:1:1":
        y[0, 1:3] = np.uint8((int(y[0, 1]) + int(y[0, 2])) // 2)
        y[1, 1:3] = np.uint8((int(y[1, 1]) + int(y[1, 2])) // 2)
        cb[0, :] = np.uint8((int(cb[0, 0]) + int(cb[0, 1]) + int(cb[0, 2]) + int(cb[0, 3])) // 4)
        cb[1, :] = np.uint8((int(cb[1, 0]) + int(cb[1, 1]) + int(cb[1, 2]) + int(cb[1, 3])) // 4)
        cr[0, :] = np.uint8((int(cr[0, 0]) + int(cr[0, 1]) + int(cr[0, 2]) + int(cr[0, 3])) // 4)
        cr[1, :] = np.uint8((int(cr[1, 0]) + int(cr[1, 1]) + int(cr[1, 2]) + int(cr[1, 3])) // 4)


def subsample_first_value(sample: NDArray, ratio: str):
    y = sample[:, :, 0]
    cb = sample[:, :, 1]
    cr = sample[:, :, 2]

    if ratio == "4:4:2":
        cb[1, 0:2] = cb[1, 0]
        cb[1, 2:4] = cb[1, 2]
        cr[1, 0:2] = cr[1, 2]
        cr[1, 2:4] = cr[1, 2]

    elif ratio == "4:4:1":
        cb[1, :] = cb[1, 0]
        cr[1, :] = cr[1, 0]

    elif ratio == "4:4:0":
        cb[1, :] = cb[0, :]
        cr[1, :] = cr[0, :]

    elif ratio == "4:2:2":
        cb[0, 0:2] = cb[0, 0]
        cb[0, 2:4] = cb[0, 2]
        cb[1, 0:2] = cb[1, 0]
        cb[1, 2:4] = cb[1, 2]
        cr[0, 0:2] = cr[0, 0]
        cr[0, 2:4] = cr[0, 2]
        cr[1, 0:2] = cr[1, 0]
        cr[1, 2:4] = cr[1, 2]

    elif ratio == "4:2:1":
        cb[0, :] = cb[0, 0]
        cb[1, :] = cb[1, 0]
        cr[0, 0:2] = cr[0, 0]
        cr[0, 2:4] = cr[0, 2]
        cr[1, 0:2] = cr[1, 0]
        cr[1, 2:4] = cr[1, 2]

    elif ratio == "4:2:0":
        cb[:, 0:2] = cb[0, 0]
        cb[:, 2:4] = cb[0, 2]
        cr[:, 0:2] = cr[0, 0]
        cr[:, 2:4] = cr[0, 2]

    elif ratio == "4:1:1":
        cb[0, :] = cb[0, 0]
        cb[1, :] = cb[1, 0]
        cr[0, :] = cr[0, 0]
        cr[1, :] = cr[1, 0]

    elif ratio == "4:1:0":
        cb[:, :] = cb[0, 0]
        cr[:, :] = cr[0, 0]

    elif ratio == "3:1:1":
        y[0, 1:3] = y[0, 1]
        y[1, 1:3] = y[1, 1]
        cb[0, :] = cb[0, 0]
        cb[1, :] = cb[1, 0]
        cr[0, :] = cr[0, 0]
        cr[1, :] = cr[1, 0]
