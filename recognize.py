import cv2
import imutils
import numpy as np
import argparse
import load_ml
import math
import time
from datetime import datetime
import sys
from pathlib import Path   

filename = "log_"
GEN_BIN = False # when false, the script will use ML model to read plate
DEBUG = True # when true, intermittent photos will pop up with letter extraction progress
PROMPT_CHECKER = False # whether or not to compare result to given value ahead of time
GEN_PHOTOS = False # whether to always generate letters extracted in output/*
SHOW_CAM_FRAMES = True # whether or not to show camera frames when detecting

USE_WEBCAM_NUMBER = 1 # starts at 0, set to 0 if you only have one webcam connected; I'm just using my secondary webcam
PHOTO_INTERVAL = 15 # number of seconds between shots

# Given an array of corner co-ordinates, return the indices or the top (index = 0) or right (index = 1) corners
# args:
# > vertex_array: the input array of corner coorindates
# > index: 0 if you want the top indices and 1 if you want the right indices.
# returns:
# > indices of requested side.
def separate_sides(vertex_array, index):
    # get the indices of either the top corners or right corners
    # 0 - top corners ; 1 - right corners

    target_indices = []
    max_value = float('-inf')
    max_index = 0
    for idx,a in enumerate(vertex_array):
        if (a[index] > max_value):
            max_index = idx
            max_value = a[index]
        
    target_indices.append(max_index)

    max_value = float('-inf')
    for idx,a in enumerate(vertex_array):
        if (a[index] > max_value) and (idx not in target_indices):
            max_index = idx
            max_value = a[index]

    target_indices.append(max_index)


    return target_indices


# Given two numbers, find whether they are within <count> of one another
# args:
# > elem1, elem2: the two values to compare
# > count: the maximum difference between the two elems
# returns:
# > whether the elems are within <count> apart
def within_range(elem1, elem2, count):
    return (elem1 < elem2 + count and elem1 > elem2 - count)

# Turn on camera and try to find edges of plate. If it cannot find it, take a photo after 50 loops of not much motion
# returns:
# > taken photo with any cropping performed if possible
def take_photo():
    # run webcam to take photo

    print("getting ready to take photo...")
    # define a video capture object 
    vid = cv2.VideoCapture(USE_WEBCAM_NUMBER) 

    img = None
    frame = None
    should_skew = True
    last_frame = None
    frame_nums_without_detection = 0
    frame_num_count = 0
    prev_corners = []
    consec_detect = 0
    while(True): 

        if frame_num_count > 5:
            if last_frame is not None:
                frame_diff = cv2.absdiff(last_frame,frame)
                print(frame_nums_without_detection)
                if (frame_diff.sum() < 15000000):
                    frame_nums_without_detection +=1
                else:
                    frame_nums_without_detection =0

            frame_num_count = 0
            last_frame = frame
        
        frame_num_count+=1

        # Capture the video frame 
        ret, frame = vid.read() 

        corner_points, marked_img, should_skew = find_plate(frame)
        if (marked_img is None):
            marked_img = cv2.resize(frame, (600,400) )
            corner_points = []

            consec_detect = 0
            prev_corners = []
        else:
            frame_nums_without_detection = 0
            if (consec_detect > 0 ):
                same_range  = True
                for i in range(len(corner_points)):
                    if (not within_range(corner_points[i][0],prev_corners[i][0],5)):
                        same_range = False
                        break
                if same_range:
                    consec_detect+=1
                    prev_corners = corner_points

                    if (consec_detect == 3):
                        break
                else:
                    consec_detect = 0
                    prev_corners = []
            else:
                consec_detect=1
                prev_corners = corner_points
                

        if (frame_nums_without_detection > 10):
            break



        # show image with markings in where it found the rectangle
        if SHOW_CAM_FRAMES:
            cv2.imshow('frame', marked_img) 
            
        # press q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
    # After the loop release the cap object 
    vid.release() 
    # Destroy all the windows 
    cv2.destroyAllWindows() 

    return corner_points, frame, should_skew

# Given two points, magnitude of the vector they create
# args:
# > p1, p2: the two points to create the vector 
# returns:
# > the magnitude of the vector connecting P2 and P1
def distance_between_points(p2, p1):
    return (((p2[0] - p1[0])**2)+((p2[1] - p1[1])**2))**0.5

