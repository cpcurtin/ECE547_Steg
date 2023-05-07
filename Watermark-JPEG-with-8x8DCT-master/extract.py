import cv2 as cv  
import numpy as np  
import math
import walk


def extract(src,dst):
	wmrgb = cv.imread(src)
	wmyuv = cv.cvtColor(wmrgb, cv.COLOR_RGB2YUV)
	wmf = wmyuv.astype('float32')
	part8x8rownum = int(wmf.shape[0]/8)
	part8x8colnum = int(wmf.shape[1]/8)
	# Temporarily guess the largest square watermark image size
	# from r and the host image
	r = 5
	fingernum = 230
	extractxydict = walk.findpoint((3, 4, -1), r)
	# Max empty vector to restore watermark
	finishfinger = np.zeros([fingernum, fingernum, 3], np.uint8)
	i, j = 0, 0
	count = 0
	flag = 0
	for parti in range(part8x8rownum):
		for partj in range(part8x8colnum):
			# Blocks that are not large enough to be 8x8 are not considered
			part8x8 = cv.dct(wmf[8*parti:8*parti+8, 8*partj:8*partj+8, 0])
			if (part8x8.shape[0] < 8) | (part8x8.shape[1] < 8):
				continue
			# Each 8x8dct block stores r fingerprint pixels
			for t in range(r):
				if (i==fingernum):
					break
				# The grid coordinates where the fingerprint pixels should be
				rx, ry = extractxydict[t]
				# Observe the size relationship between r1 and r2, and get the
				# black and white situation of watermark pixels
				r1 = part8x8[rx, ry]
				r2 = part8x8[7-rx, 7-ry]  # Centrosymmetric lattice of r1
				if r1 > r2:
					finishfinger[i, j] = 0  # black
				else:
					if r1 < r2:
						finishfinger[i, j] = 255  # white
				j += 1
				if (j==fingernum):
					j = 0
					i = i+1
				count += 1
	print("countextract=", count)
	cv.imwrite(dst, finishfinger, [int(cv.IMWRITE_JPEG_QUALITY), 100])


def main():
	for x in range(6):
		wmname = "finishwm"+str(x)
		exname = str(x)+"extractfinger"
		extract(wmname+".jpg", exname+".jpg")
		img = cv.imread(exname+".jpg")
		cv.namedWindow(exname, 0)
		k = 240
		cv.resizeWindow(exname, k, int(k*img.shape[0]/img.shape[1]))
		cv.imshow(exname, img)


if __name__ == '__main__':
	main()
	cv.waitKey(0)  
	cv.destroyAllWindows()