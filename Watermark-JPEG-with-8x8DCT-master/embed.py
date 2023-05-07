import cv2 as cv  
import numpy as np
import math
import walk


def embed(srcs):

	# Change this chunk of code from converting fingerprint
	# image into b&w in numpy array into taking text and
	# converting text into numpy array if possible.
	# read in src image, converted to numpy array (opencv doc.)
	src = cv.imread(srcs)
	src = cv.bitwise_not(src)
	# convert src image into gray scale
	graysrc = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
	# cv.imshow('graysrc',graysrc)
	#中值滤波
	medianblurimg=cv.medianBlur(graysrc, 3)
	# cv.imshow('medianblurimg',medianblurimg)
	# convert grayscale image into b&w based on pixel
	# value above and below 70-> 0/255
	ret, bsrc = cv.threshold(graysrc, 70, 255, 1)
	cv.imshow('source', bsrc)
	# update/save new image to filename
	cv.imwrite('embedfinger.jpg', bsrc, [int(cv.IMWRITE_JPEG_QUALITY), 100])

	# read in host image, converted to numpy array (type(host))
	host = cv.imread('host.jpg')
	# convert host image from RGB to YUV color space
	hostyuv = cv.cvtColor(host, cv.COLOR_RGB2YUV)
	# converting to float32 in necessary for DCT
	hostf = hostyuv.astype('float32')

	# embedding process
	# goal completion chart
	finishwm = hostf
	# 8x8 divided observation map of goal completion
	# It is found that if wmblocks=hostf, then modifying wmblocks is equal
	# to modifying hostf, which means that these two are pointers, and the
	# variables pointing to the image here are all pointers
	wmblocks = np.zeros([hostf.shape[0], hostf.shape[1], 3], np.float32)
	wmblocks[:, :, :]=hostf[:, :, :]
	# The number of rows and columns of a matrix composed of 8x8 blocks
	# as a unit
	part8x8rownum = int(host.shape[0]/8)
	part8x8colnum = int(host.shape[1]/8)
	# Total number of fingerprint pixels
	fingernum = bsrc.shape[0]*bsrc.shape[1]
	# r is the number of fingerprint pixels to be stored in each 8x8 block
	# r=math.ceil(fingernum/(part8x8rownum*part8x8colnum))
	r = math.ceil(fingernum/(part8x8rownum*part8x8colnum))
	print("r=", r)
	# The unit grid in the 8x8 block is in a pair with the symmetrical unit grid in its center.
	# The size relationship of each pair (the former is larger than the latter, and the former
	# is smaller than the latter) is used to record the black and white of the fingerprint pixels to be stored
	# Walk the grid from the middle to the upper right to prepare for the generation of grid pairs
	xydict = walk.findpoint((3, 4, -1), r)
	# Fingerprint Pixel Generator
	fpgij = walk.fpg(bsrc)
	# traverse 8x8 blocks
	count = 0
	flag = 0
	for parti in range(part8x8rownum):
		if (flag):
			break
		for partj in range(part8x8colnum):
			if (flag):
				break
			# 8x8 blocks for DCT
			part8x8 = cv.dct(hostf[8*parti:8*parti+8, 8*partj:8*partj+8, 0])
			# Blocks that are not large enough to be 8x8 are not considered
			if (part8x8.shape[0] < 8) | (part8x8.shape[1] < 8):
				continue
			# Each 8x8dct block stores r fingerprint pixels
			for t in range(r):
				if (flag):
					break
				# Obtain the fingerprint pixels to be stored at this moment through the generator
				i, j = next(fpgij)
				if (i==-1 & j==-1):
					flag = 1
				# Grid coordinates to be used for fingerprint pixels
				rx, ry = xydict[t]
				# Modify the size relationship between r1 and r2 to reflect the black and white
				# situation of watermark pixels
				r1 = part8x8[rx, ry]
				r2 = part8x8[7-rx, 7-ry]  # Centrosymmetric lattice of r1
				detat = abs(r1-r2)
				p=float(detat+0.1)  # Embedding depth
				if bsrc[i, j] == 0:  # 0 black, fingerprint subject, use r1>r2 to record
					if(r1<=r2):  # Make sure r1 is greater than r2
						part8x8[rx, ry] += p
				else:  # 255 white, use r1<r2 to record
					if(r1>=r2):
						part8x8[7-rx, 7-ry] += p
				if not flag:
					count += 1
			# After storing r fingerprint pixels, perform inverse DCT on this 8x8 block
			finishwm[8*parti:8*parti+8, 8*partj:8*partj+8, 0] = cv.idct(part8x8)
			wmblocks[8*parti:8*parti+8, 8*partj:8*partj+8, 0] = finishwm[8*parti:8*parti+8, 8*partj:8*partj+8, 0]
			# To connect with brackets, draw a line for 8x8
			if (wmblocks.shape[0] > 8*parti+7) & (wmblocks.shape[1] > 8*partj+7):
				wmblocks[8*parti:8*parti+8, 8*partj+7, 0] = 100
				wmblocks[8*parti+7, 8*partj:8*partj+8, 0] = 100
	wmrgb = cv.cvtColor(finishwm.astype('uint8'), cv.COLOR_YUV2RGB)
	# line drawing
	cv.imshow('wmblocks', cv.cvtColor(wmblocks.astype('uint8'), cv.COLOR_YUV2RGB))
	cv.waitKey(0)  
	cv.destroyAllWindows()	
	# The quality of image saving, to be 100, the default is 95
	for x in range(6):
		name = "finishwm"+str(x)
		filename = name+".jpg"
		cv.imwrite(filename, wmrgb, [int(cv.IMWRITE_JPEG_QUALITY), 100-x])
		img = cv.imread(filename)
		cv.namedWindow(name, 0)
		k = 480
		cv.resizeWindow(name, k, int(k*img.shape[0]/img.shape[1]))
		cv.imshow(name, img)

	print("countembed=", count)


def main():
	embed('fingerprint.jpg')
	cv.waitKey(0)  
	cv.destroyAllWindows()


if __name__ == '__main__':
	main()
