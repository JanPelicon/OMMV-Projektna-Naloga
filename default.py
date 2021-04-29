from py_files.functions import *
from py_files.parser import *
from py_files.subsampler import *

args = parse_args()
images = image_load(args)
for image in images:
    image["data"] = image_cut_extra(image["data"])
    image["data"] = image_rgb2ycbcr(image["data"])

subsample_ratios = [
    #"4:4:4",
    "4:4:2",
    "4:4:1",
    "4:4:0",

    "4:2:2",
    "4:2:1",
    "4:2:0",

    "4:1:1",
    "4:1:0"]

pnsr_results = [[0] * len(subsample_ratios), [0] * len(subsample_ratios)]
ssim_results = [[0] * len(subsample_ratios), [0] * len(subsample_ratios)]
bpp_results = [[0] * len(subsample_ratios), [0] * len(subsample_ratios)]

average = [False, True]

for count_avg, avg in enumerate(average):
    for image in images:
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

            """
            #image_show(temp_image, ratio, convert=True)
            print("\n" + image["name"])
            print(ratio)
            print("  PSNR = {:.3f}".format(psnr))
            print("  SS-SSIM = {:.3f}".format(ss_ssim))
            print("  BPP = {:.3f}".format(bpp))
            """

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


# PLOT
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
plt.figure(1)
plt.ylabel("PSNR")
plt.xlabel('BPP')
ax.scatter(bpp_results[0], pnsr_results[0], marker="^", label="Default")
ax.scatter(bpp_results[1], pnsr_results[1], marker="8", label="Composite")
for count, ratio in enumerate(subsample_ratios):
    ax.annotate(ratio, (bpp_results[0][count], pnsr_results[0][count]))
    ax.annotate(ratio, (bpp_results[1][count], pnsr_results[1][count]))
plt.legend(loc="lower right")

fig, ax = plt.subplots()
plt.figure(2)
plt.ylabel("SS-SSIM")
plt.xlabel('BPP')
ax.scatter(bpp_results[0], ssim_results[0], marker="^", label="Default")
ax.scatter(bpp_results[1], ssim_results[1], marker="8", label="Composite")
for count, ratio in enumerate(subsample_ratios):
    ax.annotate(ratio, (bpp_results[0][count], ssim_results[0][count]))
    ax.annotate(ratio, (bpp_results[1][count], ssim_results[1][count]))
plt.legend(loc="lower right")

plt.show()