# Given three points, find the angle that p1-p2-p3 make
# args:
# > p1, p2, p3: the three points that create the angle
# returns:
# > the angle created from points
def find_angle_between(p1, p2, p3):
    l3= distance_between_points(p2, p1)
    l1= distance_between_points(p3, p2)
    l2= distance_between_points(p1, p3)
    try:
        angle = (math.acos((l1+l3-l2)/(2*l3*l2))*180.0)/math.pi
    except ValueError:
        angle=0
    return angle

# Reorder the given array to be in the following order:
#  4 ---- 3
#  |      |
#  1 ---- 2
# args: v
# > vertex_array: vertex array of square-like object
# returns:
# > vertex array in the above array order
def reorder_vertex_array(vertex_array):
    # reorder the array of vertices to prepare to a re-skewing of image

    topleft_index = 0
    topright_index = 0
    bottomleft_index = 0
    bottomright_index = 0

    top_indices = []
    bottom_indices = []

    top_indices = separate_sides(vertex_array, 1)
    right_indices = separate_sides(vertex_array, 0)

    for idx in range(len(vertex_array)):
        if (idx in top_indices):
            if (idx in right_indices):
                topright_index = idx
            else:
                topleft_index = idx
        else:
            if (idx in right_indices):
                bottomright_index = idx
            else:
                bottomleft_index = idx

    # should be in the order:
    #  4 ---- 3
    #  |      |
    #  1 ---- 2


    vertex_array_rearranged = [vertex_array[i] for i in [bottomleft_index, bottomright_index,topright_index, topleft_index]]


    return vertex_array_rearranged

# Re-shape and crop an image based on new corner points in the following array order:
#  4 ---- 3
#  |      |
#  1 ---- 2
# args:
# > new_corners: corners in the above array order
# > img: the image to skew
# returns:
# > skewed/cropped image.
def straighten_crop(new_corners, img):

    pts_before = np.float32([new_corners])
    pts_after = np.float32([[0,0],[600,0],[600,300],[0,300]])
    perspective_transform = cv2.getPerspectiveTransform(pts_before,pts_after)
    dst = cv2.warpPerspective(img,perspective_transform,(600,300))
    return dst

# Given a license plate, try to find the edges of the plate to reduce background clutter before letter extraction
# args:
# > img: full image with plate
# returns:
# > the corners of the actual plate if found
# > the image marked with the rectangle detected (during above corners)
# > whether or not the corners were found
def find_plate(img):
    # identify where the plate is in the photo and return the marked img and cropped img
    # initial transforming
    img = cv2.resize(img, (600,400) )
    corners = []
    proportions_changed = False

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    gray = cv2.bilateralFilter(gray, 13, 15, 15) 

    edged = cv2.Canny(gray, 20, 200) 


    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
    dilated = cv2.dilate(edged, kernel)

    contours = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:15]
    dst = None
    marked_img = None
    # iterate through candidates
    for c in contours:

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        if (cv2.contourArea(c) < 400*600/4):
            break #frame should take at least a quarter of the screen

        if len(approx) == 4:
            # re-skew array so that the image is a perfect rectangle
            subarray = []
            for a in approx:
                # due to nature of shape, approx should only need first element extracted
                subarray.append(a[0])

            corners = reorder_vertex_array(subarray)

            correct_angles = True
            for i in range(4):
                i_1 = i % 4
                i_2 = (i+1) % 4
                i_3 = (i+2) % 4
                angle_between = find_angle_between(corners[i_1],corners[i_2],corners[i_3])
                if (angle_between > 100.0 or angle_between < 80.0):
                    correct_angles = False
                    break

            if (not correct_angles):
                continue


            marked_img = img.copy()
            cv2.drawContours(marked_img,[approx], -1, (255, 0, 0), 2)

            proportions_changed = True
            break
        
    return corners, marked_img, proportions_changed

# Make an extracted letter formatted well for the ML analysis
# args:
# > regular cropped letter image from original image
# returns:
# > image filtered and reduced for ML model.
def process_letter(img):
    blur = cv2.blur(img,(10,10))
    max_dimen = max(img.shape[0],img.shape[1])
    vert_border = int((max_dimen-img.shape[0])/2)
    hori_border = int((max_dimen-img.shape[1])/2)
    image = cv2.copyMakeBorder(blur, vert_border, vert_border, hori_border, hori_border, cv2.BORDER_CONSTANT) 
    image = cv2.resize(image, (28,28) )
    return image

