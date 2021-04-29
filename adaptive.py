from py_files.functions import *
from py_files.parser import *
from py_files.subsampler import *

args = parse_args()

subsample_ratios = [
    ["4:4:0", "4:2:0", "4:1:0"],
    ["4:4:0", "4:2:0", "3:1:1"],
    ["4:2:0", "4:1:0", "3:1:1"],
    ["4:2:0", "3:1:1", "2:1:1"]]

pnsr_adaptive_results = [0] * len(subsample_ratios)
ssim_adaptive_results = [0] * len(subsample_ratios)
bpp_adaptive_results = [0] * len(subsample_ratios)

for index, sr in enumerate(subsample_ratios):

    images = image_load(args)
    for image in images:
        image["data"] = image_cut_extra(image["data"])
        image["data"] = image_rgb2ycbcr(image["data"])

    for image in images:
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

        image_show(temp_image, " ".join(sr), convert=True)

# MEAN
for index, sr in enumerate(subsample_ratios):
    pnsr_adaptive_results[index] /= len(images)
    ssim_adaptive_results[index] /= len(images)
    bpp_adaptive_results[index] /= len(images)

    print()
    print(" ".join(sr))
    print("  PSNR = {:.3f}".format(pnsr_adaptive_results[index]))
    print("  SS-SSIM = {:.3f}".format(ssim_adaptive_results[index]))
    print("  BPP = {:.3f}".format(bpp_adaptive_results[index]))

wait()
