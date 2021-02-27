import sys
sys.path.append("./src")
from recognize import *
import os

# # PURPOSE:
# Testing accuracy of multiple images at once. For testing and debugging purposes.
# # HOW TO USE:
# 1. Create a folder and add you license plate images. Name the images after the value on the plate, including the spaces.
# For example, the photo of the plate "ABC 123" would be called "ABC 123.jpg". 
# 2. Call this function using `python test_samples.py <DIRNAME>`.
# 3. Results should be writted to `TEST - <DATE>`.

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs='?', const="")
    args = parser.parse_args()

    testfilename = f"TEST - {datetime.today().strftime('%Y-%m-%d')}.txt"
    with open(testfilename, "w") as f:
        f.write("START:\n")

    dirname = args.file
    for filename in os.listdir(dirname):
        print(f"looking at {dirname}{filename}")
        result = perform_reading_singular(f"{dirname}{filename}")
        str_label = filename[0:filename.find(".")]

        str_result = "FAIL"
        if (result == str_label):
            str_result = "PASS"

        with open(testfilename, "a") as f:
            f.write(f"\'{str_result}\' -- GOT \'{result}\' AND EXPECTED {str_label}\n")