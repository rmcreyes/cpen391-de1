import numpy as np
from ctypes import *
import constants

if constants.USE_C:
    x = CDLL(constants.RFS_SO_FILE)

# initialize the RFS card and WiFi module
def init_rfs_wifi():
    x.Init_RFS()
    x.initWifi()

# close the Wifi module (must be always called at the 
# end of the program if WiFi module is initialized)
def close_wifi():
    x.close_wifi()
    print("closed wifi")

# tell the server to begin the parking process for a car 
# or begin a leaving process for a car
# args:
# > a string with the plate number
# > whether they just parked or have left (true if parked, false if left)
# returns:
# > a string with the parkingID for this session
def update_parking_status(plate, parked):
    x.argtypes = [c_char_p, c_char_p, c_int, c_int]
    x.notify.restype = c_int

    plate_c = plate.encode('utf-8')
    buf = create_string_buffer(constants.COMM_BUF_SIZE)
    parked_c = c_int(int(parked))

    x.notify.restype = c_int

    print("about to call notify..")
    n = x.notify(plate_c, buf, c_int(constants.COMM_BUF_SIZE), parked_c)
    print("done call to notify..")

    return buf.value.decode("utf-8").strip()[1:-1]

# confirm the plate number with the server
# args:
# > a string with the plate number
# > a string with the parkingID for this session
# > whether or not the plate has changed from 
#   original update_parking_status() call
# returns:
# > whether or not the plate is registered under a user
def confirm_wifi(plate, id, correct):
    x.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_int]
    x.confirm_wifi.restype = c_int

    plate_c = plate.encode('utf-8')
    id_c = id.encode('utf-8')
    buf = create_string_buffer(constants.COMM_BUF_SIZE)
    correct_c = c_int(int(correct))

    x.confirm_wifi(id_c, plate_c, buf, c_int(constants.COMM_BUF_SIZE), correct_c)

    ret = buf.value.decode("utf-8")
    ret_array = ret.split(",")

    isUser = ret_array[0].strip()
    if isUser == "true":
        print("Plate belongs to a user.")
        return True
    else:
        print("Plate does not belong to a user.")
        return False

# Confirm the scanned plate number with the user on the hardware app
# args:
# > a string with the plate number
# returns:
# > whether or not the user has corrected the plate number to something different
# > whether or not a timeout occurred
# > the revised plate number (may be the same as the original)
def confirm_bluetooth(plate):
    x.argtypes = [c_char_p, c_char_p, c_int]
    x.confirm_BT.restype = c_int

    plate_c = plate.encode('utf-8')
    buf = create_string_buffer(constants.COMM_BUF_SIZE)

    x.confirm_BT(plate_c, buf, c_int(constants.COMM_BUF_SIZE))

    ret = buf.value.decode("utf-8")
    ret_array = ret.split(",")

    for i in range(len(ret_array)):
        ret_array[i] = ret_array[i].strip()

    confirm_str = ret_array[1]

    if confirm_str == "TIMEOUT":
        return False, True, ""
    else:
        if confirm_str == "TRUE":
            confirm = True
        else:
            confirm = False
        return confirm, False, ret_array[2]

# reset the meter since a timeout has occurred
def reset_meter():
    print("resetting meter...")
    x.argtypes = [c_char_p, c_int]

    buf = create_string_buffer(constants.COMM_BUF_SIZE)

    x.reset_meter(buf, c_int(constants.COMM_BUF_SIZE))

# send payment information to the server
# args:
# > a string with the parkingID for this session
# > the credit card number
# > the credit card expiry date
# > the credit card CVV
def send_payment(parking_id, card_num, exp, cvv):
    x.argtypes = [c_char_p, c_int]

    parking_id_c = parking_id.encode('utf-8')
    card_num_c = card_num.encode('utf-8')
    exp_c = exp.encode('utf-8')
    cvv_c = cvv.encode('utf-8')

    buf = create_string_buffer(constants.COMM_BUF_SIZE)

    x.send_payment(parking_id_c, card_num_c, exp_c, cvv_c, buf, c_int(constants.COMM_BUF_SIZE))

# Tell the hardware app that it can proceed to begin the parking timer
# args
# > a string with the plate number
def ok_done(plate):
    x.argtypes = [c_char_p, c_char_p, c_int]

    plate_c = plate.encode('utf-8')
    buf = create_string_buffer(constants.COMM_BUF_SIZE)

    x.ok_done(plate_c, buf, c_int(constants.COMM_BUF_SIZE))

# prompt the hardware app to do one of the following:
# - prompt the user for payment info if the plate number is not linked to an account
# OR
# - go straight to begin parking if the plate number is linked to an account
# args:
# > a string with the plate number
# > whether or not the plate is registered under a user.
# returns:
# > the credit card number (if applicable)
# > the credit card expiry date (if applicable)
# > the credit card CVV (if applicable)
# > whether or not the hardware app timed out
def ok_user(plate, isUser):
    x.argtypes = [c_char_p, c_char_p, c_int, c_int]
    x.ok_user.restype = c_int

    plate_c = plate.encode('utf-8')
    buf = create_string_buffer(constants.COMM_BUF_SIZE)
    isUser_c = c_int(int(isUser))

    x.ok_user(plate_c, buf, c_int(constants.COMM_BUF_SIZE), isUser_c)

    ret = buf.value.decode("utf-8")
    ret_array = ret.split(",")
    if len(ret_array) == 1:
        return
    for i in range(len(ret_array)):
        ret_array[i] = ret_array[i].strip()

    if ret_array[1] == "TIMEOUT":
        return "", "", "", True

    return ret_array[1],ret_array[2],ret_array[3], False

# tell the hardware app to quit its current session
def ok_leave():
    x.ok_user.restype = c_int
    x.ok_leave()

# the main function called by the main loop that 
# runs through the communication process that occurs when a car parks
# returns:
# > the new plate number if re-entered by user
def new_parked(plate):

    # three attempts to notify
    for i in range(3):
        parking_id = update_parking_status(plate, True)
        if not " " in parking_id:
            break

    confirm, timeout, plate = confirm_bluetooth(plate)

    if timeout:
        reset_meter()
        return plate

    is_user= confirm_wifi(plate, parking_id, confirm)

     # card information be will be non-blank only if is_user is false
    card_num, exp, cvv, timeout = ok_user(plate, is_user)

    if not is_user:
        if timeout:
            reset_meter()
            return plate

        send_payment(parking_id, card_num, exp, cvv)
        ok_done(plate)

    return plate


# the function called by the main loop that 
# runs through the communication process that occurs when a car leaves
def leave(plate):
    update_parking_status(plate, False)
    ok_leave()
