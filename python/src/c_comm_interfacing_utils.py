import numpy as np
from ctypes import *
import constants

BUF_SIZE = 300

if constants.USE_C:
    x = CDLL(constants.RFS_SO_FILE)

def init_rfs_wifi():
    x.Init_RS323.restype = c_int
    x.Init_Wifi.restype = c_int

    init_rfs = x.Init_RS323()
    init_wifi = x.Init_Wifi()
    return init_rfs and init_wifi

def begin_park(plate):
    x.argtypes = [c_char_p, c_char_p, c_int, c_int]
    x.confirm_wifi.restype = c_int

    plate_c = plate.encode('utf-8')
    buf = create_string_buffer(BUF_SIZE)

    x.notify.restype = c_int

    x.notify(plate_c, buf, c_int(BUF_SIZE), c_int(1))

    return buf.value.decode("utf-8")

def confirm_wifi(plate, id, correct):
    x.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_int]
    x.confirm_wifi.restype = c_int

    plate_c = plate.encode('utf-8')
    id_c = id.encode('utf-8')
    buf = create_string_buffer(BUF_SIZE)
    correct_c = c_int(int(correct))

    x.confirm_wifi(id_c, plate_c, buf, c_int(BUF_SIZE), correct_c)

    return buf.value.decode("utf-8")

def confirm_bluetooth(plate):
    x.argtypes = [c_char_p, c_char_p, c_int]
    x.confirm_BT.restype = c_int

    plate_c = plate.encode('utf-8')
    buf = create_string_buffer(BUF_SIZE)

    x.confirm_BT(plate_c, buf, c_int(BUF_SIZE))

    return buf.value.decode("utf-8")

def reset_meter():
    x.argtypes = [c_char_p, c_int]
    x.reset_meter.restype = c_int

    buf = create_string_buffer(BUF_SIZE)

    x.reset_meter(buf, c_int(BUF_SIZE))

    return buf.value.decode("utf-8")


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


def ok_user(plate, isUser):
    x.argtypes = [c_char_p, c_char_p, c_int, c_int]
    x.ok_done.restype = c_int

    plate_c = plate.encode('utf-8')
    buf = create_string_buffer(BUF_SIZE)
    isUser_c = c_int(int(correct))

    x.ok_done(plate_c, buf, c_int(BUF_SIZE), isUser_c)

    return buf.value.decode("utf-8")