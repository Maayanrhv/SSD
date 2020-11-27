import numpy as np
import h5py
import math
import scipy.io.wavfile

"""
Globals
"""
# The array length of each wave.
# Needs to be short as possible to keep the sound changes congruent with the velocity changes,
# but not too short to keep the sound changes smooth.
FRAMES = 256  # 256 frames = 256*1000/44100 = 5.8ms ~ 6ms

# The sound sampling rate for one second (44.1 ms)
RATE = 44100

global a, b, shift, y0, yf  # parameters for the velocity-to-frequency function


"""
Velocity To Volume Section
"""


# Determine the volume changes ratio.
# Input: vel - roll velocity
#        denominator - determines the range of the velocities.
#        Ex: a velocity of 100 or above will have the highest volume when tha denominator is 100.
# Output: Temporary volume value between 0-1 of the left ear (the right ear will be 1-output respectively)
# Logic: Divide a given yaw velocity by a maximum value to convert it to a value between 0-1 and return that value.
def velToVol(vel, denominator=100):
    velVol = round(vel / denominator, 1)  # round the quotient to one decimal. Ex: 0.6
    velVol = round(velVol, 2)  # round the quotient to two decimal. Ex: 0.60
    return velVol


# Determine the volume changes logic.
# Input: leftVol - temporary roll left volume
#        prevLeftVol - the previous roll volume
# Output: leftVolVec - the left volumes change array
#         rightVolVec - the right volumes change array
#         currentLeftVol - the current left volume.
#         The latter parameter is for the next volume change as a reference (the current volume will become
#         the previous one in the next calling to this function).
# Logic: Gradually change the volume from the previous one to the current one in both ears, by stretching
#        the volume range in each ear across the amount of frames.
def volVec(leftVol, prevLeftVol):
    volLeftTemp = 0.5 + leftVol  # setting the volume to be around 0.5
    currentLeftVol = round(float(np.clip(volLeftTemp, 0, 1)), 3)  # round the velocity to three decimal. Ex: 0.600
    diffVol = round(prevLeftVol - currentLeftVol, 2)  # the difference between the current and the previous volumes
    if (diffVol != 0):  # in case there's been a change in the movement
        # gradually change the volumes from the previous one to the current one by stretching this volume range across
        # the amount of frames.
        # Ex: an array of volumes change across the range of 0.1 to 0.4 with 4 frames will be: [0.1, 0.2, 0.3, 0.4]
        leftVolVec = np.arange(prevLeftVol, currentLeftVol,
                               ((prevLeftVol - currentLeftVol) / FRAMES) * -1, np.float32)
        prevRightVol = 1 - prevLeftVol  # the corresponding previous right volume
        currentRightVol = 1 - currentLeftVol  # the corresponding current right volume
        rightVolVec = np.arange(prevRightVol, currentRightVol,
                                ((prevRightVol - currentRightVol) / FRAMES) * -1, np.float32)
    else:  # in case there hasn't been a change in the movement
        # create an array with the same current volume in each frame (its size is thus the number of frames).
        # there's an array like this for each ear with its own current volume.
        leftVolVec = np.zeros(FRAMES) + currentLeftVol
        rightVolVec = np.zeros(FRAMES) + 1 - currentLeftVol
    return leftVolVec, rightVolVec, currentLeftVol


"""
Velocity To Frequency Section
"""


# Determine the frequency changes logic.
# Logic: Create a logarithmic function that will represent the transformation of velocity to frequency.
#        The function chosen is logarithmic due to human logarithmic hearing of frequencies.
#        f(x) = a * log(x + shifter) + b
#        The head pitch velocities range from about -130 to 130, so that is the range of the X axis of the function
#        (though mathematically there's no limit).
#        The corresponding frequencies range (Y axis) was chosen so it will be pleasant for human hearing.
def vecToFreqFunction():
    global a, b, shift, y0, yf
    yf = 554.3522  # the highest frequency allowed
    y0 = 311.1209  # the lowest frequency allowed
    x0 = -130
    xf = 130
    shift = 440  # a number to add to the velocities and shift the curve in order to avoid negative values
    a = (yf - y0) / (math.log(((xf + shift) / (x0 + shift)), 10))  # find a using 2 points: (x0,y0),(xf, yf)
    b = yf - a * math.log(xf + shift, 10)  # find b using a and one point


