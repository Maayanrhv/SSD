import time
import numpy as np
from datetime import datetime

"""
Globals
"""
# The array length of each wave.
# Needs to be short as possible to keep the sound changes congruent with the velocity changes,
# but not too short to keep the sound changes smooth.
FRAMES = 256

# The sound sampling rate for one second (44.1 ms).
RATE = 44100

CHANNELS = 2
TT = time.time()
startTT = TT
prevFreq = 100
currentFreq = 400
phase = 0

yaw_vel=0
rollMaxVel=100
prevVol=0.5
currentVol=0.5
timestr = datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S.%f')[:-3]

soundStatus=1
#0 no sound #1 combined #2 only roll #3 only pitch

global fulldataL,fulldataR,yy
yy=0
fulldataL=np.zeros(FRAMES)
fulldataR=np.zeros(FRAMES)

global freqTempVecFull
freqTempVecFull=np.zeros(1)

global volRightTempVecFull,volLeftTempVecFull
volRightTempVecFull=np.zeros(1)
volLeftTempVecFull=np.zeros(1)

global timeVec
timeVec=np.zeros(1)

global elpasedtimeTT
