from Embeding import *
from evaluate import *
import os 
import pandas as pd
import openpyxl
from Retrieve import *

skipEncode = True
message = "@ThomasGreeley5432"
cwd = os.getcwd()
imageNames = os.listdir(cwd+"\ImageToEncode")
if(not skipEncode):
    for image in imageNames:
        print("Started Embeding: "+image)
        embed("{0}\ImageToEncode\{1}".format(cwd,image),message,75,image[0:-4]+"E")
        print("Finished embeding "+image)
    print("All Embeding Finished")
psnrD = []
mseD = []
message = []
rate = []
if(False):
    for imageEval in imageNames:
        original = "{0}\ImageToEncode\{1}".format(cwd,imageEval)
        encoded = "{0}\EncodedImages\{1}.jpg".format(cwd,imageEval[0:-4]+"E")
        print("Image Name: "+imageEval)
        psnrO , mseO = psnr(original, encoded)
        message0, rate0 = Retrieve(encoded,75)
        message.append(message0)
        rate.append(rate0)
        psnrD.append(psnrO)
        mseD.append(mseO)
    d = {'File Name':imageNames, 'PSNR': psnrD, 'MSE': mseD, 'Rate': rate, 'message':message}
    df = pd.DataFrame(data=d)
    df.to_excel('DataPSNR.xlsx', sheet_name='PSNR')
if(True):
    cwd = os.getcwd()
    TwitterimageNames = os.listdir(cwd+"\Tempimages")
    rate2 = []
    message2 = []
    for image0 in TwitterimageNames:
        encoded = "{0}\Tempimages\{1}".format(cwd,image0)
        message0, rate0 = Retrieve(encoded,75)
        rate2.append(rate0)
        message2.append(message0)
    d = {'Rate': rate2, 'message':message2}
    df = pd.DataFrame(data=d)
    df.to_excel('DataTwitter.xlsx', sheet_name='Rate')