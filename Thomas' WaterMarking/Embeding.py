import cv2 as cv 
import numpy as np
import os
import math
from generateQMatrix import *
from zigzag import *
from inverse_zigzag import *
from PIL import Image as im
import random

def embed(imagePath,message,qf = 85):
    count = 0
    count2 = 0
    #Get Image and convert it to YUV format
    img = cv.imread(imagePath)
    imgyuv = cv.cvtColor(img, cv.COLOR_RGB2YUV)
    imgf = imgyuv.astype('float32')

    wmblocks = np.zeros([imgf.shape[0], imgf.shape[1], 3], np.float32)
    wmblocks[:, :, :]=imgf[:, :, :]

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

            dEnd = 64
            for b in range(64):
                if(dEnd == 64):
                    if(imgDCTZZ[63-b] != 0):
                        dEnd = 64 - b 
            if(63-dEnd)>=30:
                for i in range(7):
                    count = count + 1
                    imgDCTZZ[dEnd+i] = random.randint(0,1)


            imgEncDct = inverse_zigzag(imgDCTZZ)
            for k in range(8):
                for l in range(8):
                    imgEncDct[k][l] = int(imgEncDct[k][l]*Q[k][l])
            imgEncDct = imgEncDct.astype('float32')
            imEncSub = cv.idct(imgEncDct)
            for d in range(8):
                for c in range(8):
                    if(imEncSub[d][c] >= 255):
                        count2=count2+1
                        imEncSub[d][c] = 255
                    if(imEncSub[d][c] < 0):
                        count2=count2+1
                        imEncSub[d][c] = 0
            EncodedImage[8*n:8*n+8, 8*m:8*m+8, 0] = imEncSub
            EncodedImage[8*n:8*n+8, 8*m:8*m+8, 1] = imgf[8*n:8*n+8, 8*m:8*m+8, 1]
            EncodedImage[8*n:8*n+8, 8*m:8*m+8, 2] = imgf[8*n:8*n+8, 8*m:8*m+8, 2]
            wmblocks[8*n:8*n+8, 8*m:8*m+8, 0] = EncodedImage[8*n:8*n+8, 8*m:8*m+8, 0]
            wmblocks[8*n:8*n+8, 8*m:8*m+8, 1] = imgf[8*n:8*n+8, 8*m:8*m+8, 1]
            wmblocks[8*n:8*n+8, 8*m:8*m+8, 2] = imgf[8*n:8*n+8, 8*m:8*m+8, 2]
            if (wmblocks.shape[0] > 8*n+7) & (wmblocks.shape[1] > 8*m+7):
                wmblocks[8*n:8*n+8, 8*m+7, 0] = 100
                wmblocks[8*n+7, 8*m:8*m+8, 0] = 100
            #print(imgDCTZZ)
    wmrgb = cv.cvtColor(EncodedImage.astype('uint8'), cv.COLOR_YUV2RGB)
    wmblocks = cv.cvtColor(wmblocks.astype('uint8'), cv.COLOR_YUV2RGB)
    
    filename = cwd+"\Thomas' WaterMarking\Images\EncodedImage.jpg"
    cv.imwrite(filename,wmrgb,[int(cv.IMWRITE_JPEG_QUALITY), qf])
    filename = cwd+"\Thomas' WaterMarking\Images\EncodedImageEDITED.jpg"
    cv.imwrite(filename,wmblocks,[int(cv.IMWRITE_JPEG_QUALITY), qf])
    print(count)
    print(count2)




if __name__ == '__main__':
    # print(generateQMatrix(80))
    cwd = os.getcwd()
    embed(cwd+"\Thomas' WaterMarking\Images\CrowGSM.jpg","Thomas' Image")