# Determine the frequency value according to a given velocity by using a logarithmic function.
# Input: vel - pitch velocity
# Output: prevFreq - frequency value between the high and low limits determined. No difference between ears.
def velToFreq(vel):
    tempFreq = a * math.log(vel + shift, 10) + b  # use the logarithmic function to find the current frequency
    tempFreq = round(tempFreq)  # round the frequency to lower a bit the frequency changes sensitivity
    freq = np.clip(tempFreq, y0, yf)  # ensure the calculated frequency doesn't exceed the limits determined
    return freq


# Create an array of the n-th previous velocities (to later calculate their average velocity).
# Input: velAvgVec - an array containing the last n velocities (this array's length is n).
#        vel - the new velocity to add to this array instead of the oldest one.
# Output: velAvgVec - the given array after the required modification: removing the oldest velocity
#         in it and adding the newest to it.
def velAvg(velAvgVec, vel):
    velAvgVec[:-1] = velAvgVec[1:]
    velAvgVec[-1] = vel
    return velAvgVec


"""
Adaptations of Frequencies and Volume to the Produced Complete Sound
"""


# Create a sinus wave of the current frequency that continues the previous frequency's sinus wave.
# Input: prevFreq - the current frequency
#        phase - the phase of the previous sinus wave
#        TT - current time, global parameter
# Output: a sinus wave formed according to the current frequency that continues the previous frequency's sinus wave.
def freqSin(freq, phase, TT):
    return np.sin(phase + 2 * np.pi * freq * (TT + np.arange(FRAMES) / float(RATE)))


"""
Output File Section
"""


# Calculate the root mean square of the data. Usable in analysis.
def rms(data):
    return np.sqrt(np.mean(data ** 2))


# Start creating the data file.
# Input: path - the file path to keep it in.
#        input_data - the data to write in.
def startOutputFile(path, input_data):
    vec = np.zeros(6)
    velMat = np.append([vec], [vec + 1], axis=0)
    with h5py.File(path, "w") as f:
        f.create_dataset('fulldataL', data=input_data, chunks=True, maxshape=(None,))
        f.create_dataset('fulldataR', data=input_data, chunks=True, maxshape=(None,))
        f.create_dataset('volRightVec', data=input_data, chunks=True, maxshape=(None,))
        f.create_dataset('volLeftVec', data=input_data, chunks=True, maxshape=(None,))
        f.create_dataset('freq_sin', data=input_data, chunks=True, maxshape=(None,))
        f.create_dataset('timeVec', data=input_data, chunks=True, maxshape=(None,))
        f.create_dataset('IMUMat', data=velMat, chunks=True, maxshape=(None, None))


# Write to the data file.
# Input: path - the file path.
#        datasetName - the dataset to write to in the file.
#        input_data - the data to write in.
def writeToFile(path, datasetName, input_data):
    with h5py.File(path, "a") as f:
        f[datasetName].resize(f[datasetName].shape[0] + input_data.shape[0], axis=0)
        f[datasetName][-input_data.shape[0]:] = input_data


# Write to the data file.
# Input: path - the file path.
#        timestr - a string of the current date and time
# Note: In the code directory there needs to be a folder named 'Sound'.
def writeSoundFiles(path, timestr):
    with h5py.File(path, "r") as f:
        fulldataL = f['fulldataL'][:]
        fulldataR = f['fulldataR'][:]
    filenameSound = 'Sound\\sound_' + timestr + '.wav'
    fulldata = np.append([fulldataL], [fulldataR], axis=0)
    scipy.io.wavfile.write(filenameSound, RATE, fulldata.transpose())


# Decipher the binary data file and allow reading it.
# Input: path - the file path to read.
# Output: file - the file object.
def readFromFile(path):
   file = h5py.File(path, 'r')
   return file
