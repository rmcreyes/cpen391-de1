import cv2
import imutils
import numpy as np
import argparse
import load_ml
import math


GEN_BIN = False # when false, the script will use ML model to read plate
DEBUG = True
SHOW_CAM_FRAMES = True # TODO: does not work when False, should find a way to take photos without showing preview to reduce CPU usage

USE_WEBCAM_NUMBER = 1 # starts at 0, set to 0 if you only have one webcam connected; I'm just using my secondary webcam

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

def take_photo():
    # run webcam to take photo

    print("press g when you want to take the photo")
    # define a video capture object 
    vid = cv2.VideoCapture(USE_WEBCAM_NUMBER) 
    
    img = None
    frame = None
    while(True): 
        
        # Capture the video frame 
        ret, frame = vid.read() 

        corner_points, marked_img = find_plate(frame)
        if (marked_img is None):
            marked_img = cv2.resize(frame, (600,400) )
            corner_points = [(0,0),(600,0),(600,400),(0,400)]

        # show image with markings in where it found the rectangle
        if SHOW_CAM_FRAMES:
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

    return corner_points, frame

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
    corners = [(0,0),(600,0),(600,400),(0,400)]

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
        if (cv2.contourArea(c) < 400*600/4):
            break #frame should take at least a quarter of the screen
        
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        if len(approx) == 4:
            print(cv2.contourArea(c))
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

            

            break
        

    return corners, marked_img

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
    
    hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)

    # define range of black color in HSV to detect letters
    lower_val = np.array([55,55,55])
    upper_val = np.array([255, 255, 255])

    # Threshold the HSV image to get only black colors
    mask = cv2.inRange(hsv, lower_val, upper_val)
    # crop out 6 letters from plate
    # TODO: make smarter algorithm for sensing letters and numbers

    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
    dilated = cv2.dilate(mask, kernel)


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

        if (h < (img.shape[0]*0.125) or w>(img.shape[1]*0.5)):
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

            cropped_img = mask[y_min:y_max, x_min:x_max]
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


    img = None
    if args.file is None:
        # no arguments, start camera to take a photo
        print("nothing specified.. starting camera")
        corners,img = take_photo()
        if (corners is None):
            quit()
    else:
        # if a photo is passed in, read it in and use it
        img = cv2.imread(args.file,cv2.IMREAD_COLOR)
        corners, _ = find_plate(img)

    img = cv2.resize(img, (600,400) )
    dst = straighten_crop(corners, img)
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
    recog_imgs = []
    for key in keys:
        recog_imgs.append(images[key])

    # either generate the bin files to perform low-level ML or use python ML to get answer
    if GEN_BIN:
        load_ml.create_bin(recog_imgs)
    else:
        plate_num = load_ml.recog_images(recog_imgs)
        print(f"\n\nthe plate number is {plate_num}")