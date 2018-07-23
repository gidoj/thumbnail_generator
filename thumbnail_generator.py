# Author: Joseph Gido (2018)
# Note: ONLY FOR USE WITH PYTHON 2
# (Script only grabs photos with .png, .jpg, .jpeg file extensions)
# Usage: thumbnail_generator.py [DIRECTORY] [PAR] [WIDTH] [HEIGHT]
# What: Pull each picture in given directory and reduce to given width and height.
# 		If PAR (preserve aspect ratio):
#			-is 0: keep given width and height unchanged
#			-is 1: use given width to calculate aspect ratio and recalc height
#			-is 2: use given height to calculate aspect ratio and recalc width
# Notes:
# - New width/height is min of given width/height and original photo width/height
# - Reduced image in such a way that not stretched horizontally/vertically from original
#
# Some definitions:
# -> pw = photo width, ph = photo height
# -> gw = given width, pw = given width
# 	*-> note: if pw < gw --> gw = pw; if ph < gh --> gh = ph
# -> w_shrink = pw/gw, h_shrink = ph/gh
# -> min_shrink = min(w_shrink, h_shrink)
# -> w_span = gw * min_shrink, h_span = gh * min_shrink
# -> dx = dy = min_shrink
# -> x0 = (pw - w_span) / 2, y0 = (ph - h_span) / 2
#

import sys, os
import cv2 #for image manipulation
import numpy as np

gw = 0 # given width arg - can be float if par == 3
gh = 0 # given height arg
par = -1 # par (0, 1, 2, or 3)

def print_usage():
	print("Usage: thumbnail_generator.py [FROM] [TO] [PAR] [WIDTH] [HEIGHT]")
	print(">> FROM: directory of images to reduce to thumbnails")
	print(">> TO: directory to place thumbnails")
	print(">> PAR: preserve aspect ratio")
	print(">> --- 0 (don't preserve)")
	print(">> --- 1 (preserve based on given width)")
	print(">> --- 2 (preserve based on given height)")
	print(">> --- 3 (shrink image by factor given in WIDTH argument")
	print(">> WIDTH: new width to reduce to (any number if PAR=2; shrink factor if PAR=3)")
	print(">> HEIGHT: new height to reduce to (any number if PAR=1,3)")


def parse_args():
	if (len(sys.argv)-1 != 5):
		print_usage()
		sys.exit()
	
	from_dir = sys.argv[1] # source directory for photos
	to_dir = sys.argv[2] # directory to place new thumbnails
	par = int(sys.argv[3]) # preserve aspect ratio (0-3)
	width = float(sys.argv[4]) # new potential width (unless PAR=2,3)
	height = int(sys.argv[5]) # new potential height (unless PAR=1,3)

	return ({"from":from_dir, "to":to_dir, "par":par, "w":width, "h":height})


def get_dir_list(directory):
	#Get list of photos in given directory.
	#-only return list containing .png, .jpg, .jpeg
	files = os.listdir(directory)
	images = []
	for file in files:
		parts = file.split(".")
		ext = parts[len(parts)-1].lower() #use len(parts)-1 rather than 1
										  #to account for filenames with '.' > 1
		if (ext == "png" or ext == "jpg" or ext == "jpeg"):
			images.append(file)

	return images


def write_thumbnail(thumbnail, filename, destination):
	path = destination + filename
	cv2.imwrite(path, thumbnail)


def check_par(pw, ph):
	#Check PAR parameter (Preserve Aspect Ratio)
	#-change goal width, height depending on PAR value
	tw = gw #thumbnail width - don't want to change gw
	th = gh #thumbnail height - don't want to change gh
	#change (tw, th) if par nonzero
	if par == 1:
		th = ph * tw / pw
	elif par == 2:
		tw = pw * th / ph
	elif par == 3:
		# in case where par == 3, gw is reduction factor
		tw = int(pw / gw)
		th = int(ph / gw)

	return (tw, th)


def reduce_image(img):
	#Generate new thumbnail for given image.
	ph, pw, _ = img.shape
	tw, th = check_par(pw, ph)
	#account for edge cases
	if pw < tw:
		tw = pw
	if ph < th:
		th = ph
	#define new thumbnail
	thumbnail = np.zeros((th, tw,3), np.uint8)
	#get reduction factors
	w_shrink = 1.0 * pw / tw
	h_shrink = 1.0 * ph / th
	min_shrink = min(w_shrink, h_shrink)
	w_span = tw * min_shrink
	h_span = th * min_shrink
	dx = min_shrink
	dy = min_shrink
	x0 = (pw - w_span) / 2
	y0 = (ph - h_span) / 2
	y = y0
	ty = 0
	while ty < th:
		x = x0
		tx = 0
		while tx < tw:
			pixel = np.zeros(3)
			# pixel = img[int(y), int(x)]
			###average try - delete in between if doesn't work
			total = 0
			cy = int(y - dy/3)
			while cy <= int(y + dy/3):
				cx = int(x - dx/3)
				while cx <= int(x + dx/3):
					if (cy >= 0 and cy < ph and cx >= 0 and cx < pw):
						pixel += img[cy, cx]
						total += 1
					cx += 1
				cy += 1
			pixel /= total
			###end try
			thumbnail[ty, tx] = pixel
			x += dx
			tx += 1
		y += dy
		ty += 1

	return thumbnail


def generate_thumbnails(source, destination):
	images = get_dir_list(source)
	total = len(images)
	count = 0;
	for image in images:
		print ("Reducing image " + str(count+1) + " (of " + str(total) + ")")
		img = cv2.imread(source + image, 1)
		thumbnail = reduce_image(img)
		name = "thumbnail" + str(count) + ".png"
		write_thumbnail(thumbnail, name, destination)
		count += 1;
		

def run():
	global gw, gh, par
	args = parse_args()
	gw = args["w"]
	gh = args["h"]
	par = args["par"]
	#round gw if not using width as reduce factor (par != 3)
	if par < 0 or par > 3:
		print_usage()
		sys.exit()
	if par != 3:
		gw = int(gw);
	generate_thumbnails(args["from"], args["to"])


run()

