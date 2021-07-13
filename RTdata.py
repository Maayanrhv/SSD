import numpy as np
import IMUtosound
from enum import Enum


class Sound(Enum):
    NoSound = 0
    Combined = 1
    YawOnly = 2
    RollOnly = 3
    Beep = 4


soundStatus = Sound.Combined
# soundStatus = Sound.NoSound
# soundStatus = Sound.RollOnly


def set_sound_status(val):
    global soundStatus
    soundStatus = val


datasetNames = ['fulldataL', 'fulldataR', 'volLeftVec', 'freq_sin', 'timeVec', 'pitchVelVec', 'rollVelVec', 'IMUMat']


# The class to keep the data of a running experiment and later store it.
class RTdata:
    # Initialize all data values to keep
    def __init__(self, startTT=0):
        # sound data
        self.fullDataL = np.zeros(IMUtosound.FRAMES)  # sound generated in left ear
        self.fullDataR = np.zeros(IMUtosound.FRAMES)  # sound generated in right ear

        # freq and vol
        self.freqTempVecFull = np.zeros(1)  # generated frequency array
        self.volRightTempVecFull = np.zeros(1)  # generated volume array  in right ear
        self.volLeftTempVecFull = np.zeros(1)  # generated volume array in left ear

        # Time
        self.startTT = startTT  # the starting time of the experiment
        self.timeVec = np.zeros(1)  # contains the timing of each sampling sound
        self.yy = 0  # callback counter
        self.trialType = 0  # the current trial type

        # Freq
        self.currentFreq = 400  # the current frequency value
        self.prevFreq = 100  # the previous frequency value
        self.TT = 0  # the current date and time
        self.phase = 0  # the sound wave's phase of the current frequency
        self.freqVec = np.zeros(IMUtosound.FRAMES)

        # Vol
        self.volVecLRT = np.zeros(IMUtosound.FRAMES)  # ?
        self.volVecRRT = np.zeros(IMUtosound.FRAMES)  # ?
        self.currentVol = 0.5  # the current volume ratio value
        self.prevVol = 0.5  # the previous volume ratio value

        # IMU data
        self.rollVelTemp = np.zeros(1)  # contains roll velocity (after average)
        self.yawVelTemp = np.zeros(1)  # contains yaw velocity (after average)
        IMUVec = np.zeros(6)  # the IMU data collected in RT
        self.IMUMat = np.append([IMUVec], [IMUVec + 1],
                                axis=0)  # contains the data from IMU throughout the entire program run

        # WiaSLMarks events
        self.WiaSLMark = 0
        # HomingMarks events
        self.HomingMark = 0

    def set_data(self, roll_vel, yaw_vel, IMUMat, current_trial_type, current_yy, WiaSL_mark, Homing_mark):  # , Homing_mark):
        self.timeVec = self.TT-self.startTT
        self.IMUMat = IMUMat
        self.yy = current_yy
        self.trialType = current_trial_type
        RTdata.set_roll_vel(self, roll_vel)
        RTdata.set_yaw_vel(self, yaw_vel)
        self.WiaSLMark = WiaSL_mark
        self.HomingMark = Homing_mark

    def set_trial_type(self, current_trial_type):
        self.trialType = current_trial_type
    #
    # def set_WiaSL_mark(self, mark):
    #     self.WiaSLMark = mark

    def get_trial_type(self):
        return self.trialType

    def get_yy(self):
        return self.yy

    def set_TT(self, TT):
        self.TT = TT

    def set_roll_vel(self, roll_vel):
        self.rollVelTemp = roll_vel
        if soundStatus == Sound.Beep:
            set_sound_status(Sound.RollOnly)
            self.currentFreq = IMUtosound.vel_to_freq(120)  # get this roll velocity's frequency
        elif soundStatus != Sound.YawOnly:
            self.currentFreq = IMUtosound.vel_to_freq(roll_vel)  # get this pitch velocity's frequency

        self.set_frequency()

    def set_frequency(self):
        if self.currentFreq != self.prevFreq:
            # in case there needs to be a change of frequencies, add the new frequency to the sound wave from the
            # last phase, and update the phase.
            self.phase = 2 * np.pi * self.TT * (self.prevFreq - self.currentFreq) + self.phase
            self.prevFreq = self.currentFreq  # update the previous frequency to be the current one
            self.freqTempVecFull = self.currentFreq

    def set_yaw_vel(self, yaw_vel):
        self.yawVelTemp = yaw_vel
        if soundStatus != Sound.RollOnly:
            self.velVol = IMUtosound.vel_to_vol(yaw_vel)  # get this roll velocity's volume ratio for the left ear
        else:
            # in case the yaw status flag is off, set an equal volume ratio for both ears
            self.velVol = IMUtosound.vel_to_vol(0)
        # get this yaw velocity's volume
        self.volVecLRT, self.volVecRRT, self.currentVol = IMUtosound.vol_vec(self.velVol, self.prevVol)
        self.prevVol = self.currentVol  # update the previous volume value to be the current one
        self.volLeftTempVecFull = self.currentVol

    def get_freq_sin_val(self):
        return self.phase, self.prevFreq, self.TT

    def get_RTdata(self):
        # create a sinus wave of the current frequency that continues the previous frequency's sinus wave.
        self.freqVec = IMUtosound.freq_sin(self)

        if soundStatus != Sound.NoSound:
            self.fullDataL = self.freqVec * self.volVecLRT
            self.fullDataR = self.freqVec * self.volVecRRT
        else:
            self.fullDataL = 0
            self.fullDataR = 0

        return self.fullDataL, self.fullDataR

    def append_data(self, other):
        self.fullDataL = np.append(self.fullDataL, other.fullDataL)
        self.fullDataR = np.append(self.fullDataR, other.fullDataR)
        self.rollVelTemp = np.append(self.rollVelTemp, other.rollVelTemp)
        self.yawVelTemp = np.append(self.yawVelTemp, other.yawVelTemp)
        self.freqTempVecFull = np.append(self.freqTempVecFull, other.freqTempVecFull)
        self.volLeftTempVecFull = np.append(self.volLeftTempVecFull, other.volLeftTempVecFull)
        self.timeVec = np.append(self.timeVec, other.timeVec)
        self.yy = np.append(self.yy, other.yy)
        self.trialType = np.append(self.trialType, other.trialType)
        self.WiaSLMark = np.append(self.WiaSLMark, other.WiaSLMark)
        self.HomingMark = np.append(self.HomingMark, other.HomingMark)

        if np.shape(other.IMUMat)[0] != 2:
            self.IMUMat = np.append(self.IMUMat, [other.IMUMat], axis=0)

    def init_vec(self):
        self.fullDataL = np.zeros(IMUtosound.FRAMES)  # sound generated in left ear
        self.fullDataR = np.zeros(IMUtosound.FRAMES)  # sound generated in right ear
        self.freqTempVecFull = np.zeros(1)  # generated frequency array
        self.volRightTempVecFull = np.zeros(1)  # generated volume array  in right ear
        self.volLeftTempVecFull = np.zeros(1)  # generated volume array in left ear
        self.timeVec = np.zeros(1)  # contains the timing of each sampling sound
        self.rollVelTemp = np.zeros(1)  # contains roll velocity (after average)
        self.yawVelTemp = np.zeros(1)  # contains yaw velocity (after average)
        self.yy = np.zeros(1)  # callback counter
        self.trialType = np.zeros(1)  # current trial type
        self.WiaSLMark = np.zeros(1)
        self.HomingMark = np.zeros(1)
        IMUVec = np.zeros(6)  # the IMU data collected in RT
        self.IMUMat = np.append([IMUVec], [IMUVec + 1],
                                axis=0)  # contains the data from IMU throughout the entire program run
