#db.shelve
#To run this code use following in command prompt:
# python dbshelve.py --dataset dataset --shelve db.shelve

from PIL import Image
import imagehash
import argparse
import shelve
import glob

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True ,
help = "path to input dataset of images")
ap.add_argument("-s", "--shelve", required = True ,
help = "output shelve database")
args = vars(ap.parse_args())

# open the shelve database
db = shelve.open(args["shelve"], writeback = True )
# loop over the image dataset
for imagePath in glob.glob(args["dataset"] + "/*.jpg"):
#compute the difference hash
	image = Image.open(imagePath)
	h = str(imagehash.whash(image))
	print(h)

 #Save the hash as the key and filename
	filename = imagePath[imagePath.rfind("/") + 1:]
	db[h] = db.get(h, []) + [filename]
	print(db[h])
 # close the shelf database
db.close()