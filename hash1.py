#IMAGE HASHING ALGORITHMS- AVERAGE HASH, PERCEPTUAL HASH, DIFFRENCE HASH, WAVELET HASH

#To compile this script through command prompt –
#python hash.py --dataset dataset --query brain/87.jpg

from __future__ import (absolute_import, division, print_function)
from PIL import Image
import os.path
import imagehash
import argparse
import glob
import numpy as np
import matplotlib.pyplot as plt
import uuid

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
    help = "path to input dataset of images")
ap.add_argument("-q", "--query", required = True,
       help = "path to the query image")
args = vars(ap.parse_args())

def _binary_array_to_hex(arr):
	bit_string = ''.join(str(b) for b in 1 * arr.flatten())
	width = int(np.ceil(len(bit_string)/4))
	return '{:0>{width}x}'.format(int(bit_string, 2), width=width)

def hex_to_hash(hexstr):
	hash_size = int(np.sqrt(len(hexstr)*4))
	binary_array = '{:0>{width}b}'.format(int(hexstr, 16), width = hash_size * hash_size)
	bit_rows = [binary_array[i:i+hash_size] for i in range(0, len(binary_array), hash_size)]
	hash_array = np.array([[bool(int(d)) for d in row] for row in bit_rows])
	return ImageHash(hash_array)

def old_hex_to_hash(hexstr, hash_size=8):
	l = []
	count = hash_size * (hash_size // 4)
	if len(hexstr) != count:
		emsg = 'Expected hex string size of {}.'
		raise ValueError(emsg.format(count))
	for i in range(count // 2):
		h = hexstr[i*2:i*2+2]
		v = int("0x" + h, 16)
		l.append([v & 2**i > 0 for i in range(8)])
	return ImageHash(np.array(l))

# string1 and string2 should be the same length.
def hamming_distance(string1, string2): 
    # Start with a distance of zero, and count up
    distance = 0
    # Loop over the indices of the string
    L = len(string1)
    for i in range(L):
        # Add 1 to the distance if these two characters are not equal
        if string1[i] != string2[i]:
            distance += 1
    # Return the final count of differences
    return distance



