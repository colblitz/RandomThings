import time
import requests
import urllib
import random
import os
from PIL import Image
from shutil import copyfile

def getFilename(i):
	return "red-storm-{:03d}.jpg".format(i)

downloadFolder = "redstorm/original"
croppedFolder = "redstorm/cropped"
dedupedFolder = "redstorm/deduped"

def checkDirectoryExists(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

checkDirectoryExists(downloadFolder)
checkDirectoryExists(croppedFolder)
checkDirectoryExists(dedupedFolder)

urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

def actuallyDownload(i, url):
	print url
	filename = getFilename(i)
	testfile = urllib.URLopener()
	testfile.retrieve(url, downloadFolder + filename)
	time.sleep(random.random() + 1)

template1 = "https://merakiscans.com/manga/red-storm/{}/01.jpg"
template2 = "https://merakiscans.com/manga/red-storm/{}/001.jpg"

def tryChapter(i):
	try:
		actuallyDownload(i, template1.format(i))
		return
	except Exception as e:
		print e
	try:
		actuallyDownload(i, template2.format(i))
		return
	except Exception as e:
		print e

# https://blog.iconfinder.com/detecting-duplicate-images-using-python-cb240b05a3b6
def dhash(image, hash_size = 8):
	# Grayscale and shrink the image in one step.
	image = image.convert('L').resize(
		(hash_size + 1, hash_size),
		Image.ANTIALIAS,
	)
	pixels = list(image.getdata())
	# Compare adjacent pixels.
	difference = []
	for row in xrange(hash_size):
		for col in xrange(hash_size):
			pixel_left = image.getpixel((col, row))
			pixel_right = image.getpixel((col + 1, row))
			difference.append(pixel_left > pixel_right)
	# Convert the binary array to a hexadecimal string.
	decimal_value = 0
	hex_string = []
	for index, value in enumerate(difference):
		if value:
			decimal_value += 2**(index % 8)
		if (index % 8) == 7:
			hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
			decimal_value = 0
	return ''.join(hex_string)

if __name__ == '__main__':
	if len(os.listdir(downloadFolder)) == 0:
		print "Try to download images"
		for i in range(55, 265):
			tryChapter(i)
	else:
		print "Have images"

	if len(os.listdir(croppedFolder)) == 0:
		print "Crop images"
		crop = (15, 127, 307, 488)
		for filename in os.listdir(downloadFolder):
			if filename.endswith(".jpg"):
				image = Image.open(os.path.join(downloadFolder, filename))
				cropped = image.crop(crop)
				cropped.save(os.path.join(croppedFolder, filename))
				print "Cropped " + filename

	if len(os.listdir(dedupedFolder)) == 0:
		print "Deduping"
		hashes = set()
		for filename in os.listdir(croppedFolder):
			if filename.endswith(".jpg"):
				image = Image.open(os.path.join(croppedFolder, filename))
				imageHash = dhash(image)
				if not imageHash in hashes:
					print "New file:", filename
					copyfile(os.path.join(croppedFolder, filename), os.path.join(dedupedFolder, filename))
					hashes.add(imageHash)

	print "Done"


