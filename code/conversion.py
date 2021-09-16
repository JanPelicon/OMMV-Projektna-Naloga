import cv2

from nptyping import NDArray


def convert_RGB_YCbCr(image: NDArray) -> NDArray:
    return cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)


def convert_YCbCr_RGB(image: NDArray) -> NDArray:
    return cv2.cvtColor(image, cv2.COLOR_YCR_CB2BGR)
