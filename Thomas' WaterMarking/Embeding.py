import cv2 as cv 
import numpy as np
import os
import math
from generateQMatrix import *
from zigzag import *
from inverse_zigzag import *
from PIL import Image as im

def embed(imagePath,message,qf = 85):
    #Get Image and convert it to YUV format
    img = cv.imread(imagePath)
    imgyuv = cv.cvtColor(img, cv.COLOR_RGB2YUV)
    imgf = imgyuv.astype('float32')
    cwd = os.getcwd()
    filename0 = cwd+"\Thomas' WaterMarking\Images\ConvertedToJpg.jpg"
    imgTem0 = cv.cvtColor(imgf.astype('uint8'), cv.COLOR_YUV2RGB)
    cv.imwrite(filename0,imgTem0,[int(cv.IMWRITE_JPEG_QUALITY), qf])

    #Convert image to numpy array
    # imgArray = np.asarray(imgf)    
    # print(imgArray.shape)
    Q = generateQMatrix(qf)
    rowNum = int(imgf.shape[0]/8)
    colNum = int(imgf.shape[1]/8)
    #For each 8 by 8 section
    EncodedImage = np.zeros(imgf.shape,int)
    for n in range(rowNum):
        for m in range(colNum):
            #Compute DCT
            start = imgf[8*n:8*n+8, 8*m:8*m+8, 0]
            dctImgSeq = cv.dct(start)
            lossyImg = np.zeros((8,8),dtype=int)
            # print(dctImgSeq)
            #LOSSY division by Q matrix (elemtwise)
            for i in range(8):
                for j in range(8):
                    lossyImg[i][j] = int(dctImgSeq[i][j]/Q[i][j])
            # print(lossyImg)
            imgDCTZZ = zigzag(lossyImg)
            #imgDCTZZ = zigzag(dctImgSeq)


            #ENCODE HERE in imgDCTZZ



            imgEncDct = inverse_zigzag(imgDCTZZ)
            for k in range(8):
                for l in range(8):
                    imgEncDct[k][l] = int(imgEncDct[k][l]*Q[k][l])
            imgEncDct = imgEncDct.astype('float32')
            imEncSub = cv.idct(imgEncDct)
            EncodedImage[8*n:8*n+8, 8*m:8*m+8, 0] = imEncSub
            EncodedImage[8*n:8*n+8, 8*m:8*m+8, 1] = imgf[8*n:8*n+8, 8*m:8*m+8, 1]
            EncodedImage[8*n:8*n+8, 8*m:8*m+8, 2] = imgf[8*n:8*n+8, 8*m:8*m+8, 2]
            
            #print(imgDCTZZ)
    wmrgb = cv.cvtColor(EncodedImage.astype('uint8'), cv.COLOR_YUV2RGB)
    
    filename = cwd+"\Thomas' WaterMarking\Images\EncodedImage.jpg"
    cv.imwrite(filename,wmrgb,[int(cv.IMWRITE_JPEG_QUALITY), qf])




if __name__ == '__main__':
    # print(generateQMatrix(80))
    cwd = os.getcwd()
    embed(cwd+"\Thomas' WaterMarking\Images\CrowGSM.jpg","Thomas' Image")