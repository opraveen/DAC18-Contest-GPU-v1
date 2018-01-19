## This program is for DAC HDC contest ######
## 2017/11/22
## xxu8@nd.edu
## University of Notre Dame

import procfunc
import math
import numpy as np
import time
#### !!!! you can import any package needed for your program ######

if __name__ == "__main__":
    ############### configurations for dir #################################################################################
    ## Folder structure:
    ## $DAC$|
    ##    |images   (all the test images are stored in this folder)
    ##    |results-$teamName$|
    ##            |time
    ##            |xml

    ## !!!! Please specify your team name here
    teamName = 'RandomSearch'
    ## !!!! please specify the dir here, and please put all the images for test in the folder "images".
    ## Important! You can specify the folder in your local test. But for the sumission, DAC folder is fixed as follows
    #DAC = '/home/DACSDC_GPU' ## uncomment this line when submitting your code
    DAC = '/home/nvidia/DAC/DAC18-Contest-GPU-v1'
    # DAC = 'D:/DAC-dataset/test'
    [imgDir, resultDir, timeDir, xmlDir, myXmlDir, allTimeFile] = procfunc.setupDir(DAC, teamName)

    ############### processing for object detection and tracking ###########################################################
    ### load all the images names
    [allImageName, imageNum] = procfunc.getImageNames(imgDir)
    ### process all the images in batch
    batchNumDiskToDram = 5 ## the # of images read from disk to DRAM in one time
    batchNumDramToGPU  = 3 ## the # of images read from DRAM to GPU in one time for batch processing on the GPU
    imageReadTime = int(math.ceil(imageNum/batchNumDiskToDram))
    imageProcTimeEachRead = int(math.ceil(batchNumDiskToDram/batchNumDramToGPU))
    resultRectangle = np.zeros((imageNum, 4)) ## store all the results about tracking accuracy

    time_start=time.time()

    for i in range(imageReadTime):
        ImageDramBatch = procfunc.readImagesBatch(imgDir,allImageName, imageNum, i, batchNumDiskToDram)
        for j in range(imageProcTimeEachRead):
            start = j*batchNumDramToGPU
            end = start + batchNumDramToGPU
            if end > len(ImageDramBatch):
                end = len(ImageDramBatch)
                if end < start:
                    break
            inputImageData = ImageDramBatch[start:end, :,:,:]
            ############ !!!!!!!!!! your detection and tracking code, please revise the function: detectionAndTracking() !!!!!!!############
            resultRectangle[i * batchNumDiskToDram + start:i * batchNumDiskToDram + end, :] = procfunc.detectionAndTracking(inputImageData, end-start)
    time_end = time.time()
    resultRunTime = time_end-time_start

    print (myXmlDir)
    ############### write results (write time to allTimeFile and detection results to xml) #################################
    procfunc.storeResultsToXML(resultRectangle, allImageName, myXmlDir)
    procfunc.write(imageNum,resultRunTime,teamName, allTimeFile)