# Create a factor of difference between (y1, h1) and (y2, h2)
# args:
# > y1, y2: two y-midpoints to compare
# > h1, h2: two heights to compare
# returns:
# > weighted factor of the elements of 1 and 2.
def compare_vals(y1, h1, y2, h2):
    factor_y=(abs((y1**2)-(y2**2)))**0.5
    factor_h=(abs((h1**2)-(h2**2)))**0.5
    return factor_y*2 +factor_h

# Remove odd detected shapes from photo
# args:
# > img: dict mapping leftmost x-coordinate of character to image of character
# > captured_data: data relating y-coordinate, height, and x-coordinate of each image
# returns:
# > new filtered dict mapping leftmost x-coordinate of character to image of character with no/less outliers
def remove_outliers(images, captured_data):

    len_of_data = len(captured_data)
    comparison_arr = np.full((len_of_data,len_of_data), 10000)

    for i in range(len_of_data):
        for j in range(i+1,len_of_data):
            comparison_arr[i][j] = compare_vals(captured_data[i][0],captured_data[i][1],captured_data[j][0],captured_data[j][1])

    indices_to_include = set()
    # print(comparison_arr)
    while len(indices_to_include) <= 7:
        next_min = np.amin(comparison_arr)
        pair = np.unravel_index(np.argmin(comparison_arr),(len(comparison_arr),len(comparison_arr)))
        
        if (next_min > 125):
            break
        pair = sorted(pair)
        comparison_arr[pair[0]][pair[1]] = 10000
        comparison_arr[pair[1]][pair[0]] = 10000

        indices_to_include.add(pair[1])
        indices_to_include.add(pair[0])

    final_images = {}
    print(indices_to_include)
    for elem in indices_to_include:
        target_x = captured_data[elem][2]
        final_images[target_x] = images[target_x]
    
    return final_images

# Crop plate letters out of photo
# args: 
# > img: image to crop letters out of
# returns:
# > dict mapping leftmost x-coordinate of character to image of character
def crop_letters(img):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    if DEBUG:
        cv2.imshow('image',hsv)
        cv2.waitKey(0)
    # define range of black color in HSV to detect letters
    lower_val_1 = np.array([0,120,0]) # reds (for alberta)
    upper_val_1 = np.array([10, 255, 230])

    lower_val_2 = np.array([50,120,0]) # cool colours
    upper_val_2 = np.array([360, 255, 230])

    # Threshold the HSV image to get only black colors
    mask = cv2.inRange(hsv, lower_val_1, upper_val_1)
    mask2 = cv2.inRange(hsv, lower_val_2, upper_val_2)

    mask_final = cv2.bitwise_or(mask, mask2)

    # crop out letters from plate
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(4,4))
    dilated = cv2.morphologyEx(mask_final, cv2.MORPH_CLOSE, kernel)

    if DEBUG:
        cv2.imshow('image',dilated)
        cv2.waitKey(0)

    padding = 6
    contours = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:15]

    collected_rectangles = []
    images = {}
    captured_data = []
    full_img_height = img.shape[0]
    full_img_width = img.shape[1]
    for idx,c in enumerate(contours):
        
        x,y,w,h = cv2.boundingRect(c)

        if (h < (full_img_height*0.125) or w>(full_img_width*0.5) or w > h or h > 200 or h < w*(4/3)): # ensure shape has reasonable proportions
            continue

        x_min = max(x-padding,0)
        y_min = max(y-padding,0)
        x_max = min(x+w+padding,full_img_width)
        y_max = min(y+h+padding,full_img_height)

        y_midpoint = (y_min+y_max)/2.0

        valid = True
        # remove any rectangles from other rectangles
        for cr in collected_rectangles:
            if (x_min >= cr[0][0] and  y_min >= cr[0][1] and x_max <= cr[1][0] and y_max <= cr[1][1]):
                valid = False
                break

        if valid:
            collected_rectangles.append([(x_min, y_min), (x_max, y_max)])
            
            if DEBUG:
                cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

            cropped_img = dilated[y_min:y_max, x_min:x_max]
            cropped_img = process_letter(cropped_img)

            images[x] = cropped_img
            captured_data.append((y_midpoint,h,x))
            if GEN_PHOTOS:
                cv2.imwrite(f"./output/elem_{x}.png",cropped_img)
                
    final_images = remove_outliers(images, captured_data)

    return final_images

