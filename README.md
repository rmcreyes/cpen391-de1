# Summary
OpenCV license plate detection, which uses a neural network to classify characters. The code that runs on the DE1-SoC for our CPEN 391 project.

# Instructions
Run the following commands to install needed packages:
- For base requirements:
    - `pip install -r requirements/requirements.txt`
- To run neural network on python layer - OPTIONAL:
    - `pip install -r requirements/requirements_for_tensorflow.txt` 

To run the code to detect using the camera every few seconds, use:
- `python recognize.py`

If you have a pre-taken photo for detection, use:
- `python recognize.py <path/to/file>`