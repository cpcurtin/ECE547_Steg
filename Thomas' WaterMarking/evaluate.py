import cv2 as cv  
import numpy as np  
import math
import os


def psnr(src, dst):
	im1 = cv.imread(src)
	im2 = cv.imread(dst)
	# mean square error
	mse = np.mean((im2 - im1)**2)
	sqrtmse = math.sqrt(mse)
	# psnr
	psnr = 20*math.log10(255/sqrtmse)
	print("PSNR: "+str(psnr))
	print("MSE: "+str(mse))
	return psnr


def main():
	src = 'embedfinger.jpg'
	for x in range(6):
		name = str(x)+"extractfinger"+".jpg"
		print(x, "PSNR =", '%.3f' % psnr(src, name))
	cv.waitKey(0)  
	cv.destroyAllWindows()


if __name__ == '__main__':
	cwd = os.getcwd()
	imgEnc = cwd+"\Thomas' WaterMarking\Images\EncodedImage.jpg"
	img = cwd+"\Thomas' WaterMarking\Images\GSM_TE.jpg"
	psnr(img,imgEnc)
