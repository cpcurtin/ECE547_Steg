from Embeding import *
from evaluate import *
import os 
import pandas as pd
import openpyxl

skipEncode = True
message = "@tgreelz"
cwd = os.getcwd()
imageNames = os.listdir(cwd+"\Thomas' WaterMarking\ImageToEncode")
if(not skipEncode):
    for image in imageNames:
        print("Started Embeding: "+image)
        embed("{0}\Thomas' WaterMarking\ImageToEncode\{1}".format(cwd,image),message,85,image[0:-4]+"E")
        print("Finished embeding "+image)
    print("All Embeding Finished")
psnrD = []
mseD = []
for imageEval in imageNames:
    original = "{0}\Thomas' WaterMarking\ImageToEncode\{1}".format(cwd,imageEval)
    encoded = "{0}\Thomas' WaterMarking\EncodedImages\{1}.jpg".format(cwd,imageEval[0:-4]+"E")
    print("Image Name: "+imageEval)
    psnrO , mseO = psnr(original, encoded)
    psnrD.append(psnrO)
    mseD.append(mseO)
d = {'PSNR': psnrD, 'MSE': mseD}
df = pd.DataFrame(data=d)
df.to_excel('DataPSNR.xlsx', sheet_name='PSNR')