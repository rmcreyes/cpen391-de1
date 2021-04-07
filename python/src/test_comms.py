import c_comm_interfacing_utils
import time
c_comm_interfacing_utils.init_rfs_wifi()
# c_comm_interfacing_utils.ok_leave()
print(c_comm_interfacing_utils.update_parking_status("ABC 123\0",True))
# print(c_comm_interfacing_utils.confirm_bluetooth("ABC 123"))
# print(c_comm_interfacing_utils.ok_user("ABC 123", False))
# print(c_comm_interfacing_utils.ok_done("ABC 123"))

# print("sleep for 3s")
# time.sleep(3)
# print("calling leave")
# print(c_comm_interfacing_utils.ok_leave())
# print("called leave")