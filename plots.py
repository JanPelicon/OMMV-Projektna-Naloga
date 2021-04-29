from py_files.functions import *
from py_files.parser import *
from py_files.subsampler import *

args = parse_args()
images = image_load(args)
for image in images:
    image["data"] = image_cut_extra(image["data"])
    image["data"] = image_rgb2ycbcr(image["data"])

subsample_ratios = [ 
    "4:4:2",
    "4:4:1",
    "4:4:0",
    "4:2:2",
    "4:2:1",
    "4:2:0",
    "4:1:1",
    "4:1:0",
    "3:1:1"]

pnsr_results = [[0] * len(subsample_ratios), [0] * len(subsample_ratios)]
ssim_results = [[0] * len(subsample_ratios), [0] * len(subsample_ratios)]
bpp_results = [[0] * len(subsample_ratios), [0] * len(subsample_ratios)]

average = [False, True]

for count_avg, avg in enumerate(average):
    for p, image in enumerate(images):
        print(p)
        for count_ratio, ratio in enumerate(subsample_ratios):
            temp_image = np.copy(image["data"])
            samples = image_samples_get(temp_image)
            image_subsample(samples, ratio, average=avg)
            

            mse = image_mse(image["data"], temp_image)
            psnr = image_psnr(mse)
            ss_ssim = image_ss_ssim(image["data"], temp_image)
            bpp = image_bpp(ratio)

            pnsr_results[count_avg][count_ratio] += psnr
            ssim_results[count_avg][count_ratio] += ss_ssim
            bpp_results[count_avg][count_ratio] += bpp

# MEAN
for count_avg, avg in enumerate(average):
    for count_ratio, ratio in enumerate(subsample_ratios):
        pnsr_results[count_avg][count_ratio] /= len(images)
        ssim_results[count_avg][count_ratio] /= len(images)
        bpp_results[count_avg][count_ratio] /= len(images)

        print("\n{}   avg = {}".format(ratio, avg))
        print("  PSNR = {:.3f}".format(pnsr_results[count_avg][count_ratio]))
        print("  SS-SSIM = {:.3f}".format(ssim_results[count_avg][count_ratio]))
        print("  BPP = {:.3f}".format(bpp_results[count_avg][count_ratio]))

"""
ADAPTIVE
"""

args = parse_args()

subsample_adaptive_ratios = [
    ["4:4:2", "4:2:2"],
    ["4:4:2", "4:2:0"],
    ["4:2:2", "4:1:0"],
    ["4:2:0", "4:1:0"]]

pnsr_adaptive_results = [0] * len(subsample_adaptive_ratios)
ssim_adaptive_results = [0] * len(subsample_adaptive_ratios)
bpp_adaptive_results = [0] * len(subsample_adaptive_ratios)

for index, sr in enumerate(subsample_adaptive_ratios):
    print(index)
    images = image_load(args)
    for image in images:
        image["data"] = image_cut_extra(image["data"])
        image["data"] = image_rgb2ycbcr(image["data"])

    for p, image in enumerate(images):
        
        temp_image = np.copy(image["data"])
        samples = image_samples_get(temp_image)

        image_subsample_adaptive(image, samples, sr)           

        mse = image_mse(image["data"], temp_image)
        psnr = image_psnr(mse)
        ss_ssim = image_ss_ssim(image["data"], temp_image)
        bpp = image_bpp_adaptive(image)

        pnsr_adaptive_results[index] += psnr
        ssim_adaptive_results[index] += ss_ssim
        bpp_adaptive_results[index] += bpp

        #image_show(temp_image, " ".join(sr), convert=True)

# MEAN
for index, sr in enumerate(subsample_adaptive_ratios):
    pnsr_adaptive_results[index] /= len(images)
    ssim_adaptive_results[index] /= len(images)
    bpp_adaptive_results[index] /= len(images)

    print()
    print(" ".join(sr))
    print("  PSNR = {:.3f}".format(pnsr_adaptive_results[index]))
    print("  SS-SSIM = {:.3f}".format(ssim_adaptive_results[index]))
    print("  BPP = {:.3f}".format(bpp_adaptive_results[index]))

# PLOT
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
plt.figure(1)
plt.ylabel("PSNR")
plt.xlabel('BPP')
ax.scatter(bpp_results[0], pnsr_results[0], marker="s", label="Default")
ax.scatter(bpp_results[1], pnsr_results[1], marker="x", label="Average")

ax.scatter(bpp_adaptive_results[0], pnsr_adaptive_results[0], marker="v", label="Adaptive (4:4:2, 4:2:2)")
ax.scatter(bpp_adaptive_results[1], pnsr_adaptive_results[1], marker="^", label="Adaptive (4:4:2, 4:2:0)")
ax.scatter(bpp_adaptive_results[2], pnsr_adaptive_results[2], marker="<", label="Adaptive (4:2:2, 4:1:0)")
ax.scatter(bpp_adaptive_results[3], pnsr_adaptive_results[3], marker=">", label="Adaptive (4:2:0, 4:1:0)")

for count, ratio in enumerate(subsample_ratios):
    ax.annotate(" "+ratio, (bpp_results[0][count], pnsr_results[0][count]))
    ax.annotate(" "+ratio, (bpp_results[1][count], pnsr_results[1][count]))
"""
for count, sr in enumerate(subsample_adaptive_ratios):
    text = "\n ".join(sr)
    text = " " + text
    ax.annotate(text, (bpp_adaptive_results[count], pnsr_adaptive_results[count]))
"""
plt.xlim([8, 24])
plt.legend(loc="lower right")

fig, ax = plt.subplots()
plt.figure(2)
plt.ylabel("SSIM")
plt.xlabel('BPP')
ax.scatter(bpp_results[0], ssim_results[0], marker="s", label="Default")
ax.scatter(bpp_results[1], ssim_results[1], marker="x", label="Average")

ax.scatter(bpp_adaptive_results[0], ssim_adaptive_results[0], marker="v", label="Adaptive (4:4:2, 4:2:2)")
ax.scatter(bpp_adaptive_results[1], ssim_adaptive_results[1], marker="^", label="Adaptive (4:4:2, 4:2:0)")
ax.scatter(bpp_adaptive_results[2], ssim_adaptive_results[2], marker="<", label="Adaptive (4:2:2, 4:1:0)")
ax.scatter(bpp_adaptive_results[3], ssim_adaptive_results[3], marker=">", label="Adaptive (4:2:0, 4:1:0)")

for count, ratio in enumerate(subsample_ratios):
    ax.annotate(" "+ratio, (bpp_results[0][count], ssim_results[0][count]))
    ax.annotate(" "+ratio, (bpp_results[1][count], ssim_results[1][count]))
"""
for count, sr in enumerate(subsample_adaptive_ratios):
    text = "\n ".join(sr)
    text = " " + text
    ax.annotate(text, (bpp_adaptive_results[count], ssim_adaptive_results[count]))
"""
plt.xlim([8, 22])
plt.legend(loc="lower right")

plt.show()
