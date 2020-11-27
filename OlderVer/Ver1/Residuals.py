# IMUToSound.py
import h5py
import math
import numpy as np


def velToFreq3(vel,counter=1):

    highLimit = 1567.98
    lowLimit = 103.8262
    num=1.016
    freqhNumTemp = 440 * num ** (vel/5)
    freqhNumTemp=round(freqhNumTemp)
    freqhNum = np.clip(freqhNumTemp, lowLimit, highLimit)
    #print(vel,freqhNumTemp)
    return freqhNum

def velToFreq2(vel,counter=1):

    pitchStart = 640
    highLimit = 1567.98
    lowLimit = 103.8262
    #pitchNum = pitchStart
    #endValue = 1000
    #semitone = 1.0595465
    C0 = 16.35160
    semitone = 17.32391 / 16.35160
    x = np.arange(1, 80, 1)
    velY = C0 * semitone ** x
    notesFreq = velY[velY > 100]
    velX = (np.arange(-125, 115, 5))
    if counter == 1:
        counter = 0
        pitchVelround = roundup5(vel)
        pitchVelround = np.clip(pitchVelround, -120, 110)
        # pitchNumTemp = ((pitchVelround + 300) ** semitone)
        freqNumTemp = notesFreq[velX == pitchVelround]
        #print(vel,pitchVelround,freqNumTemp)
    freqhNumTemp = np.clip(freqNumTemp, lowLimit, highLimit)
    # print(pitchNumTemp)
    freqNum = freqhNumTemp
    return freqNum

def velToFreq(vel):
    # frequencies range is between highLimit and lowLimit
    highLimit = 1567.98
    lowLimit = 103.8262
    Clid0 = 16.35160
    semitone = 17.32391 / 16.35160
    x = np.arange(1, 80, 1)
    velY = Clid0 * semitone ** x
    notesFreq = velY[velY > 210]
    notesFreq = notesFreq[notesFreq < 850]
    velX = (np.arange(-125, 115, 10))

    pitchVelround = roundup5(vel)
    freqNumTemp = notesFreq[velX == pitchVelround]
    freqhNumTemp = np.clip(freqNumTemp, lowLimit, highLimit)
    freqNum = freqhNumTemp
    return freqNum


def roundup5(x):
    return int(math.ceil(x / 5.0)) * 5

# ?????????
def rms(data):
    return np.sqrt(np.mean(data ** 2))


# Write to a matrix in the data file.
# Input: path - the file path.
#        datasetName - the dataset to write to in the file.
#        input_data - the data to write in.
def writeToFileMat(path, datasetName, input_data):
    with h5py.File(path, "a") as f:
        f[datasetName].resize(f[datasetName].shape[0] + input_data.shape[0], axis=0)
        f[datasetName][-input_data.shape[0]:] = input_data