import cv2

# Apply spaces to extracted letters based on how far they are from one another in the photo
# args:
# > keys: keys containing x-coordinates of analyzed images 
# > plate_num: the output plate number without spaces
# returns:
# > New plate number after analysis
def apply_spaces(keys,plate_num):
    prev_left = keys[0]

    # will track the number of spaces between letters
    space_tracker = []

    # will track the estimated distance in pixels for each space type (distances for no space, distance for 1 space, etc.)
    space_estimates = []

    for elem in keys[1:]:
        diff = elem-prev_left
        if len(space_estimates) == 0:
            space_estimates.append(diff)
            space_tracker.append(0)
        else:
            done_cat = False
            for i in range(len(space_estimates)):
                # first and third quartiles
                q1 = space_estimates[i]*0.5
                q3 = space_estimates[i]*1.5
                if (diff <= q3 and diff >= q1):
                    # add it to average if it fits with a current space width (within q1 and q3)
                    space_estimates[i] = (space_estimates[i]+diff)/2
                    space_tracker.append(i)
                    done_cat = True
                    break
                elif (diff < q1):
                    # area is less than first quartile but passed the last val; insert new value for it
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

    # if too many spaces were added, reduce the spaces in the space tracker
    while (sum(space_tracker)+ len(plate_num) > 8):
        for i in range(len(space_tracker)):
            if (space_tracker[i] >0):
                space_tracker[i] -=1

    # apply spaces from space tracker into string
    for i in range(len(space_tracker)):
        if (space_tracker[i] >=1):
            plate_num = plate_num[:i+1+spaces_added] + " "*space_tracker[i] + plate_num[i+1+spaces_added:]
            spaces_added += space_tracker[i]

    return plate_num
