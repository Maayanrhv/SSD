import pyaudio
import numpy as np
import IMUComponent
import time
from datetime import datetime
import winsound
import IMUtosound
from enum import Enum


# A flag of the options of which data to play and collect.
class Sound(Enum):
    NoSound = 0
    Combined = 1
    RollOnly = 2
    PitchOnly = 3


"""
Globals
"""
# The array length of each wave.
# Needs to be short as possible to keep the sound changes congruent with the velocity changes,
# but not too short to keep the sound changes smooth.
FRAMES = 256  # 256 frames = 256*1000/44100 = 5.8ms ~ 6ms

# The sound sampling rate for one second (44.1 ms)
RATE = 44100

# Number of channels for PyAudio library
CHANNELS = 2

# The current date and time
TT = time.time()

# The starting time
startTT = TT

# The previous frequency
prevFreq = 100

# The current frequency
currentFreq = 400

# The phase of the sounds's wave. No phase in initialization
phase = 0

# The pitch velocity given from the IMU
roll_vel = 0

# The roll velocity given from the IMU
yaw_vel = 0

# The maximum roll velocity to be used as a reference to calculate volume
rollMaxVel = 100

# The previous volume. Equal volume to both ears in initialization
prevVol = 0.5

# The current volume. Equal volume to both ears in initialization
currentVol = 0.5

# The current date and time as a string
timestr = datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S.%f')[:-3]

# A flag indicating which data to play and collect.
soundStatus = Sound.Combined

yy = 0  # callback counter

fulldataL = np.zeros(FRAMES)  # sound generated in left ear

fulldataR = np.zeros(FRAMES)  # sound generated in right ear

freqTempVecFull = np.zeros(1)  # generated frequency array

volRightTempVecFull = np.zeros(1)  # generated volume array  in right ear

volLeftTempVecFull = np.zeros(1)  # generated volume array in left ear

timeVec = np.zeros(1)  # contains the timing of each sampling sound

global elpasedtimeTT  # how long the program runs

# Creating Logs data file. Require directory named 'Output'
filenameFullDataVec = 'Output\\FullData_' + timestr + '.hdf5'
zerosVec = np.zeros(FRAMES)

IMUtosound.startOutputFile(filenameFullDataVec, zerosVec)

data = np.zeros(FRAMES * 2, np.float32)  # the current sound that is played through callback
IMUVec = np.zeros(6)  # the IMU data collected in RT
IMUMat = np.append([IMUVec], [IMUVec + 1], axis=0)  # contains the data from IMU throughout the entire program run


