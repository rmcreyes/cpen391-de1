import cv2
import imutils
import numpy as np
import argparse
import load_ml
import math
import time
from datetime import datetime

filename = "log_"
GEN_BIN = False # when false, the script will use ML model to read plate
DEBUG = False
SHOW_CAM_FRAMES = True # TODO: does not work when False, should find a way to take photos without showing preview to reduce CPU usage

USE_WEBCAM_NUMBER = 1 # starts at 0, set to 0 if you only have one webcam connected; I'm just using my secondary webcam
PHOTO_INTERVAL = 30 
def separate_sides(subarray, index):
    # get the indices of either the top corners or right corners
    # 0 - top corners ; 1 - right corners

    target_indices = []
    max_value = float('-inf')
    max_index = 0
    for idx,a in enumerate(subarray):
        if (a[index] > max_value):
            max_index = idx
            max_value = a[index]
        
    target_indices.append(max_index)

    max_value = float('-inf')
    for idx,a in enumerate(subarray):
        if (a[index] > max_value) and (idx not in target_indices):
            max_index = idx
            max_value = a[index]

    target_indices.append(max_index)


    return target_indices

def within_range(elem1, elem2, count):
    return (elem1 < elem2 + count and elem1 > elem2 - count)



def take_photo():
    # run webcam to take photo

    print("taking background photo")

    print("press g when you want to take the photo")
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
                

        if (frame_nums_without_detection > 20):
            break



        # show image with markings in where it found the rectangle
        if SHOW_CAM_FRAMES:
            # frame_diff = cv2.absdiff(background_frame,frame)
            
            # gray = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY) 
            # gray = cv2.bilateralFilter(gray, 13, 15, 15) 

            # ret, image = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
            # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(20,20))
            # mask = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

            # result = cv2.bitwise_and(frame, frame, mask=mask)
            # cv2.imshow('frame', result) 
            # frame = result
            cv2.imshow('frame', marked_img) 

        # press g to take photo
        if cv2.waitKey(1) & 0xFF == ord('g'): 
            break
            
        # press q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
    # After the loop release the cap object 
    vid.release() 
    # Destroy all the windows 
    cv2.destroyAllWindows() 

    return corner_points, frame, should_skew

def distance_between_points(p2, p1):
    return (((p2[0] - p1[0])**2)+((p2[1] - p1[1])**2))**0.5

def find_angle_between(p1, p2, p3):
    l3= distance_between_points(p2, p1)
    l1= distance_between_points(p3, p2)
    l2= distance_between_points(p1, p3)
    try:
        angle = (math.acos((l1+l3-l2)/(2*l3*l2))*180.0)/math.pi
    except ValueError:
        angle=0
    return angle

def reorder_vertex_array(subarray):
    # reorder the array of vertices to prepare to a re-skewing of image

    topleft_index = 0
    topright_index = 0
    bottomleft_index = 0
    bottomright_index = 0

    top_indices = []
    bottom_indices = []

    top_indices = separate_sides(subarray, 1)
    right_indices = separate_sides(subarray, 0)

    for idx in range(len(subarray)):
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


    subarray_rearranged = [subarray[i] for i in [bottomleft_index, bottomright_index,topright_index, topleft_index]]


    return subarray_rearranged


def straighten_crop(subarray_rearranged, img):

    pts_before = np.float32([subarray_rearranged])
    pts_after = np.float32([[0,0],[600,0],[600,300],[0,300]])
    perspective_transform = cv2.getPerspectiveTransform(pts_before,pts_after)
    dst = cv2.warpPerspective(img,perspective_transform,(600,300))
    return dst

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


    # if DEBUG:
    #     cv2.imshow('image',dilated)
    #     cv2.waitKey(0)

    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:15]
    dst = None
    marked_img = None
    # iterate through candidates
    for c in contours:

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        if (cv2.contourArea(c) < 400*600/4):
            break #frame should take at least a quarter of the screen
        # else:
        #     marked_img = img.copy()
        #     cv2.drawContours(marked_img,[approx], -1, (0, 255, 0), 2)

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


def process_letter(img):
    # make the letter formatted well for the ml model
    blur = cv2.blur(img,(10,10))
    max_dimen = max(img.shape[0],img.shape[1])
    vert_border = int((max_dimen-img.shape[0])/2)
    hori_border = int((max_dimen-img.shape[1])/2)
    image = cv2.copyMakeBorder(blur, vert_border, vert_border, hori_border, hori_border, cv2.BORDER_CONSTANT) 
    image = cv2.resize(image, (28,28) )
    return image

