import math
import numpy as np
import matplotlib.pyplot as plt

# # Globals
# global highLimit, lowLimit, velRanges, freqRange
FRAMES = 256


def roundup5(x):
    return int(math.ceil(x / 5.0)) * 5


def roundup10(x):
    return int(math.ceil(x / 10.0)) * 10


def roundup15(x):
    return int(math.ceil(x / 15.0)) * 15


def roundup20(x):
    return int(math.ceil(x / 20.0)) * 20


def roundup25(x):
    return int(math.ceil(x / 25.0)) * 25


# def setFreqRange():
#     # frequencies range is between highLimit and lowLimit
#     highLimit = 1567.98
#     lowLimit = 103.8262
#     # set the range of frequencies to be those of a piano keys.
#     key0 = 16.35160
#     semitone = 17.32391 / key0
#     pow = np.arange(1, 80, 1)
#     keyboardFreq = key0 * semitone ** pow  # all keyboard frequencies in semitones
#     freqRange = keyboardFreq[keyboardFreq > 100]  # all 48 keyboard frequencies above 100Hz
#     velRanges = np.arange(-125, 115, 5)  # 48 ranges of 5s between -125-115. Ex: 105 represents velocities between 105-109.


def velToFreq(vel):
    highLimit = 554.3522  # 1567.98  # yf
    lowLimit = 311.1209  # 103.8262  # y0
    x0 = -130
    xf = 130
    num = 131
    a = (highLimit-lowLimit)/(math.log(((xf+num)/(x0+num)), 10))
    b = highLimit - a * math.log(xf + num, 10)
    freqhNumTemp = a * math.log(vel + num, 10) + b
    # num = 1.02
    # freqhNumTemp = 440 * num ** (vel / 5)
    freqhNumTemp = round(freqhNumTemp)
    freqhNumTemp = np.clip(freqhNumTemp, lowLimit, highLimit)
    return freqhNumTemp


    # # frequencies range is between highLimit and lowLimit
    # highLimit = 1567.98
    # lowLimit = 103.8262
    # # set the range of frequencies to be those of a piano keys.
    # key0 = 16.35160
    # semitone = 17.32391 / key0
    # pow = np.arange(1, 80, 1)
    # keyboardFreq = key0 * semitone ** pow  # all keyboard frequencies in semitones
    # freqRange = keyboardFreq[keyboardFreq > 300]  # all 36 keyboard frequencies above 210Hz
    # freqRange = freqRange[freqRange < 560]  # all 24 keyboard frequencies above 210Hz and below 850Hz
    # velRanges = np.arange(-125, 130, 25)  # 48 ranges of 5s between -125-115. Ex: 105 represents velocities between 105-109.
    #
    # # round vel to be divisible by 5
    # pitchVelround = roundup25(vel)
    # # take the frequency from notesFreq in the index where the velocity range is equal to the rounded velocity
    # freqNumTemp = freqRange[velRanges == pitchVelround]
    # if not freqNumTemp:
    #     if pitchVelround<velRanges[0]:
    #         freqNumTemp=velRanges[0]
    #     else:
    #         freqNumTemp = velRanges[-1]
    # # if the chosen frequency is higher than the highest frequency determined, then change it to be the highest allowed.
    # # if the chosen frequency is lower than the lowest frequency determined, then change it to be the lowest allowed.
    # freqNum = np.clip(freqNumTemp, lowLimit, highLimit)
    # return freqNum


# Determine the volume changes ratio.
# Input: Roll velocity
# Output: Volume value between 0-1 of the left ear (the right ear will be 1-output respectively)
# Logic: Divide a given yaw velocity by a maximum value to convert it to a value between 0-1 and return that value.
def velToVol(vel, denominator=100):
    velVol = round(vel / denominator, 1)  # round the quotient to one decimal. Ex: 0.6
    velVol = round(velVol, 2)  # round the quotient to two decimal. Ex: 0.60
    return velVol


# Determine the volume changes logic.
# Input: Roll left velocity
# Output: The left volumes change array, the right volumes change array and the current left volume.
#         The latter parameter is for the next volume change as a reference (the current volume will become
#         the previous one in the next calling to this function).
# Logic: Gradually change the volume from the previous one to the current one in both ears, by stretching
#        the volume range in each ear across the amount of frames.
def volVec(leftVol, prevLeftVol):
    volLeftTemp = 0.5 + leftVol
    currentLeftVol = round(float(np.clip(volLeftTemp, 0, 1)), 3)  # round the velocity to three decimal. Ex: 0.600
    diffVol = round(prevLeftVol - currentLeftVol, 2)
    if (diffVol != 0):  # in case there's been a change in the movement
        # gradually change the volumes from the previous one to the current one by stretching this volume range across
        # the amount of frames.
        # Ex: an array of volumes change across the range of 0.1 to 0.4 with 4 frames will be: [0.1, 0.2, 0.3, 0.4]
        leftVolVec = np.arange(prevLeftVol, currentLeftVol, ((prevLeftVol - currentLeftVol) / FRAMES) * -1, np.float32)
        prevRightVol = 1 - prevLeftVol  # the corresponding previous right volume
        currentRightVol = 1 - currentLeftVol  # the corresponding current right volume
        rightVolVec = np.arange(prevRightVol, currentRightVol, ((prevRightVol - currentRightVol) / FRAMES) * -1, np.float32)
    else:  # in case there hasn't been a change in the movement
        # create an array with the same current volume in each frame (its size is thus the number of frames).
        # there's an array like this for each ear with its own current volume.
        leftVolVec = np.zeros(FRAMES) + currentLeftVol
        rightVolVec = np.zeros(FRAMES) + 1 - currentLeftVol
    return leftVolVec, rightVolVec, currentLeftVol


# setFreqRange()
# for i in range(-200, 201):
#     res = vel_to_freq(i)
#     print(i, res)

prevVol = 0.5
for i in range(-400, 400):
    leftVol = velToVol(i)
    volVecL, volVecR, currentVolLeft = volVec(leftVol, prevVol)
    prevVol = currentVolLeft

x=np.arange(-130,130,1)
y=np.zeros(len(x))
ii=0
for value in x:
    a = velToFreq(value)
    y[ii]=(velToFreq(value))
    print(x[value],y[ii])
    ii+=1
plt.plot(x,y)
plt.ylabel("Frequency: Hz")
plt.xlabel("Velocity: m/s")
plt.tight_layout()
plt.show()
