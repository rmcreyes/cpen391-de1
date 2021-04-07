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

# returns is_occupied, cost 
def update_parking_status(plate, parked):
    x.argtypes = [c_char_p, c_char_p, c_int, c_int]
    x.confirm_wifi.restype = c_int

    plate_c = plate.encode('utf-8')
    buf = create_string_buffer(BUF_SIZE)
    parked_c = c_int(int(parked))

    x.notify.restype = c_int

    n = x.notify(plate_c, buf, c_int(BUF_SIZE), parked_c)

    return buf.value.decode("utf-8")

# returns is_user, new_plate, parking_id 
def confirm_wifi(plate, id, correct):
    x.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_int]
    x.confirm_wifi.restype = c_int

    plate_c = plate.encode('utf-8')
    id_c = id.encode('utf-8')
    buf = create_string_buffer(BUF_SIZE)
    correct_c = c_int(int(correct))

    x.confirm_wifi(id_c, plate_c, buf, c_int(BUF_SIZE), correct_c)

    return buf.value.decode("utf-8")

# returns confirm, timeout, plate
def confirm_bluetooth(plate):
    x.argtypes = [c_char_p, c_char_p, c_int]
    x.confirm_BT.restype = c_int

    plate_c = plate.encode('utf-8')
    buf = create_string_buffer(BUF_SIZE)

    x.confirm_BT(plate_c, buf, c_int(BUF_SIZE))

    return buf.value.decode("utf-8")

# returns nothing
def reset_meter():
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
    return buf.value.decode("utf-8")


def ok_leave():
    x.ok_user.restype = c_int
    x.ok_leave()

# returns:
# - isOccupied
def new_parked(plate):

    is_user, is_occupied, plate, parking_id = update_parking_status(plate, True)
    confirm, timeout, plate = confirm_bluetooth(plate)

    if timeout:
        reset_meter()
        return False

    is_user, plate, parking_id = confirm_wifi(plate, id, confirm)

    if not is_user:
        card_num, exp, cvv, timeout = ok_user(plate, False) 
        if timeout:
            reset_meter()
            return False

        send_payment(parking_id, card_num, exp, cvv)

    ok_done(plate)
    return True


def leave(plate):
    # is_occupied, cost = update_parking_status(plate, False)
    update_parking_status(plate, False)
    ok_leave()
