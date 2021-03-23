import sys
sys.path.append("./src")
from recognize import *
import os
import constants

# # PURPOSE:
# Testing accuracy of multiple images at once. For testing and debugging purposes.
# # HOW TO USE:
# 1. Create a folder and add you license plate images. Name the images after the value on the plate, including the spaces.
# For example, the photo of the plate "ABC 123" would be called "ABC 123.jpg". 
# 2. Call this function using `python test_samples.py <DIRNAME>`.
# 3. Results should be writted to `TEST - <DATE>`.

if __name__ == "__main__":
    constants.DEBUG = False
    constants.SAVE_ORIGINALS = False
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs='?', const="")
    args = parser.parse_args()

    testfilename = f"output/TEST - {datetime.today().strftime('%Y-%m-%d')}.txt"
    with open(testfilename, "w") as f:
        f.write("START:\n")
    passednum = 0
    letters = set()
    dirname = args.file
    for filename in os.listdir(dirname):
        print(f"\nlooking at {dirname}{filename}")
        result = perform_reading_singular(f"{dirname}{filename}")
        str_label = filename[0:filename.find(".")]
        for s in str_label:
            letters.add(s)
        if (not result == str_label):
            with open(testfilename, "a") as f:
                f.write(f"GOT \'{result}\' BUT EXPECTED {str_label}\n")
        else:
            passednum+=1
    with open(testfilename, "a") as f:
        f.write(f"DONE - {passednum}/{len(os.listdir(dirname))} passed\n")
    
    # print(f"Tested using the following letters: {sorted(letters)}")