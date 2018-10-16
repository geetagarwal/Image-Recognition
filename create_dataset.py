# This code be run with command:
# python create_database.py --input faces1 --output dataset

from PIL import Image
import os, os.path
import argparse
import random
import shutil
import glob2
import uuid
import shutil
from shutil import copyfile

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required = True ,
help = "input directory of images")
ap.add_argument("-o", "--output", required = True ,
help = "output directory")

args = vars(ap.parse_args())

#finding image in the given folder
for imagePath in glob2.iglob(args["input"] + "/**/*.jpg"):
	filename = str(uuid.uuid4()) + ".jpg"
	shutil.copy(imagePath ,os.path.abspath(args["output"] + "/" + filename))
	numTimes = random.randint(1, 8)
	for i in range(0, numTimes):
		image = Image.open(imagePath)
		#changing the size of the image randomly
		factor = random.uniform(0.90, 1.05)
		width = int(image.size[0] * factor)
		ratio = width / float(image.size[0])
		height = int(image.size[1] * ratio)
		image = image.resize((width , height),1)

		#saving the image with random name
		adjFilename = str(uuid.uuid4()) + ".jpg"
		image = image.save (args["output"] + "/" + adjFilename)