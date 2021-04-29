import numpy as np
import math

def sample_subsample(sample, ratio, average):
    y = sample[:,:,0]
    cb = sample[:,:,1]
    cr = sample[:,:,2]

    if average:
        if ratio == "4:4:2":
            cb[1, 0:2] = np.uint8( (int(cb[1, 0]) + int(cb[1, 1]) ) // 2)
            cb[1, 2:4] = np.uint8( (int(cb[1, 2]) + int(cb[1, 3]) ) // 2)
            cr[1, 0:2] = np.uint8( (int(cr[1, 0]) + int(cr[1, 1]) ) // 2)
            cr[1, 2:4] = np.uint8( (int(cr[1, 2]) + int(cr[1, 3]) ) // 2)
        
        elif ratio == "4:4:1":
            cb[1, :] = np.uint8( (int(cb[1, 0]) + int(cb[1, 1]) + int(cb[1, 2]) + int(cb[1, 3]) ) // 4)
            cr[1, :] = np.uint8( (int(cr[1, 0]) + int(cr[1, 1]) + int(cr[1, 2]) + int(cr[1, 3]) ) // 4)

        elif ratio == "4:4:0":
            cb[:, 0] = np.uint8( (int(cb[0, 0]) + int(cb[1, 0]) ) // 2)
            cb[:, 1] = np.uint8( (int(cb[0, 1]) + int(cb[1, 1]) ) // 2)
            cb[:, 2] = np.uint8( (int(cb[0, 2]) + int(cb[1, 2]) ) // 2)
            cb[:, 3] = np.uint8( (int(cb[0, 3]) + int(cb[1, 3]) ) // 2)
            cr[:, 0] = np.uint8( (int(cr[0, 0]) + int(cr[1, 0]) ) // 2)
            cr[:, 1] = np.uint8( (int(cr[0, 1]) + int(cr[1, 1]) ) // 2)
            cr[:, 2] = np.uint8( (int(cr[0, 2]) + int(cr[1, 2]) ) // 2)
            cr[:, 3] = np.uint8( (int(cr[0, 3]) + int(cr[1, 3]) ) // 2)

        elif ratio == "4:2:2":
            cb[0, 0:2] = np.uint8( (int(cb[0, 0]) + int(cb[0, 1]) ) // 2)
            cb[0, 2:4] = np.uint8( (int(cb[0, 2]) + int(cb[0, 3]) ) // 2)
            cb[1, 0:2] = np.uint8( (int(cb[1, 0]) + int(cb[1, 1]) ) // 2)
            cb[1, 2:4] = np.uint8( (int(cb[1, 2]) + int(cb[1, 3]) ) // 2)          
            cr[0, 0:2] = np.uint8( (int(cr[0, 0]) + int(cr[0, 1]) ) // 2)
            cr[0, 2:4] = np.uint8( (int(cr[0, 2]) + int(cr[0, 3]) ) // 2)
            cr[1, 0:2] = np.uint8( (int(cr[1, 0]) + int(cr[1, 1]) ) // 2)
            cr[1, 2:4] = np.uint8( (int(cr[1, 2]) + int(cr[1, 3]) ) // 2)

        elif ratio == "4:2:1":
            cb[0, :] = np.uint8( (int(cb[0, 0]) + int(cb[0, 1]) + int(cb[0, 2]) + int(cb[0, 3]) ) // 4)
            cb[1, :] = np.uint8( (int(cb[1, 0]) + int(cb[1, 1]) + int(cb[1, 2]) + int(cb[1, 3]) ) // 4)
            cr[0, 0:2] = np.uint8( (int(cr[0, 0]) + int(cr[0, 1]) ) // 2)
            cr[0, 2:4] = np.uint8( (int(cr[0, 2]) + int(cr[0, 3]) ) // 2)
            cr[1, 0:2] = np.uint8( (int(cr[1, 0]) + int(cr[1, 1]) ) // 2)
            cr[1, 2:4] = np.uint8( (int(cr[1, 2]) + int(cr[1, 3]) ) // 2)

        elif ratio == "4:2:0":
            cb[:, 0:2] = np.uint8( (int(cb[0, 0]) + int(cb[0, 1]) + int(cb[1, 0]) + int(cb[1, 1]) ) // 4)
            cb[:, 2:4] = np.uint8( (int(cb[0, 2]) + int(cb[0, 3]) + int(cb[1, 2]) + int(cb[1, 3]) ) // 4)
            cr[:, 0:2] = np.uint8( (int(cr[0, 0]) + int(cr[0, 1]) + int(cr[1, 0]) + int(cr[1, 1]) ) // 4)
            cr[:, 2:4] = np.uint8( (int(cr[0, 2]) + int(cr[0, 3]) + int(cr[1, 2]) + int(cr[1, 3]) ) // 4)

        elif ratio == "4:1:1":
            cb[0, :] = np.uint8( (int(cb[0, 0]) + int(cb[0, 1]) + int(cb[0, 2]) + int(cb[0, 3]) ) // 4)
            cb[1, :] = np.uint8( (int(cb[1, 0]) + int(cb[1, 1]) + int(cb[1, 2]) + int(cb[1, 3]) ) // 4)
            cr[0, :] = np.uint8( (int(cr[0, 0]) + int(cr[0, 1]) + int(cr[0, 2]) + int(cr[0, 3]) ) // 4)
            cr[1, :] = np.uint8( (int(cr[1, 0]) + int(cr[1, 1]) + int(cr[1, 2]) + int(cr[1, 3]) ) // 4)

        elif ratio == "4:1:0":
            cb[:, :] = np.uint8( (int(cb[0, 0]) + int(cb[0, 1]) + int(cb[0, 2]) + int(cb[0, 3]) + int(cb[1, 0]) + int(cb[1, 1]) + int(cb[1, 2]) + int(cb[1, 3])) // 8)
            cr[:, :] = np.uint8( (int(cr[0, 0]) + int(cr[0, 1]) + int(cr[0, 2]) + int(cr[0, 3]) + int(cr[1, 0]) + int(cr[1, 1]) + int(cr[1, 2]) + int(cr[1, 3])) // 8)

        elif ratio == "3:1:1":
            y[0, 1:3] = np.uint8( (int(y[0, 1]) + int(y[0, 2]) ) // 2)
            y[1, 1:3] = np.uint8( (int(y[1, 1]) + int(y[1, 2]) ) // 2)
            cb[0, :] = np.uint8( (int(cb[0, 0]) + int(cb[0, 1]) + int(cb[0, 2]) + int(cb[0, 3]) ) // 4)
            cb[1, :] = np.uint8( (int(cb[1, 0]) + int(cb[1, 1]) + int(cb[1, 2]) + int(cb[1, 3]) ) // 4)
            cr[0, :] = np.uint8( (int(cr[0, 0]) + int(cr[0, 1]) + int(cr[0, 2]) + int(cr[0, 3]) ) // 4)
            cr[1, :] = np.uint8( (int(cr[1, 0]) + int(cr[1, 1]) + int(cr[1, 2]) + int(cr[1, 3]) ) // 4)

    else: # NOT AVERAGE
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

def image_subsample(samples, ratio="4:4:4", average=False):
    for sample in samples:
        sample_subsample(sample["sample"], ratio, average)

"""
ADAPTIVE
"""

def image_subsample_adaptive(image, samples, subsample_ratios):
    y_size = image["data"].shape[0]
    x_size = image["data"].shape[1]

    x_blocks = math.ceil(image["data"].shape[1] / 16) 

    count = [0,0,0]

    for iy in range(0, y_size, 16):
        for ix in range(0, x_size, 16):
            y_max = min(iy + 16, y_size)
            x_max = min(ix + 16, x_size)

            std = np.std(image["data"][iy:y_max, ix:x_max, 1:2]) 

            if std < 4.0:
                image["adaptive"].append(subsample_ratios[1])
            else:
                image["adaptive"].append(subsample_ratios[0])

    for sample in samples:
        y_block = sample["y"] // 16
        x_block = sample["x"] // 16

        ratio = image["adaptive"][y_block * x_blocks + x_block]

        sample_subsample(sample["sample"], ratio, True) 
