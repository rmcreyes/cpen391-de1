import c_comm_interfacing_utils
import time



c_comm_interfacing_utils.init_rfs_wifi()

print(c_comm_interfacing_utils.new_parked("ABCABC"))
print("sleep for 3s")
time.sleep(3)
c_comm_interfacing_utils.leave("ABCABC")
print("called leave")



# print(c_comm_interfacing_utils.update_parking_status("444 333",True))
# print(c_comm_interfacing_utils.confirm_wifi("444333", "606d5578a9572e001cfae9fb", True))
# print(c_comm_interfacing_utils.send_payment("606d5654a9572e001cfaea00", "1232342342344","12/31","126"))
# print(c_comm_interfacing_utils.leave("444333"))
# print(c_comm_interfacing_utils.reset_meter())


# print(c_comm_interfacing_utils.confirm_bluetooth("ABC 123"))
# print(c_comm_interfacing_utils.ok_user("ABC 123", False))
# print(c_comm_interfacing_utils.ok_done("ABC 123"))

# print("sleep for 3s")
# time.sleep(3)
# print("calling leave")
# print(c_comm_interfacing_utils.ok_leave())
# print("called leave")

c_comm_interfacing_utils.close_wifi()