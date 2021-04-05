# the following constants may be machine-dependent

USE_WEBCAM_NUMBER = 0 # starts at 0, set to 0 if you only have one webcam connected; I'm just using my secondary webcam

# auto-picture constants
FRAME_COUNT_BETWEEN_DIFFERENCE_SNAPSHOTS = 5
MATRIX_DIFFERENCE_THRESHOLD = 30000000
NUM_LOW_DIFFERENCE_FRAME_COUNT_THRESHOLD = 10
SAME_CORNERS_DETECTED_THRESHOLD = 3

# whether or not to perform edge detection (takes a considerable amount of computing time on DE1)
FIND_EDGES = False

SHOW_CAM_FRAMES = True # whether or not to show camera frames when detecting