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

def Retrieve(imagePath,qf = 85):
    wrongData = 0
    retrevedData = 0
    correctData = 0

    #Get Image and convert it to YUV format
    img = cv.imread(imagePath)
    if(type(img) != np.ndarray):
        print("Image Not Found")
        return False
    imgyuv = cv.cvtColor(img, cv.COLOR_RGB2YUV)
    imgf = imgyuv.astype('float32')

    wmblocks = np.zeros([imgf.shape[0], imgf.shape[1], 3], np.float32)
    wmblocks[:, :, :]=imgf[:, :, :]

    cwd = os.getcwd()
    # filename0 = cwd+"\Thomas' WaterMarking\Images\ConvertedToJpg.jpg"
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
    DataMatrix = np.zeros((rowNum,colNum),str)
    nOff = 0
    mOff = 0
    nPoint = []
    mPoint = []
    nPcount = 20
    offSet = False
    for i in range(nPcount):
        nPoint.append(random.randint(0,rowNum))
        mPoint.append(random.randint(0,colNum))
    for n0 in range(8):
        for m0 in range(8):
            if(not offSet):
                dataSucess = 0
                for i in range(nPcount):
                    dctSample0 = cv.dct(imgf[8*nPoint[i]+n0:8*nPoint[i]+8+n0, 8*mPoint[i]+m0:8*mPoint[i]+8+m0, 0])
                    lossyImg0 = np.zeros((8,8),dtype=int)
                    for i in range(8):
                        for j in range(8):
                            lossyImg0[i][j] = int(dctSample0[i][j]/Q[i][j])
                    imgDCTZZ0 = zigzag(lossyImg0)
                    dEnd0 = 64
                    for b in range(64):
                        if(dEnd0 == 64):
                            if(imgDCTZZ0[63-b] != 0):
                                dEnd0 = 64 - b 
                    l0 = []
                    if dEnd0 > 8:
                        for i in imgDCTZZ0[dEnd0 - 8:dEnd0-1]:
                            if(i>0):
                                l0.append(1)
                            else:
                                l0.append(0)
                        if verify(l0):
                            datHex0 = hex(int(''.join(str(e) for e in l0[0:4]),2))
                            if(datHex0 != '0x0'):
                                dataSucess += 1
                if(dataSucess > 4):
                    nOff = n0
                    mOff = m0
                    offSet = True
                    break
    if(not offSet):
        print("COUNT NOT FIND ENOUGH DATA Try again")
        return False           
    for n in range(rowNum-1):
        for m in range(colNum-1):
            #Compute DCT
            start = imgf[8*n+nOff:8*n+8+nOff, 8*m+mOff:8*m+8+mOff, 0]
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

            # HERE!!! is where changes need to be made
            # imgDCTZZ variable is an array of length 64 that has our data
            # imgDCTZZ = [Image Data, OUR DATA(7bits),1(Identifier for data),0,0,....,0 ]
            #TODO put breaks to cancel process when we dont find enough data
            #TODO BIG ISSUE data is not seen if we crop the image and dct matrix is shifted (Thomas Can explain)
            #In the for loop I work backward from the end of the array
            #until I find the identifier
            dEnd = 64
            for b in range(64):
                if(dEnd == 64):
                    if(imgDCTZZ[63-b] != 0):
                        dEnd = 64 - b 
            l = []
            #if statement prevents array size issues if its false we already
            #lost the data in that cell
            if dEnd > 8:
                for i in imgDCTZZ[dEnd - 8:dEnd-1]:
                    #for the 7 bits of OUR DATA if there is any number we consider that a 1
                    # if there is nothing we consider it a 0
                    if(i>0):
                        l.append(1)
                    else:
                        l.append(0)
                #The verify function takes OUR DATA and checks that there were not any bit errors. 
                #It can always detect 2 bit errors (3 bit errors could look like another message sometimes)
                #It only detects the bit errors NO CORRECTION
                if verify(l):
                    #We have good data here we need to start organizing it,
                    #We cant even garente that one sequence is always correct so we need to
                    #somehow keep track of when we cant retreve the data in a sequence.
                    #the data (should be) organized so going right or down will give the next data point
                    #idk if this will help
                    retrevedData = retrevedData + 1
                    datHex = hex(int(''.join(str(e) for e in l[0:4]),2))
                    DataMatrix[n,m] = datHex[2]
                else:
                    wrongData = wrongData + 1
                #
    if(retrevedData < 50):
        print("Not Enough Data")
        return False
    dataStart = []
    for n1 in range(rowNum-1):
        for m1 in range(colNum-1):
            if(DataMatrix[n1,m1] == 'f')&(DataMatrix[n1+1,m1] == 'f')&(DataMatrix[n1,m1+1] == 'f'): 
                dataStart.append(m1+n1)
    if(len(dataStart) < 2):
        print("No Message Detected")
        return False
    min1 = min(dataStart)
    dataStart2 = [i for i in dataStart if i != min1]
    min2 = min(dataStart2)
    Length = min2 - min1   
    #NEED TO IMPROVE THIS pick the most optimal Length that works for the dataStart array
    messDist = [dict() for x in range(Length)]
    for n2 in range(rowNum):
        for m2 in range(colNum):
            d =  DataMatrix[n2,m2]
            le = (n2 + m2)%Length
            if(messDist[le].get(d) == None):
                messDist[le][d] = 1
            else:
                messDist[le][d] += 1
    messHex = [''] * Length
    for dictI in range(Length):
        diction = messDist[dictI]
        correctData += max(diction.values())
        messHex[dictI]=max(diction, key=diction.get)       
    messHex2 = ''.join(messHex[2:])
    encodedMessage = bytearray.fromhex(messHex2).decode('utf-8')
    totalData = wrongData + retrevedData
    lostData = totalData - correctData
    print("Number of corupted 8x8 cells: "+str(lostData))
    print("Number of correct 8x8 cells: "+str(correctData))
    rate = 100*correctData/totalData
    print("rate of correct data: "+str(rate)+"%")
    #Data Rate of ~99%
    return encodedMessage




if __name__ == '__main__':
    # print(generateQMatrix(80))
    cwd = os.getcwd()
    mess = Retrieve(cwd+"\Thomas' WaterMarking\Images\TwitterEncodedDownload.jpg")
    print("Water marked Message: "+str(mess))