# Play generated sound in RT
def callback(in_data, frame_count, time_info, status):
    global TT, phase, prevFreq, currentFreq, vec, IMUMat, startTT, elpasedtimeTT
    global freqVec, yy
    global fulldataL, fulldataR, freqTempVecFull, filenameFullDataVec
    global volRightTempVecFull, volLeftTempVecFull, timeVec
    global yaw_vel, rollMaxVel, currentVol, prevVol

    elpasedtimeTT = TT - startTT

    # Change Frequency
    if soundStatus != Sound.RollOnly:
        if yy % 1 == 0:
            currentFreq = IMUtosound.vel_to_freq(roll_vel)  # get this pitch velocity's frequency
    if currentFreq != prevFreq:
        # in case there needs to be a change of frequencies, add the new frequency to the sound wave from the
        # last phase, and update the phase.
        phase = 2 * np.pi * TT * (prevFreq - currentFreq) + phase
        prevFreq = currentFreq  # update the previous frequency to be the current one
    # create a sinus wave of the current frequency that continues the previous frequency's sinus wave.
    freqVec = IMUtosound.freq_sin(prevFreq, phase, TT)

    # Change Volume
    if soundStatus != Sound.PitchOnly:
        velVol = IMUtosound.vel_to_vol(-rollVel)  # get this roll velocity's volume ratio for the left ear
    else:
        velVol = IMUtosound.vel_to_vol(0)  # in case the roll status flag is off, set an equal volume ratio for both ears
    volVecLRT, volVecRRT, currentVol = IMUtosound.vol_vec(velVol, prevVol)  # get this roll velocity's volume
    prevVol = currentVol  # update the previous volume to be the current one

    # Apply Change
    # data - frequency and volume
    if soundStatus != Sound.NoSound:
        data[0::2] = freqVec * volVecLRT  # left ear data
        data[1::2] = freqVec * volVecRRT  # right ear data
    else:
        data[0::2] = 0  # left ear data
        data[1::2] = 0  # right ear data
    TT += FRAMES / float(RATE)

    # RT log
    # yy += 1
    # # write to log file every 10 iterations (the data contains all those iterations)
    # if yy % 10 == 0:
    #     fulldataL = fulldataL[FRAMES:]
    #     IMUtosound.writeToFile(filenameFullDataVec, "fulldataL", fulldataL)
    #     fulldataR = fulldataR[FRAMES:]
    #     IMUtosound.writeToFile(filenameFullDataVec, "fulldataR", fulldataR)
    #
    #     IMUMat = IMUMat[2:]
    #     IMUtosound.writeToFile(filenameFullDataVec, "IMUMat", IMUMat)
    #     zerosVecVelMat = np.zeros(6)
    #     IMUMat = np.append([zerosVecVelMat], [zerosVecVelMat + 1], axis=0)
    #
    #     freqTempVecFull = freqTempVecFull[1:]
    #     IMUtosound.writeToFile(filenameFullDataVec, "freq_sin", freqTempVecFull)
    #     freqTempVecFull = np.zeros(1)
    #
    #     volLeftTempVecFull = volLeftTempVecFull[1:]
    #     IMUtosound.writeToFile(filenameFullDataVec, "volLeftVec", volLeftTempVecFull)
    #     volLeftTempVecFull = np.zeros(1)
    #
    #     timeVec = timeVec[1:]
    #     IMUtosound.writeToFile(filenameFullDataVec, "timeVec", timeVec)
    #     timeVec = np.zeros(1)
    #
    #     # after adding to file, erase data to allow new data to be kept
    #     fulldataL = np.zeros(FRAMES)
    #     fulldataR = np.zeros(FRAMES)
    #
    # # add current data (velocities, volume, frequency) to arrays (that will later be added to the log file)
    # fulldataL = np.append(fulldataL, data[0::2])
    # fulldataR = np.append(fulldataR, data[1::2])
    # freqTempVecFull = np.append(freqTempVecFull, prevFreq)
    # volLeftTempVecFull = np.append(volLeftTempVecFull, currentVol)
    # timeVec = np.append(timeVec, elpasedtimeTT)
    # IMUMat = np.append(IMUMat, [IMUVec], axis=0)

    return data, pyaudio.paContinue


"""
Initialization
"""

# Start-the-program sound
time.sleep(1)
winsound.Beep(1600, 200)
winsound.Beep(1600, 200)
time.sleep(1)

# Initialize the function that transforms velocity to frequency
IMUtosound.vec_to_freq_function()

# Initialize PyAudio
p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=FRAMES,
                output_device_index=3,
                stream_callback=callback)

stream.start_stream()

# Initialize IMU
imu_component = IMUComponent.IMUComponent(port_num='COM4',
                                          baud_rate=921600,
                                          parity='None',
                                          num_of_bits=8,
                                          stop_bit=1,
                                          time_out_in_ms=100)

imu_component.MakeOperational()

ii = 0  # loop counter

# set the program starting time
start_time = time.time()

# how long the program will run
elpasedtime = 0

# pitchVelCurr=0
pitchVelVec = np.zeros(20)

# main loop that keeps reading velocities from IMU and allows callback to stream sound
while elpasedtime < 20:
    ii += 1

    IMUVec = imu_component.GetPacket()

    # pitch velocity from IMU
    pitchVelCurr = round(IMUVec[0])
    # change to the averaged velocity of last length(pitchVelVec) velocities
    pitchVelVec = IMUtosound.vel_avg(pitchVelVec, pitchVelCurr)
    roll_vel = np.average(pitchVelVec)
    # roll velocity from IMU
    yaw_vel = round(IMUVec[2])

    # time for verifying when adding log
    elpasedtime = (round((time.time() - start_time), 3))


# Close PyAudio stream
stream.stop_stream()
stream.close()
p.terminate()

# End-the-program sound
winsound.Beep(1600, 200)
winsound.Beep(1600, 200)

# Write sound file from log file
IMUtosound.writeSoundFiles(filenameFullDataVec, timestr)

