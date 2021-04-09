import os
import argparse

# this takes all elements in a select folder and organizes 
# them to have consistent names (with current names as {char_index}_{any_string})
# used on custom_data/test and custom_data/train

parser = argparse.ArgumentParser()
parser.add_argument("file", nargs='?', const="")
args = parser.parse_args()
dirname = args.file

prefix_to_imgname = {}

for i in range(36):
    prefix_to_imgname[i] = []

for filename in os.listdir(dirname):
    str_label = filename[0:filename.find("_")]
    int_label = int(str_label)
    prefix_to_imgname[int_label].append(filename)

for i in range(0,36):
    count = 0
    for filename in prefix_to_imgname[i]:
        # get text between "_" and ".png"
        elem_after_underscore = filename[filename.find("_")+1:-4]

        try:
            # if it's an int, skip the element
            int_label = int(elem_after_underscore)
            continue
        except ValueError:
            not_valid_replacement = True
            while not_valid_replacement: 
                before_filename = os.path.join(dirname,filename)
                count+=1
                after_filename = os.path.join(dirname, f"{i}_{count}.png")
                try:
                    os.rename(before_filename,after_filename)
                    not_valid_replacement = False
                except FileExistsError:
                    continue

