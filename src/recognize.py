import cv2
import numpy as np
import argparse
import time
from datetime import datetime
from pathlib import Path   

# local files
import constants
import photo_preprocessing
import letter_extraction
import load_ml
import platenum_postprocessing
if not constants.CREATE_BIN:
    import c_interfacing_utils

# Read the plate number from the given image
# args: 
# > the corners used to crop the original image 
# > the image to crop and detect
# > whether or not the function should use the aforementioned corners to skew the image
# > if nonempty, contains the actual value for the plate to compare (for debugging)
# returns:
# > the detected plate number, empty if no plate detected
def perform_read(corners,img,should_skew, should_be):
    img = cv2.resize(img, constants.RESIZE_SIZE )
    if (should_skew):
        dst = photo_preprocessing.straighten_crop(corners, img)
    else:
        dst= img

    if constants.SAVE_DEBUG or constants.SAVE_ORIGINALS:
        now = datetime.now()
        newfilename = f"./intermediate_photos/{datetime.today().strftime('%Y-%m-%d_%H%M%S')}.png"
        print(newfilename)
        cv2.imwrite(newfilename,dst)

    if constants.DEBUG:
        cv2.imshow('image',dst)
        cv2.waitKey(0)


    # crop letters out of photo
    images = letter_extraction.crop_letters(dst)

            
    if constants.DEBUG:
        cv2.imshow('image',dst)
        cv2.waitKey(0)

    # sort keys by distance from the left
    keys = sorted(images.keys(), reverse=False)

    if (len(keys) <= 2):
        print(f"NOTHING PARKED - {datetime.now().time()}")
        return ""
    else:
        
        recog_imgs = []
        for key in keys:
            recog_imgs.append(images[key])

        # either generate the bin files to perform low-level ML or use python ML to get answer
        if constants.GEN_BIN:
            plate_num = load_ml.recog_images_c(recog_imgs)
        else:
            plate_num = load_ml.recog_images_tensorflow(recog_imgs)
        
        should_be = should_be.replace(" ", "")
        if len(should_be) > 0:
            for i in range(len(plate_num)):
                try:
                    if should_be[i] != plate_num[i]:
                        cv2.imwrite(f"./output/{should_be[i]}_{plate_num}_{i}_{plate_num[i]}.png",recog_imgs[i])
                except IndexError:
                    cv2.imwrite(f"./output/{plate_num}_{i}_{plate_num[i]}.png",recog_imgs[i])

        plate_num = platenum_postprocessing.apply_spaces(keys, plate_num)

                    

        print(f"\n\n\'{plate_num}\' PARKED - {datetime.now().time()}")


        return plate_num

# Perform a read from the camera every <PHOTO_INTERVAL> seconds and writes results to a file called "<OUTPUT_FILENAME> <DATE>"
def perform_reading_loop():

    filename = f"{constants.OUTPUT_FILENAME} {datetime.today().strftime('%Y-%m-%d')}.txt"
    with open(filename, "w") as f:
        f.write("START:\n")
        
    should_be = ""
    if constants.PROMPT_CHECKER:
        should_be = input("what is the plate number of what you're about to scan?\n> ")

    while True:
        img = None
        should_skew = True
        corners,img, should_skew = photo_preprocessing.take_photo()
        if (corners is None):
            break

        plate_num = perform_read(corners,img,should_skew,should_be)
        if len(plate_num) == 0:
            writing_str = f"NOTHING PARKED - {datetime.now().time()}\n"
        else:
            writing_str = f"{plate_num} PARKED - {datetime.now().time()}\n"
        with open(filename, "a") as f:
            f.write(writing_str)
        time.sleep(constants.PHOTO_INTERVAL)
        
# Read a singular file into algorithm and return
# args:
# > file: path to photo to analyze
# returns:
# > the detected plate number
def perform_reading_singular(file):
    img = None
    should_skew = True
    # if a photo is passed in, read it in and use it
    img = cv2.imread(file,cv2.IMREAD_COLOR)
    corners, _, should_skew = photo_preprocessing.find_plate(img)

    plate_name = ""
    if constants.PROMPT_CHECKER:
        plate_name = Path(file).name
        plate_name = plate_name[:plate_name.find(".")]
    return perform_read(corners,img,should_skew,plate_name)

if __name__ == "__main__":
    
    if constants.GEN_BIN and not constants.CREATE_BIN:
        c_interfacing_utils.load_c_nn()

    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs='?', const="")
    args = parser.parse_args()

    if args.file is None:
        perform_reading_loop()
    else:
        perform_reading_singular(args.file)
