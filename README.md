# Lego Mask Scanner

An AI image recognition program which can recognize different lego masks and returns the part number for the identified part

## What's inside this repo

* blender_render.py - A script that must be run inside blender's python text editor which can only work by getting blender's BPY (Blender-Python) extension. This script takes STL files from the results directory and renders them into png files which are placed into the test_output directory. The file contains camera, lighting, and scaling settings as well as an optional function to only render STL files from the results directory that are white listed in the whitelist_parts.txt file

* lego_scanner.py - The AI model which takes in an image (under image_path) and (through the power of the CONVOLUTIONAL NEURAL NETWORK) attempts to identify it. The script will take the images from the test_data directory to build training and validation sets which are put in the train_val_split directory. The model makes its prediction in the console after 6 epochs. (There are some test images to try the script with in test_images directory)

* ldview_convert.py - Takes all ldraw/.dat files in a given directory and converts them into STL files. You must have ldview installed on your machine in order for this to work. I have included the ldraw files that I was able to snag from Stud.IO in the ldraw_collection directory

## Future Improvements

* There are many un-utilized stl files which could be fed into the blender_render.py file to generate data which would allow the model to recognize more parts. There are a few issues that would need to be addressed first such as scaling the camera with the STL's size to avoid parts being too big or too small and finding more optimal camera angles for different models.

* Currently the AI model is a convolutional neural network which is only capable of recognizing one object at a time. Ideally this will be replaced with a "multi-class object detector" style AI model which can reduce the amount of time needed to recognize several legos at once. 

* The data is labeled with there corresponding bricklink part number (some data files are of parts which aren't sold on bricklink). Adding a way to take the parts recognized by the AI model and connect them to a user's bricklink account could unlock the connection between AI model and inventory management.