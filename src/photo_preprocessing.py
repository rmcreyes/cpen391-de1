import cv2
import constants
import imutils
import math
import numpy as np

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
    vid = cv2.VideoCapture(constants.USE_WEBCAM_NUMBER,cv2.CAP_DSHOW) 

    vid.set(cv2.CAP_PROP_FRAME_WIDTH, int(640))
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, int(480))

    img = None
    frame = None
    should_skew = True
    last_frame = None
    frame_nums_without_detection = 0
    frame_num_count = 0
    prev_corners = []
    consec_detect = 0
    while(True): 

        if frame_num_count > constants.FRAME_COUNT_BETWEEN_DIFFERENCE_SNAPSHOTS:
            if last_frame is not None:
                frame_diff = cv2.absdiff(last_frame,frame)
                print(frame_nums_without_detection)
                if (frame_diff.sum() < constants.MATRIX_DIFFERENCE_THRESHOLD):
                    frame_nums_without_detection += 1
                else:
                    frame_nums_without_detection = 0

            frame_num_count = 0
            last_frame = frame
        else:
            frame_num_count+=1

        # Capture the video frame 
        ret, frame = vid.read() 
        if (frame is not None):
            resize_width = int(constants.RESIZE_SIZE[1]/frame.shape[0]*frame.shape[1])
            constants.RESIZE_SIZE = (resize_width, constants.RESIZE_SIZE[1])

        corner_points, marked_img, should_skew = find_plate(frame)

        if (marked_img is None):

            marked_img = cv2.resize(frame, constants.RESIZE_SIZE )        # capture 480 by 640 photo for consistency 
            # if (marked_img is not None and (marked_img.shape[0] > constants.FRAME_SIZE[1]  or marked_img.shape[1] > constants.FRAME_SIZE[0])):
            #     center_x_offset = int(constants.FRAME_SIZE[0]/2)
            #     center_y_offset = int(constants.FRAME_SIZE[1]/2)
            #     y_midpoint = int(marked_img.shape[0]/2)
            #     x_midpoint = int(marked_img.shape[1]/2)
            #     marked_img = marked_img[y_midpoint-center_y_offset:y_midpoint+center_y_offset,x_midpoint-center_x_offset:x_midpoint+center_x_offset]

            cv2.imwrite("./debug_img.png",marked_img)
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

                    if (constants.SAME_CORNERS_DETECTED_THRESHOLD == 3):
                        break
                else:
                    consec_detect = 0
                    prev_corners = []
            else:
                consec_detect=1
                prev_corners = corner_points
                

        if (frame_nums_without_detection > constants.NUM_LOW_DIFFERENCE_FRAME_COUNT_THRESHOLD):
            break

        # show image with markings in where it found the rectangle
        if constants.SHOW_CAM_FRAMES:
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
    size_x = constants.STRAIGHTENED_SIZE[0]
    size_y = constants.STRAIGHTENED_SIZE[1]
    pts_after = np.float32([[0,0],[size_x,0],[size_x,size_y],[0,size_y]])
    perspective_transform = cv2.getPerspectiveTransform(pts_before,pts_after)
    dst = cv2.warpPerspective(img,perspective_transform,constants.STRAIGHTENED_SIZE)
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
    img = cv2.resize(img, constants.RESIZE_SIZE  )
    corners = []
    proportions_changed = False


    if not constants.FIND_EDGES:
        return corners, None, proportions_changed

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    gray = cv2.bilateralFilter(gray, 13, 15, 15) 

    edged = cv2.Canny(gray, 20, 200) 

    if constants.SAVE_DEBUG:
        cv2.imwrite("canny_after.png",edged)
        cv2.imwrite("canny_before.png",img)

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
        if (cv2.contourArea(c) < constants.RESIZE_SIZE[0]*constants.RESIZE_SIZE[1]/4):
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
