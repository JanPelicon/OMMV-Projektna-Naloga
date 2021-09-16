import math
import numpy as np
from skimage.metrics import structural_similarity as ssim

from nptyping import NDArray


def mse(original: NDArray, subsampled: NDArray):
    return np.mean((original - subsampled) ** 2)


def psnr(mse_value: float):
    if mse_value == 0:
        return math.inf
    return 10 * math.log10((255*255) / mse_value)


def ss_ssim(original: NDArray, subsampled: NDArray):
    return ssim(original, subsampled, multichannel=True)


def bpp(ratio):
    if ratio == "4:4:4":
        return 24
    elif ratio == "4:4:2":
        return 20
    elif ratio == "4:4:1":
        return 18
    elif ratio == "4:4:0":
        return 16
    elif ratio == "4:2:2":
        return 16
    elif ratio == "4:2:1":
        return 14
    elif ratio == "4:2:0":
        return 12
    elif ratio == "4:1:1":
        return 12
    elif ratio == "4:1:0":
        return 10
    elif ratio == "3:1:1":
        return 10


def bpp_adaptive(image):
    bpp_value = 0
    for ratio in image["adaptive"]:
        bpp_value += bpp(ratio)
    bpp_value = bpp_value / len(image["adaptive"])
    bpp_value += len(image["adaptive"]) / (image["data"].shape[0] * image["data"].shape[1])
    return bpp_value
