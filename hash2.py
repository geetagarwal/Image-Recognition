def average_hash(image, hash_size=8):
	if hash_size < 2:
		raise ValueError("Hash size must be greater than or equal to 2")

	# reduce size and complexity, then covert to grayscale
	image = image.convert("L").resize((hash_size, hash_size), Image.ANTIALIAS)

	# find average pixel value; 'pixels' is an array of the pixel values, ranging from 0 (black) to 255 (white)
	pixels = numpy.asarray(image)
	avg = pixels.mean()

	# create string of bits
	diff = pixels > avg
	# make a hash
	return str(ImageHash(diff))

def phash(image, hash_size=8, highfreq_factor=4):
	if hash_size < 2:
		raise ValueError("Hash size must be greater than or equal to 2")

	import scipy.fftpack
	img_size = hash_size * highfreq_factor
	image = image.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
	pixels = numpy.asarray(image)
	dct = scipy.fftpack.dct(scipy.fftpack.dct(pixels, axis=0), axis=1)
	dctlowfreq = dct[:hash_size, :hash_size]
	med = numpy.median(dctlowfreq)
	diff = dctlowfreq > med
	return str(ImageHash(diff))

def dhash_vertical(image, hash_size=8):
	# resize(w, h), but np.array((h, w))
	image = image.convert("L").resize((hash_size, hash_size + 1), Image.ANTIALIAS)
	pixels = np.asarray(image)
	# compute differences between rows
	diff = pixels[1:, :] > pixels[:-1, :]
	return str(ImageHash(diff))


def whash(image, hash_size = 8, image_scale = None, mode = 'haar', remove_max_haar_ll = True):
	import pywt
	if image_scale is not None:
		assert image_scale & (image_scale - 1) == 0, "image_scale is not power of 2"
	else:
		image_natural_scale = 2**int(np.log2(min(image.size)))
		image_scale = max(image_natural_scale, hash_size)

	ll_max_level = int(np.log2(image_scale))

	level = int(np.log2(hash_size))
	assert hash_size & (hash_size-1) == 0, "hash_size is not power of 2"
	assert level <= ll_max_level, "hash_size in a wrong range"
	dwt_level = ll_max_level - level

	image = image.convert("L").resize((image_scale, image_scale), Image.ANTIALIAS)
	pixels = np.asarray(image) / 255
	hex_string = []
	if remove_max_haar_ll:
		coeffs = pywt.wavedec2(pixels, 'haar', level = ll_max_level)
		coeffs = list(coeffs)
		coeffs[0] *= 0
		pixels = pywt.waverec2(coeffs, 'haar')

	coeffs = pywt.wavedec2(pixels, mode, level = dwt_level)
	#print(coeffs)
	dwt_low = coeffs[0]

	med = np.median(dwt_low)
	diff = dwt_low > med
	return str(ImageHash(diff))
	
# loop over the image dataset
hashes = []
for imagePath in glob.glob(args["dataset"] + "/*"):
    # load the image and compute the difference hash
    image = Image.open(imagePath)
    k = whash(image)
    hashes.append([k,imagePath])
    #print(hashes)

wbhash = [x[0] for x in hashes] # gives the hash for image
path = [x[1] for x in hashes]   # gives the path+filename for the image
#print(wbhash)

#open input image and calculate difference hash
query = Image.open(args["query"])
ohash = whash(query)
print(ohash)

#calculate hamming distance for image
for hashes, path in zip(wbhash, path):
	ham = hamming_distance(ohash,hashes)
	#print(ham)
        # Hamming Distance is zero means duplicate image is detected
	if (ham == 0):
		image = Image.open(path)        
		image.show()
		print("hamming distance is ", ham)
		print(path)
        # hamming distance < 6 gives those images which are almost alike
	elif (ham <6):
		num = 0
		image = Image.open(path)
		image.show()
		print("hamming distance is ", ham)
		print(path)