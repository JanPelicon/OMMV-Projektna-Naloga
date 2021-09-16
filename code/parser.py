import sys
import os


def parser():

    images = []
    ratios = []
    average = False
    show = False

    for file in os.listdir("./kodak_dataset"):
        if file.endswith(".png") or file.endswith(".jpg"):
            images.append(os.path.join("./kodak_dataset", file))

    for index, arg in enumerate(sys.argv):

        if arg == "--images" or arg == "-i":
            images = []
            for file in os.listdir("./custom_images"):
                if file.endswith(".png") or file.endswith(".jpg"):
                    images.append(os.path.join("./custom_images", file))

        elif arg == "--ratios" or arg == "-r":
            if sys.argv[index+1][0:2] == "--":
                print("Ratio format incorrect!")
                display_help()
            else:
                ratios = sys.argv[index+1].split(",")

        elif arg == "--average" or arg == "-a":
            average = True

        elif arg == "--show" or arg == "-s":
            show = True

        elif arg == "--help" or arg == "-h":
            display_help()

    if len(images) == 0:
        print("No images in directory!")
        display_help()

    if len(ratios) == 0:
        print("No ratios specified!")
        display_help()

    return images, ratios, average, show


def display_help():
    print("-h --help\t\t(display help)")
    print("-i --images\t\t(use custom images instead of kodak dataset)")
    print("-s --show\t\t(show subsampled images)")
    print("-a --average\t\t(use average sampling instead of first value sampling)")
    print("-r --ratios\t\t(specify the list of ratios - example: [-r \"4:4:2,4:2:0,3:1:1\"])")
    print("Possible ratios: 4:4:2, 4:4:1, 4:4:0, 4:2:2, 4:2:1, 4:2:0, 4:1:1, 4:1:0, 3:1:1")
    print("adaptive_chroma_subsampling.py requires exactly 2 ratios - example [-r \"4:4:2,4:2:0\"]\n")
    sys.exit()
