import cv2
import math
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim

def image_load(dict_form):
    temp = []
   
    if "image" in dict_form.keys():
        image = {
            "name": dict_form["image"],
            "data": cv2.imread(dict_form["image"]),
            "adaptive": []
        }
        temp.append(image)        

    elif "folder" in dict_form.keys():
        for image_name in os.listdir(dict_form["folder"]):
            image = {
                "name": image_name,
                "data": cv2.imread(dict_form["folder"] + "/" + image_name),
                "adaptive": []
            }
            temp.append(image)   

    return temp

def image_rgb2ycbcr(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)

def image_ycbcr2rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_YCR_CB2BGR)

def image_show(image, name, convert=False):
    if convert:
        image = image_ycbcr2rgb(image)
    cv2.imshow(name, image)
    cv2.waitKey(1)

def image_info(image):
    size = image.shape
    print("Size: {} x {} x {}".format(size[1], size[0], size[2]))

def image_crop_center(image, new_size):
    size_x = new_size[0] // 2
    size_y = new_size[1] // 2
    center_x = image.shape[1] // 2
    center_y = image.shape[0] // 2
    return image[center_y-size_y:center_y+size_y, center_x-size_x:center_x+size_x]

def image_cut_extra(image):
    size_x = image.shape[1]
    size_y = image.shape[1]
    size_x = size_x - (size_x % 4)
    size_y = size_y - (size_y % 2)
    return image[0:size_y, 0:size_x, :]

def image_samples_get(image):
    samples_list = []
    for iy in range(0, image.shape[0], 2):
        for ix in range(0, image.shape[1], 4):
            dict_form = {
                "y": iy,
                "x": ix,
                "sample": image[iy:iy+2, ix:ix+4, :]
            }
            samples_list.append(dict_form)
    return samples_list

def sample_print(sample):
    sample = sample["sample"]
    print("{}    {}    {}    {}\n{}    {}    {}    {}".format(
        sample[0,0], sample[0,1], sample[0,2], sample[0,3],
        sample[1,0], sample[1,1], sample[1,2], sample[1,3]
    ))

def sample_show(sample, name, constant_luma=False):
    temp = np.ndarray((256,512,3), dtype=np.uint8)
    for iy in range(sample["sample"].shape[0]):
        for ix in range(sample["sample"].shape[1]):
            temp[iy*128:(iy+1)*128, ix*128:(ix+1)*128,:] = sample["sample"][iy,ix,:]
    if constant_luma:
        temp[:,:,0] = 127
    cv2.imshow(name, image_ycbcr2rgb(temp))
    cv2.waitKey(1)

def sample_get_test():
    return np.random.randint(0, 255, (2,4,3), dtype=np.uint8)

def image_mse(image_0, image_1):
    return np.mean((image_0 - image_1) ** 2)

def image_psnr(mse):
    if mse == 0:
        return math.inf
    return 10 * math.log10((255*255) / mse)  

def image_ss_ssim(image_0, image_1):
    return ssim(image_0, image_1, multichannel=True)
    #return ssim(image_0, image_1, data_range=image_0.max() - image_0.min(), multichannel=True)

def image_bpp(ratio):
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

def image_bpp_adaptive(image):
    bpp = 0
    for ratio in image["adaptive"]:
        bpp += image_bpp(ratio)
    bpp = bpp / len(image["adaptive"])  
    bpp += len(image["adaptive"]) / (image["data"].shape[0] * image["data"].shape[1])
    return bpp

def wait():
    cv2.waitKey(0)