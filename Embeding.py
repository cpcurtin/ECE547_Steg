import cv2 as cv 
import numpy as np
import os
import math
from generateQMatrix import *
from zigzag import *
from inverse_zigzag import *
from PIL import Image as im
import random
from MessageData import *

def embed(imagePath,message,qf = 85,outname="EncodedImage"):
    messageBank,mLen = generateMessageBank(message)
    count = 0
    count2 = 0
    #Get Image and convert it to YUV format
    img = cv.imread(imagePath)
    if(type(img) != np.ndarray):
        print("Image Not Found")
        return False
    imgyuv = cv.cvtColor(img, cv.COLOR_RGB2YUV)
    imgf = imgyuv.astype('float32')

    cwd = os.getcwd()
    # filename0 = cwd+"\Images\ConvertedToJpg.jpg"
    # imgTem0 = cv.cvtColor(imgf.astype('uint8'), cv.COLOR_YUV2RGB)
    # cv.imwrite(filename0,imgTem0,[int(cv.IMWRITE_JPEG_QUALITY), qf])

    #Convert image to numpy array
    # imgArray = np.asarray(imgf)    
    # print(imgArray.shape)
    Q = generateQMatrix(qf)
    rowNum = int(imgf.shape[0]/8)
    colNum = int(imgf.shape[1]/8)
    #For each 8 by 8 section
    EncodedImage = np.zeros(imgf.shape,int)
    EncodedImage[:,:,:] = imgf[:,:,:]
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
                    #ENCODE DATA HERE
                    lossyImg[i][j] = int(dctImgSeq[i][j]/Q[i][j])
            # print(lossyImg)
            imgDCTZZ = zigzag(lossyImg)
            #imgDCTZZ = zigzag(dctImgSeq)

            dEnd = 64
            for b in range(64):
                if(dEnd == 64):
                    if(imgDCTZZ[63-b] != 0):
                        dEnd = 64 - b 
            if(63-dEnd)>=10:
                for i in range(7):
                    #POS = n+m mod l
                    count = count + 1
                    #TODO Change the data type of the items in imgDCTZZ and messageBank
                    #Want to change the "2" to maybe 1.5? (next 2 line)
                    #1 is exactly the cutoff and the JPEG compression is loosing to much data
                    #2 is not bad but the larger the number the more distortion we introduce
                    #This is what we can change durring testing if we are loosing to much data
                    imgDCTZZ[dEnd+i] = messageBank[(n+m)%mLen][0,i]*2
                imgDCTZZ[dEnd+7] = 2


            imgEncDct = inverse_zigzag(imgDCTZZ)
            for k in range(8):
                for l in range(8):
                    imgEncDct[k][l] = int(imgEncDct[k][l]*Q[k][l])
            imgEncDct = imgEncDct.astype('float32')
            imEncSub = cv.idct(imgEncDct)
            for d in range(8):
                for c in range(8):
                    if(imEncSub[d][c] >= 255):
                        imEncSub[d][c] = 255
                    if(imEncSub[d][c] < 0):
                        imEncSub[d][c] = 0
            EncodedImage[8*n:8*n+8, 8*m:8*m+8, 0] = imEncSub
            EncodedImage[8*n:8*n+8, 8*m:8*m+8, 1] = imgf[8*n:8*n+8, 8*m:8*m+8, 1]
            EncodedImage[8*n:8*n+8, 8*m:8*m+8, 2] = imgf[8*n:8*n+8, 8*m:8*m+8, 2]
            #print(imgDCTZZ)
    wmrgb = cv.cvtColor(EncodedImage.astype('uint8'), cv.COLOR_YUV2RGB)
    
    filename = cwd+"\EncodedImages\{0}.jpg".format(outname)
    cv.imwrite(filename,wmrgb,[int(cv.IMWRITE_JPEG_QUALITY), qf])
    #cv.imwrite(filename,wmblocks,[int(cv.IMWRITE_JPEG_QUALITY), qf])
    print(count)
    print(count2)




if __name__ == '__main__':
    # print(generateQMatrix(80))
    cwd = os.getcwd()
    #File Path Wrong need to be fixed if used
    #embed("C:\DevCode\ECE547_Steg\Images\GSM_TE.jpg","This is a watermarked Image")