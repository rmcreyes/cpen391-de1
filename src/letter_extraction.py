import cv2
import constants
import numpy as np
import imutils
import datetime

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

# Remove the most off-linear shapes
# args:
# > x, y, h: midpoint x, midpoint y, and height array values
# > yhat: expected y values based on predetermined slope
# returns:
# > new versions of x, y, h arrays
def remove_furthest(x, y, h, yhat):
    distances = abs(y-yhat)
    max_index = np.argmax(distances)

    x.pop(max_index)
    y.pop(max_index)
    h.pop(max_index)
    return (x, y, h)

# Calculate line of best fit for points and determines yhat (expected y) values
# base code from https://stackoverflow.com/questions/893657/how-do-i-calculate-r-squared-using-python-and-numpy
# args:
# > x, y: x and y arrays with points to base slope off of
# returns:
# > results dict, has yhat array and error sum of squares
def linear_fit(x, y):
    results = {}
    y = [abs(a - 400) for a in y]
    coeffs = np.polyfit(x, y, 1)
    p = np.poly1d(coeffs)

    yhat = p(x)
    results['yhat'] = yhat # expected values
    ybar = np.sum(y)/len(y)     

    if constants.SAVE_DEBUG:
        
        import matplotlib.pyplot as plt 
        e = (y-yhat)
        fig = plt.figure()
        plt.errorbar(x, y, yerr=e, fmt='o', linewidth=0.5)
        plt.plot(x,p(x)) 
        plt.xlim([0, 600])
        plt.ylim([0, 400])
        fig.savefig(f'temp_{len(x)}.png', dpi=fig.dpi)


    sse = np.sum((y-yhat)**2)   
    results['sse'] = sse  # error sum of squares

    return results    

# Remove odd detected shapes from photo
# args:
# > img: dict mapping leftmost x-coordinate of character to image of character
# > x_pts, y_pts, h_pts: data relating x-coordinate,y-coordinate, and height of each image
# returns:
# > new filtered dict mapping leftmosdt x-coordinate of character to image of character with no/less outliers
def remove_outliers(images, x_pts, y_pts, h_pts):

    final_images = {}
    if len(x_pts) == 0:
        return final_images
    # use error of sum of squares to ensure that letters follow linear pattern
    polyfit_obj = linear_fit(x_pts, y_pts)
    sse = abs(polyfit_obj["sse"])**0.5

    while sse > 35:
        yhat = polyfit_obj["yhat"]
        x_pts, y_pts,h_pts = remove_furthest(x_pts, y_pts, h_pts, yhat)
        polyfit_obj = linear_fit(x_pts, y_pts)
        sse = abs(polyfit_obj["sse"])**0.5
    
    # remove outliers from heights
    indices_to_remove = set()
    for i, h in enumerate(h_pts):
        if abs(h_pts[i] - np.mean(h_pts)) > 2.25*np.std(h_pts):
            indices_to_remove.add(i)

    for i,x in enumerate(x_pts):
        if (not i in indices_to_remove):
            final_images[x] = images[x]

    return final_images

# Crop plate letters out of photo
# args: 
# > img: image to crop letters out of
# returns:
# > dict mapping leftmost x-coordinate of character to image of character
def crop_letters(img):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    if constants.DEBUG:
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

    if constants.DEBUG:
        cv2.imshow('image',dilated)
        cv2.waitKey(0)

    padding = 6
    contours = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:15]

    collected_rectangles = []
    images = {}
    y_vals = {}

    full_img_height = img.shape[0]
    full_img_width = img.shape[1]
    x_pts = []
    y_pts = []
    h_pts = []
    for idx,c in enumerate(contours):
        
        x,y,w,h = cv2.boundingRect(c)

        if (h < (full_img_height*0.125) or w>(full_img_width*0.5) or w > h or h > 200 or h < w*(4/3)): # ensure shape has reasonable proportions
            continue

        x_min = max(x-padding,0)
        y_min = max(y-padding,0)
        x_max = min(x+w+padding,full_img_width)
        y_max = min(y+h+padding,full_img_height)

        

        valid = True
        # remove any rectangles from other rectangles
        for cr in collected_rectangles:
            if (x_min >= cr[0][0] and  y_min >= cr[0][1] and x_max <= cr[1][0] and y_max <= cr[1][1]):
                valid = False
                break

        if valid:
            y_midpoint = int((y_min+y_max)/2.0)
            x_midpoint = int((x_min+x_max)/2.0)

            y_pts.append(y_midpoint)
            x_pts.append(x_midpoint)
            h_pts.append(h)

            img = cv2.circle(img, (x_midpoint,y_midpoint), radius=0, color=(0, 0, 255), thickness=4)
            collected_rectangles.append([(x_min, y_min), (x_max, y_max)])
            
            if constants.DEBUG:
                cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

            cropped_img = dilated[y_min:y_max, x_min:x_max]
            cropped_img = process_letter(cropped_img)

            images[x_midpoint] = cropped_img
            y_vals[x_midpoint] = y_midpoint
            if constants.GEN_PHOTOS:
                cv2.imwrite(f"./output/elem_{x}.png",cropped_img)
                
    final_images = remove_outliers(images, x_pts, y_pts, h_pts)

    for k in final_images.keys():
        img = cv2.circle(img, (k,y_vals[k]), radius=0, color=(0, 255, 0), thickness=5)
        if constants.SAVE_DEBUG:
            cv2.imwrite("./debug_img.png",img)

    return final_images