def crop_letters(img):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    if DEBUG:
        cv2.imshow('image',hsv)
        cv2.waitKey(0)
    # define range of black color in HSV to detect letters
    lower_val_1 = np.array([0,140,0]) # reds (for alberta)
    upper_val_1 = np.array([10, 255, 200])

    lower_val_2 = np.array([40,140,0]) # cool colours
    upper_val_2 = np.array([360, 255, 200])

    # Threshold the HSV image to get only black colors
    mask = cv2.inRange(hsv, lower_val_1, upper_val_1)
    mask2 = cv2.inRange(hsv, lower_val_2, upper_val_2)

    mask_final = cv2.bitwise_or(mask, mask2)

    # crop out 6 letters from plate
    # TODO: make smarter algorithm for sensing letters and numbers

    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(4,4))
    dilated = cv2.morphologyEx(mask_final, cv2.MORPH_CLOSE, kernel)

    if DEBUG:
        cv2.imshow('image',dilated)
        cv2.waitKey(0)

    padding = 6
    contours = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]

    elem_num = 0
    collected_rectangles = []
    images = {}
    for idx,c in enumerate(contours):
        
        x,y,w,h = cv2.boundingRect(c)

        if (h < (img.shape[0]*0.125) or w>(img.shape[1]*0.5) or w > h or h > 200 or h < w*(4/3)): # can't have height larger than half of the original image
            continue

        x_min = max(x-padding,0)
        y_min = max(y-padding,0)
        x_max = min(x+w+padding,img.shape[1])
        y_max = min(y+h+padding,img.shape[0])

        valid = True
        # remove any rectangles from other rectangles
        for cr in collected_rectangles:
            if (x_min >= cr[0][0] and  y_min >= cr[0][1] and x_max <= cr[1][0] and y_max <= cr[1][1]):
                valid = False
                break

        if valid:
            elem_num+=1
            collected_rectangles.append([(x_min, y_min), (x_max, y_max)])
            
            if DEBUG:
                cv2.rectangle(dst, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

            cropped_img = dilated[y_min:y_max, x_min:x_max]
            cropped_img = process_letter(cropped_img)

            images[x] = cropped_img
            
            if DEBUG:
                cv2.imwrite(f"./output/elem_{x}.png",cropped_img)

            if (elem_num == 6):
                break
    return images

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs='?', const="")
    args = parser.parse_args()

    filename = f"log - {datetime.today().strftime('%Y-%m-%d')}"
    with open(filename, "w") as f:
        f.write("START:\n")

    done = False
    while not done:
        img = None
        should_skew = True
        if args.file is None:
            # no arguments, start camera to take a photo
            print("nothing specified.. starting camera")
            corners,img, should_skew = take_photo()
            if (corners is None):
                quit()
        else:
            # if a photo is passed in, read it in and use it
            img = cv2.imread(args.file,cv2.IMREAD_COLOR)
            corners, _, should_skew = find_plate(img)
            done = True

        img = cv2.resize(img, (600,400) )
        if (should_skew):
            dst = straighten_crop(corners, img)
        else:
            dst= img
        if (dst is None):
            dst = img

        if DEBUG:
            cv2.imshow('image',dst)
            cv2.waitKey(0)

        # crop letters out of photo
        images = crop_letters(dst)

        if DEBUG:
            cv2.imshow('image',dst)
            cv2.waitKey(0)

        # sort keys by distance from the left
        keys = sorted(images.keys(), reverse=False)

        if (len(keys) <= 2):
            print(f"only {len(keys)} elements found... not supported")
            print(f"NOTHING PARKED - {datetime.now().time()}")
            with open(filename, "a") as f:
                f.write(f"NOTHING PARKED - {datetime.now().time()}\n")
        else:
            recog_imgs = []
            for key in keys:
                recog_imgs.append(images[key])
            plate_num = "000 000"
            # either generate the bin files to perform low-level ML or use python ML to get answer
            if GEN_BIN:
                load_ml.create_bin(recog_imgs)
            else:
                plate_num = load_ml.recog_images(recog_imgs)
                print(f"\n\n{plate_num} PARKED - {datetime.now().time()}")

            with open(filename, "a") as f:
                f.write((f"{plate_num} PARKED - {datetime.now().time()}\n"))
        time.sleep(PHOTO_INTERVAL)