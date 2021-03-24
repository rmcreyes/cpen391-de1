OUTPUT_FILENAME_PREFIX = "output/log_"
PHOTO_INTERVAL = 5 # number of seconds between shots

USE_C = False # when false, the script will use ML model to read plate

CREATE_BIN = False # generate a bin file; must also enable USE_C
GEN_EXTRACTED_LETTER_PNG = False # whether to always generate letters extracted in output/*

DEBUG = False # when true, intermittent photos will pop up with letter extraction progress
SAVE_DEBUG = False # whether to save demo photos

PROMPT_CHECKER = True # whether or not to compare result to given value ahead of time
SAVE_ORIGINALS = True # whether or not to save the original photos taken to a directory

# sizes for resized photos 
RESIZE_HEIGHT = 400
STRAIGHTENED_SIZE = (600,300)
FRAME_SIZE = (640,480)

# neural network constants
IN_SIZE = 784
L1_SIZE = 1000
L2_SIZE = 750
L3_SIZE = 36

NN_BIN = 'models/model_hl_1000_750_generated_nn.bin' # neural network weights and biases (bin format)
NN_H5 = "debug_tools/letterrecog1000_750.h5" # neural network weights and biases (h5 format)
SO_FILE = "./src/compiled_c/libnn.so"

# mapping labels to actual character
# 0-9 represents the 0-9 characters
# 10-25 represents A-Z
PREDICT_MAP = ['0','1','2','3','4','5',
            '6','7','8','9','A','B',
            'C','D','E','F','G','H',
            'I','J','K','L','M','N',
            'O','P','Q','R','S','T',
            'U','V','W', 'X','Y','Z']