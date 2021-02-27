OUTPUT_FILENAME = "log_"
GEN_BIN = False # when false, the script will use ML model to read plate
DEBUG = False # when true, intermittent photos will pop up with letter extraction progress
PROMPT_CHECKER = False # whether or not to compare result to given value ahead of time
GEN_PHOTOS = False # whether to always generate letters extracted in output/*
SHOW_CAM_FRAMES = True # whether or not to show camera frames when detecting

USE_WEBCAM_NUMBER = 1 # starts at 0, set to 0 if you only have one webcam connected; I'm just using my secondary webcam
PHOTO_INTERVAL = 15 # number of seconds between shots

# sizes for resized photos 
RESIZE_SIZE = (600,400)
STRAIGHTENED_SIZE = (600,300)

# auto-picture constants
FRAME_COUNT_BETWEEN_DIFFERENCE_SNAPSHOTS = 5
MATRIX_DIFFERENCE_THRESHOLD = 15000000
NUM_LOW_DIFFERENCE_FRAME_COUNT_THRESHOLD = 10
SAME_CORNERS_DETECTED_THRESHOLD = 3