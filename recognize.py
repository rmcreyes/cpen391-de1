import cv2
import imutils
import numpy as np
import argparse
import load_ml


GEN_BIN = False # when false, the script will use ML model to read plate
DEBUG = True
SHOW_CAM_FRAMES = True

USE_WEBCAM_NUMBER = 1 # starts at 0, set to 0 if you only have one webcam connected; I'm just using my secondary webcam

def separate_sides(subarray, index):

    top_indices = []
    max_value = float('-inf')
    max_index = 0
    for idx,a in enumerate(subarray):
        if (a[index] > max_value):
            max_index = idx
            max_value = a[index]
        
    top_indices.append(max_index)

    max_value = float('-inf')
    for idx,a in enumerate(subarray):
        if (a[index] > max_value) and (idx not in top_indices):
            max_index = idx
            max_value = a[index]

    top_indices.append(max_index)


    return top_indices

def take_photo():
    print("press g when you want to take the photo")
    # define a video capture object 
    vid = cv2.VideoCapture(USE_WEBCAM_NUMBER) 
    
    img = None
    frame = None
    while(True): 
        
        # Capture the video frame 
        ret, frame = vid.read() 

        img, marked_img = find_plate(frame)
        if (marked_img is None):
            marked_img = cv2.resize(frame, (600,400) )
            img = marked_img

        # Display the resulting frame 
        if SHOW_CAM_FRAMES:
            cv2.imshow('frame', marked_img) 
        
        if cv2.waitKey(1) & 0xFF == ord('g'): 
            break
            
        # the 'q' button is set as the 
        # quitting button you may use any 
        # desired button of your choice 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
  
    # After the loop release the cap object 
    vid.release() 
    # Destroy all the windows 
    cv2.destroyAllWindows() 

    return img, cv2.resize(frame, (600,400) )

def find_plate(img):
    img = cv2.resize(img, (600,400) )

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    gray = cv2.bilateralFilter(gray, 13, 15, 15) 

    edged = cv2.Canny(gray, 20, 200) 

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
    dilated = cv2.dilate(edged, kernel)

    contours = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = imutils.grab_contours(contours)


    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:15]
    screenCnt = None
    dst = None
    marked_img = None
    for c in contours:
        
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        if len(approx) == 4:

            screenCnt = approx
            marked_img = img.copy()
            cv2.drawContours(marked_img,[approx], -1, (255, 0, 0), 2)


            subarray = []
            for a in approx:
                subarray.append(a[0])
            
            #####
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

            ##
            
            #####
            subarray_rearranged = [subarray[i] for i in [bottomleft_index,bottomright_index,topleft_index,topright_index]]
            pts1 = np.float32([subarray_rearranged])
            pts2 = np.float32([[0,0],[600,0],[0,300],[600,300]])
            M = cv2.getPerspectiveTransform(pts1,pts2)
            dst = cv2.warpPerspective(img,M,(600,300))



            break
    return dst, marked_img

def process_letter(img):
    blur = cv2.blur(cropped_img,(10,10))
    max_dimen = max(img.shape[0],img.shape[1])
    vert_border = int((max_dimen-img.shape[0])/2)
    hori_border = int((max_dimen-img.shape[1])/2)
    image = cv2.copyMakeBorder(blur, vert_border, vert_border, hori_border, hori_border, cv2.BORDER_CONSTANT) 
    image = cv2.resize(image, (28,28) )
    return image

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs='?', const="")
    args = parser.parse_args()


    img = None
    if args.file is None:
        print("nothing specified.. starting camera")
        dst,img = take_photo()
        if (dst is None):
            quit()
    else:
        img = cv2.imread(args.file,cv2.IMREAD_COLOR)
        dst, _ = find_plate(img)
        img = cv2.resize(img, (600,400) )

    if (dst is None):
        dst = img

    if DEBUG:
        cv2.imshow('image',dst)
        cv2.waitKey(0)

    hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)

    if DEBUG:
        cv2.imshow('image',hsv)
        cv2.waitKey(0)

    # define range of black color in HSV to detect letters
    lower_val = np.array([55,55,55])
    upper_val = np.array([255, 255, 255])

    # Threshold the HSV image to get only black colors
    mask = cv2.inRange(hsv, lower_val, upper_val)

    if DEBUG:
        cv2.imshow('image',mask)
        cv2.waitKey(0)


    padding = 6
    contours = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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

    if DEBUG:
        cv2.imshow('image',dst)
        cv2.waitKey(0)

    keys = sorted(images.keys(), reverse=False)
    recog_imgs = []
    for key in keys:
        recog_imgs.append(images[key])

    if GEN_BIN:
        load_ml.create_bin(recog_imgs)
    else:
        plate_num = load_ml.recog_images(recog_imgs)
        print(f"\n\nthe plate number is {plate_num}")