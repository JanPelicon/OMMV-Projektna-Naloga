import os 
import sys

def parse_args():
    
    dict_form = {}
    
    counter = 0
    while counter < len(sys.argv):
        arg = sys.argv[counter]


        if arg[0] == "-":
            if arg[1:] == "image":
                dict_form["image"] = sys.argv[counter+1]
            elif arg[1:] == "folder":
                dict_form["folder"] = sys.argv[counter+1]
            else:
                print("Not supported: ", arg[1:])
                exit()

        counter += 1
    
    return dict_form
    
    