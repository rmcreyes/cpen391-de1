import numpy as np
from ctypes import *
import constants

BUF_SIZE = 300

if constants.USE_C:
    x = CDLL(constants.RFS_SO_FILE)

def init_rfs_wifi():
    x.Init_RFS()
    x.initWifi()
    print(x)

def close_wifi():
    x.close_wifi()
    print("closed wifi")

# returns is_occupied, cost 
def update_parking_status(plate, parked):
    x.argtypes = [c_char_p, c_char_p, c_int, c_int]
    x.notify.restype = c_int

    plate_c = plate.encode('utf-8')
    buf = create_string_buffer(BUF_SIZE)
    parked_c = c_int(int(parked))

    x.notify.restype = c_int

    print("about to call notify..")
    n = x.notify(plate_c, buf, c_int(BUF_SIZE), parked_c)
    print("done call to notify..")
    return buf.value.decode("utf-8").strip()[1:-1]

# returns is_user, new_plate, parking_id 
def confirm_wifi(plate, id, correct):
    x.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_int]
    x.confirm_wifi.restype = c_int

    plate_c = plate.encode('utf-8')
    id_c = id.encode('utf-8')
    buf = create_string_buffer(BUF_SIZE)
    correct_c = c_int(int(correct))

    x.confirm_wifi(id_c, plate_c, buf, c_int(BUF_SIZE), correct_c)

    ret = buf.value.decode("utf-8")
    print(ret)
    ret_array = ret.split(",")

    isUser = ret_array[0].strip()
    print("isUser is " + isUser)
    if isUser == "true":
        return True
    else:
        return False

# returns confirm, timeout, plate
def confirm_bluetooth(plate):
    x.argtypes = [c_char_p, c_char_p, c_int]
    x.confirm_BT.restype = c_int

    plate_c = plate.encode('utf-8')
    buf = create_string_buffer(BUF_SIZE)

    print("calling confirm_BT")
    x.confirm_BT(plate_c, buf, c_int(BUF_SIZE))
    print("done calling confirm_BT")

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

# returns nothing
def reset_meter():
    print("resetting meter...")
    x.argtypes = [c_char_p, c_int]
    x.reset_meter.restype = c_int

    buf = create_string_buffer(BUF_SIZE)

    x.reset_meter(buf, c_int(BUF_SIZE))

    return buf.value.decode("utf-8")

# returns nothing
def send_payment(parking_id, card_num, exp, cvv):
    x.argtypes = [c_char_p, c_int]
    x.send_payment.restype = c_int

    parking_id_c = parking_id.encode('utf-8')
    card_num_c = card_num.encode('utf-8')
    exp_c = exp.encode('utf-8')
    cvv_c = cvv.encode('utf-8')

    buf = create_string_buffer(BUF_SIZE)

    x.send_payment(parking_id_c, card_num_c, exp_c, cvv_c, buf, c_int(BUF_SIZE))

    return buf.value.decode("utf-8")

# returns nothing
def ok_done(plate):
    x.argtypes = [c_char_p, c_char_p, c_int]
    x.ok_done.restype = c_int

    plate_c = plate.encode('utf-8')
    buf = create_string_buffer(BUF_SIZE)

    print("about to call..")
    x.ok_done(plate_c, buf, c_int(BUF_SIZE))
    print("returning..")
    return buf.value.decode("utf-8")

# > returns:
# card_num
# exp
# cvv
# timeout
def ok_user(plate, isUser):
    x.argtypes = [c_char_p, c_char_p, c_int, c_int]
    x.ok_user.restype = c_int

    plate_c = plate.encode('utf-8')
    buf = create_string_buffer(BUF_SIZE)
    isUser_c = c_int(int(isUser))

    print("calling ok_user")
    x.ok_user(plate_c, buf, c_int(BUF_SIZE), isUser_c)

    print("returning ok_user")

    ret = buf.value.decode("utf-8")
    ret_array = ret.split(",")
    if len(ret_array) == 1:
        return
    for i in range(len(ret_array)):
        ret_array[i] = ret_array[i].strip()

    if ret_array[1] == "TIMEOUT":
        return "", "", "", True

    return ret_array[1],ret_array[2],ret_array[3], False


def ok_leave():
    x.ok_user.restype = c_int
    x.ok_leave()

# returns:
# - isOccupied
def new_parked(plate):

    # three attempts
    for i in range(3):
        parking_id = update_parking_status(plate, True)
        if not " " in parking_id:
            break

    confirm, timeout, plate = confirm_bluetooth(plate)

    if timeout:
        print("timed out")
        reset_meter()
        return plate

    is_user= confirm_wifi(plate, parking_id, confirm)

    print(is_user)
    if not is_user:
        card_num, exp, cvv, timeout = ok_user(plate, False) 
        if timeout:
            reset_meter()
            return plate

        send_payment(parking_id, card_num, exp, cvv)
    else:
        ok_user(plate, True) 

    ok_done(plate)
    return plate


def leave(plate):
    # is_occupied, cost = update_parking_status(plate, False)
    update_parking_status(plate, False)
    ok_leave()