# Apply spaces to extracted letters based on how far they are from one another in the photo
# args:
# > keys: keys containing x-coordinates of analyzed images 
# > plate_num: the output plate number without spaces
# returns:
# > New plate number after analysis
def apply_spaces(keys,plate_num):
    prev_left = keys[0]
    space_tracker = []
    space_estimates = []
    for elem in keys[1:]:
        diff = elem-prev_left
        if len(space_estimates) == 0:
            space_estimates.append(diff)
            space_tracker.append(0)
        else:
            done_cat = False
            for i in range(len(space_estimates)):
                q1 = space_estimates[i]*0.5
                q3 = space_estimates[i]*1.5
                if (diff <= q3 and diff >=q1):
                    space_estimates[i] = (space_estimates[i]+diff)/2
                    space_tracker.append(i)
                    done_cat = True
                    break
                elif (diff < q1):
                    space_estimates.insert(i,diff)
                    for j in range(len(space_tracker)):
                        if (space_tracker[j] >=i):
                            space_tracker[j] +=1
                    
                    space_tracker.append(i)
                    done_cat = True
                    break
            if not done_cat:
                space_estimates.append(diff)
                space_tracker.append(len(space_estimates)-1)
            
        prev_left = elem
    spaces_added = 0
    for i in range(len(space_tracker)):
        if (space_tracker[i] >=1):
            plate_num = plate_num[:i+1+spaces_added] + " "*space_tracker[i] + plate_num[i+1+spaces_added:]
            spaces_added += space_tracker[i]
    return plate_num

# Read the plate number from the given image
# args: 
# > the corners used to crop the original image 
# > the image to crop and detect
# > whether or not the function should use the aforementioned corners to skew the image
# > if nonempty, contains the actual value for the plate to compare (for debugging)
# returns:
# > the detected plate number
def perform_read(corners,img,should_skew, should_be):
        img = cv2.resize(img, (600,400) )
        if (should_skew):
            dst = straighten_crop(corners, img)
        else:
            dst= img

        if DEBUG:
            cv2.imshow('image',dst)
            cv2.waitKey(0)

        # crop letters out of photo
        images = crop_letters(dst)


        # sort keys by distance from the left
        keys = sorted(images.keys(), reverse=False)

        if (len(keys) <= 2):
            print(f"only {len(keys)} elements found... not supported")
            print(f"NOTHING PARKED - {datetime.now().time()}")
            with open(filename, "a") as f:
                f.write(f"NOTHING PARKED - {datetime.now().time()}\n")
        else:
            
                
            if DEBUG:
                cv2.imshow('image',dst)
                cv2.waitKey(0)

            recog_imgs = []
            for key in keys:
                recog_imgs.append(images[key])
            plate_num = "000 000"
            # either generate the bin files to perform low-level ML or use python ML to get answer
            if GEN_BIN:
                load_ml.create_bin(recog_imgs)
            else:
                plate_num = load_ml.recog_images(recog_imgs)
                
                should_be = should_be.replace(" ", "")
                if len(should_be) > 0:
                    for i in range(len(plate_num)):
                        try:
                            if should_be[i] != plate_num[i]:
                                cv2.imwrite(f"./output/{should_be[i]}_{plate_num}_{i}_{plate_num[i]}.png",recog_imgs[i])
                        except IndexError:
                            cv2.imwrite(f"./output/{plate_num}_{i}_{plate_num[i]}.png",recog_imgs[i])

                plate_num = apply_spaces(keys, plate_num)

                            

                print(f"\n\n\'{plate_num}\' PARKED - {datetime.now().time()}")


            return plate_num

# Perform a read from the camera every <PHOTO_INTERVAL> seconds and writes results to a file called "log - <DATE>"
def perform_reading_loop():

    filename = f"log - {datetime.today().strftime('%Y-%m-%d')}.txt"
    with open(filename, "w") as f:
        f.write("START:\n")
        
    should_be = ""
    if PROMPT_CHECKER:
        should_be = input("what is the plate number of what you're about to scan?")

    while True:
        img = None
        should_skew = True
        corners,img, should_skew = take_photo()
        if (corners is None):
            break

        plate_num = perform_read(corners,img,should_skew,should_be)

        writing_str = f"{plate_num} PARKED - {datetime.now().time()}\n"
        with open(filename, "a") as f:
            f.write(writing_str)
        time.sleep(PHOTO_INTERVAL)
        
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
    corners, _, should_skew = find_plate(img)

    plate_name = ""
    if PROMPT_CHECKER:
        plate_name = Path(file).name
        plate_name = plate_name[:plate_name.find(".")]
    return perform_read(corners,img,should_skew,plate_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs='?', const="")
    args = parser.parse_args()

    if args.file is None:
        perform_reading_loop()
    else:
        perform_reading_singular(args.file)
