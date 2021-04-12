import c_comm_interfacing_utils
import time

# simple communication script that parks and leaves 3 seconds after entering the information

# initialize wifi and rfs
c_comm_interfacing_utils.init_rfs_wifi()

# park
c_comm_interfacing_utils.new_parked("ABCABC")

# leave after 3 seconds
print("sleep for 3s")
time.sleep(3)
c_comm_interfacing_utils.leave("ABCABC")
print("called leave")

# close wifi
c_comm_interfacing_utils.close_wifi()