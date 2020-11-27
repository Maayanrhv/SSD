import numpy as np
import IMUtosound
from enum import Enum

class Sound(Enum):
    NoSound = 0
    Combined = 1
    RollOnly = 2
    PitchOnly = 3
#soundStatus = Sound.Combined
soundStatus = Sound.RollOnly

datasetNames=['fulldataL','fulldataR','volLeftVec','freq_sin','timeVec','pitchVelVec','rollVelVec','IMUMat']

class RTdata:
    def __init__(self,startTT=0):
        #sound data
        self.fulldataL = np.zeros(IMUtosound.FRAMES)  # sound generated in left ear
        self.fulldataR = np.zeros(IMUtosound.FRAMES)  # sound generated in right ear

        #freq and vol
        self.freqTempVecFull = np.zeros(1)  # generated frequency array
        self.volRightTempVecFull = np.zeros(1)  # generated volume array  in right ear
        self.volLeftTempVecFull = np.zeros(1)  # generated volume array in left ear

        #Time
        self.startTT=startTT
        self.timeVec = np.zeros(1)  # contains the timing of each sampling sound

        #Freq
        self.currentFreq=400
        self.prevFreq=100
        self.TT = 0
        self.phase = 0
        self.freqVec=np.zeros(IMUtosound.FRAMES)

        #Vol
        self.volVecLRT=np.zeros(IMUtosound.FRAMES)
        self.volVecRRT=np.zeros(IMUtosound.FRAMES)
        self.currentVol=0.5
        self.prevVol=0.5

        #IMU data
        self.pitchVelTemp = np.zeros(1)  # contains pitch velocity (after average)
        self.rollVelTemp = np.zeros(1)  #
        IMUVec = np.zeros(6)  # the IMU data collected in RT
        self.IMUMat = np.append([IMUVec], [IMUVec + 1],
                                axis=0)  # contains the data from IMU throughout the entire program run

    def setData(self, pitchVel, rollVel, IMUMat):
        self.timeVec=self.TT-self.startTT
        self.IMUMat=IMUMat
        RTdata.setPitchVel(self,pitchVel)
        #RTdata.set_yaw_vel(self,rollVel)
        RTdata.setRollVel(self, pitchVel)

    def setTT(self,TT):
        self.TT=TT

    def setPitchVel(self,pitchVel):
        self.pitchVelTemp=pitchVel
        if soundStatus != Sound.RollOnly:
            self.currentFreq = IMUtosound.vel_to_freq(pitchVel)  # get this pitch velocity's frequency
        self.setFrequency()

    def setFrequency(self):
        if self.currentFreq != self.prevFreq:
            # in case there needs to be a change of frequencies, add the new frequency to the sound wave from the
            # last phase, and update the phase.
            self.phase = 2 * np.pi * self.TT * (self.prevFreq - self.currentFreq) + self.phase
            self.prevFreq = self.currentFreq  # update the previous frequency to be the current one
            self.freqTempVecFull=self.currentFreq


    def setRollVel(self,rollVel):
        self.rollVelTemp=rollVel
        if soundStatus != Sound.PitchOnly:
            self.velVol = IMUtosound.vel_to_vol(rollVel)  # get this roll velocity's volume ratio for the left ear
        else:
            self.velVol = IMUtosound.vel_to_vol(0)  # in case the roll status flag is off, set an equal volume ratio for both ears
        self.volVecLRT, self.volVecRRT, self.currentVol = IMUtosound.vol_vec(self.velVol, self.prevVol)  # get this roll velocity's volume
        self.prevVol = self.currentVol  # update the previous volume to be the current one
        self.volLeftTempVecFull=self.currentVol

    def getfreqSinVal(self):
        return self.phase,self.prevFreq,self.TT

    def getRTdata(self):
        # create a sinus wave of the current frequency that continues the previous frequency's sinus wave.
        self.freqVec = IMUtosound.freq_sin(self)

        if soundStatus != Sound.NoSound:
            #self.fulldataL = self.freqVec * self.volVecLRT
            self.fulldataL = self.freqVec * self.volVecRRT
            self.fulldataR = self.freqVec * self.volVecRRT
        else:
            self.fulldataL = 0
            self.fulldataR = 0

        return self.fulldataL, self.fulldataR

    def appendData(self,other):
        self.fulldataL = np.append(self.fulldataL, other.fullDataL)
        self.fulldataR = np.append(self.fulldataR, other.fullDataR)
        self.pitchVelTemp = np.append(self.pitchVelTemp, other.rollVelTemp)
        self.rollVelTemp = np.append(self.rollVelTemp, other.yawVelTemp)
        self.freqTempVecFull = np.append(self.freqTempVecFull, other.freqTempVecFull)
        self.volLeftTempVecFull = np.append(self.volLeftTempVecFull, other.volLeftTempVecFull)
        self.timeVec = np.append(self.timeVec, other.timeVec)
        if np.shape(other.IMUMat)[0]!=2:
            self.IMUMat = np.append(self.IMUMat, [other.IMUMat], axis=0)

    def initVec(self):

        self.fulldataL = np.zeros(IMUtosound.FRAMES)  # sound generated in left ear
        self.fulldataR = np.zeros(IMUtosound.FRAMES)  # sound generated in right ear
        self.freqTempVecFull = np.zeros(1)  # generated frequency array
        self.volRightTempVecFull = np.zeros(1)  # generated volume array  in right ear
        self.volLeftTempVecFull = np.zeros(1)  # generated volume array in left ear
        self.timeVec = np.zeros(1)  # contains the timing of each sampling sound
        self.pitchVelTemp = np.zeros(1)  # contains pitch velocity (after average)
        self.rollVelTemp = np.zeros(1)  #
        IMUVec = np.zeros(6)  # the IMU data collected in RT
        self.IMUMat = np.append([IMUVec], [IMUVec + 1],
                                axis=0)  # contains the data from IMU throughout the entire program run

