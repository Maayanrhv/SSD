from datetime import datetime
import numpy as np
import h5py
import os
import time
import RTdata as rt
import scipy.io.wavfile
import IMUtosound
from math import ceil as mceil
import GUI
import Trials
import csv


# Write to the data file.
# Input: path - the file path.
#        timestr - a string of the current date and time
# Note: In the code directory there needs to be a folder named 'Sound'.


# datasetNames = ['fulldataL','fulldataR','volLeftVec','freq_sin','timeVec','pitchVelVec','rollVelVec','IMUMat']
datasetNames = ['fulldataL', 'fulldataR', 'volLeftVec', 'freq_sin', 'timeVec', 'pitchVelVec',
                'rollVelVec', 'IMUMat', 'yy', 'trialType']
# totalTimeSec=1200
# totalTimeSec=1800
totalTimeSec = 3600
# secForFile=20 # 1500 yy
secForFile = 60  # 1500 yy
numYY = 500 * secForFile


class OutputFile:
    def __init__(self, dirname=None):
        # self.timestr = datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S.%f')[:-3]
        if dirname is None:
            # self.timestr = datetime.now().strftime('%Y-%m-%d-%H-%M-%S.%f')[:-3]
            self.timestr = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        else:
            self.timestr = dirname
        # self.filenameHdf = 'Output\\FullData_' + self.timestr + '.hdf5'
        self.filenameHdf = os.path.join('Output' + os.sep, 'FullData_' + self.timestr + '.hdf5')
        self.filenmameDir = os.path.join('Output' + os.sep, self.timestr + os.sep)
        # filenameHdf = os.path.join('Output' + os.sep,test+ os.sep, 'FullData_' + timestr + '.hdf5')
        self.filenameHdf2 = os.path.join('FullData_' + self.timestr + '.hdf5')
        self.filenameCSV = os.path.join(self.filenmameDir, 'Beam_Trials-' + self.timestr + '.csv')
        self.bufferData = rt.RTdata()
        if dirname is None:
            OutputFile.startOutputFile(self)
        # outputfile.createCSVFile(self)

    def getTimestr(self):
        return self.timestr

    def getFilenameHdf(self):
        return  self.filenameHdf

    def getFilenameDir(self):
        return self.filenmameDir

    # Creating the rows for the Beam CSV file - For Balance experiment only
    def createCSVFileRows(self, trialType):
        trialsList = Trials.get_trials_list()
        rows = []
        ii = 0
        # trialType=5
        # trialsInexes=np.where(trialsList==trialType)[0]
        trialsInexes = list(np.where(np.array(trialsList) == trialType)[0])
        while ii < len(trialsInexes):
            row = [ii + 1, Trials.trialTypes[trialsList[trialsInexes[ii]]], trialsInexes[ii], "NULL", trialType]
            rows.append(row)
            ii = ii+1
        return rows

    # Filling Beam CSV file with the created rows above - For Balance experiment only
    def createCSVFile(self):
        rows_list = [["Index", "trialType", "trial Number", 'Dist', "trialTypeInd"]]
        rows_list = rows_list + OutputFile.createCSVFileRows(self, 5)
        rows_list = rows_list + OutputFile.createCSVFileRows(self, 6)
        with open(self.filenameCSV, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows_list)
        print(self.filenameCSV)

    def startOutputFile(self):
        vec = np.zeros(6)
        input_data = np.zeros(IMUtosound.vecStart)
        velMat = np.append([vec], [vec + 1], axis=0)
        # with h5py.File(self.filenameHdf, "w") as f:
        #     for ii in datasetNames:
        #         if ii in ['IMUMat']:
        #             f.create_dataset(ii, data=velMat, chunks=True, maxshape=(None, None))
        #         else:
        #             f.create_dataset(ii, data=input_data, chunks=True, maxshape=(None,))

        os.mkdir(self.filenmameDir)
        counter = 0
        numOfFiles = totalTimeSec/secForFile
        while counter < numOfFiles:
            fileIndex = counter
            fileIndex = "{:02d}_".format(fileIndex)
            fullname = os.path.join(self.filenmameDir, fileIndex + self.filenameHdf2)
            with h5py.File(fullname, "w") as f:
                for ii in datasetNames:
                    if ii in ['IMUMat']:
                        f.create_dataset(ii, data=velMat, chunks=True, maxshape=(None, None))
                    else:
                        f.create_dataset(ii, data=input_data, chunks=True, maxshape=(None,))
            print(counter, fullname)
            counter = counter+1

    def appendData(self, other, ii):
        self.bufferData.append_data(other)
        if ii % 5 == 0:
            OutputFile.addVecToFile(self, ii)

    def writeToFile(self, datasetName, input_data, currentYY):

        fileIndex = int(currentYY/1500)
        fileIndex = "{:02d}_".format(fileIndex)
        fullname = os.path.join(self.filenmameDir, fileIndex+self.filenameHdf2)
        with h5py.File(fullname, "a") as f:
        # with h5py.File(self.filenameHdf, "a") as f:
            f[datasetName].resize(f[datasetName].shape[0] + input_data.shape[0], axis=0)
            f[datasetName][-input_data.shape[0]:] = input_data

        # print(fullname)

    # update output file to remove all unnecessary
    def updateOutputfile(self, finYY):
        outputFilesFin = mceil((finYY / numYY))
        numOfFiles = totalTimeSec / secForFile
        print(outputFilesFin, numOfFiles)
        counter = 0
        needToBeUpdated = OutputFile.checkIfNeedToBeUpdated(self)
        while (counter < numOfFiles) and needToBeUpdated:
            fileIndex = counter
            fileIndex = "{:02d}_".format(fileIndex)
            fullname = os.path.join(self.filenmameDir, fileIndex + self.filenameHdf2)
            # os.remove(fullname)
            if (counter < outputFilesFin):
                origFilePath = fullname
                filename1 = IMUtosound.read_from_file(origFilePath)
                # path = "Output\\newfile.hdf5"
                path = os.path.join(self.filenmameDir + os.sep, 'newfile.hdf5')
                # temp = "Output\\tempfile.hdf5"
                temp = os.path.join(self.filenmameDir + os.sep, 'tempfile.hdf5')
                with h5py.File(path, "w") as f:
                    f.create_dataset('freq_sin', data=filename1['freq_sin'][IMUtosound.vecStart:], chunks=True,
                                     maxshape=(None,))
                    f.create_dataset('fulldataL', data=filename1['fulldataL'][IMUtosound.vecStart:], chunks=True,
                                     maxshape=(None,))
                    f.create_dataset('fulldataR', data=filename1['fulldataR'][IMUtosound.vecStart:], chunks=True,
                                     maxshape=(None,))
                    f.create_dataset('timeVec', data=filename1['timeVec'][IMUtosound.vecStart:], chunks=True,
                                     maxshape=(None,))
                    f.create_dataset('volLeftVec', data=filename1['volLeftVec'][IMUtosound.vecStart:], chunks=True,
                                     maxshape=(None,))
                    f.create_dataset('pitchVelVec', data=filename1['pitchVelVec'][IMUtosound.vecStart:], chunks=True,
                                     maxshape=(None,))
                    f.create_dataset('rollVelVec', data=filename1['rollVelVec'][IMUtosound.vecStart:], chunks=True,
                                     maxshape=(None,))
                    f.create_dataset('yy', data=filename1['yy'][IMUtosound.vecStart:], chunks=True,
                                     maxshape=(None,))
                    f.create_dataset('trialType', data=filename1['trialType'][IMUtosound.vecStart:], chunks=True,
                                     maxshape=(None,))
                    f.create_dataset('IMUMat', data=filename1['IMUMat'][2:], chunks=True, maxshape=(None, None))

                filename1.close()
                time.sleep(1)
                os.rename(origFilePath, temp)
                os.rename(path, origFilePath)
                os.remove(temp)
                print(fullname)

            else:
                os.remove(fullname)
                # print(fullname + " Deleted")
            counter = counter + 1

        # # Write sound file from log file
        # # if os.name=='posix':
        # #     self.writeSoundFiles()

    def addVecToFile(self, counter=10):
        # self.bufferData.fulldataL = self.bufferData.fulldataL[IMUtosound.FRAMES:]
        # outputfile.writeToFile(self, "fulldataL", self.bufferData.fulldataL,counter)
        # print(counter)
        # outputfile.writeToFile(self, "fulldataL", self.bufferData.fulldataL, counter)

        fileIndex = int(counter / numYY)  # every numYY times, fileIndex increases by 1 (fileIndex range: 0, 1, 2,...)
        fileIndex = "{:02d}_".format(fileIndex)
        fullname = os.path.join(self.filenmameDir, fileIndex + self.filenameHdf2)
        with h5py.File(fullname, "a") as f:
            # with h5py.File(self.filenameHdf, "a") as f:
            # def writeToFile(self, datasetName, input_data,numyy=1000):
            self.bufferData.fullDataL = self.bufferData.fullDataL[IMUtosound.FRAMES:]
            self.bufferData.fullDataL = self.bufferData.fullDataL[0::4]
            f["fulldataL"].resize(f["fulldataL"].shape[0] + self.bufferData.fullDataL.shape[0], axis=0)
            f["fulldataL"][-self.bufferData.fullDataL.shape[0]:] = self.bufferData.fullDataL
            
            self.bufferData.fullDataR = self.bufferData.fullDataR[IMUtosound.FRAMES:]
            self.bufferData.fullDataR = self.bufferData.fullDataR[0::4]
            f["fulldataR"].resize(f["fulldataR"].shape[0] + self.bufferData.fullDataR.shape[0], axis=0)
            f["fulldataR"][-self.bufferData.fullDataR.shape[0]:] = self.bufferData.fullDataR

            self.bufferData.IMUMat = self.bufferData.IMUMat[2:]
            # outputfile.writeToFile(self, "IMUMat", self.bufferData.IMUMat,counter)
            f["IMUMat"].resize(f["IMUMat"].shape[0] + self.bufferData.IMUMat.shape[0], axis=0)
            f["IMUMat"][-self.bufferData.IMUMat.shape[0]:] = self.bufferData.IMUMat
            zerosVecVelMat = np.zeros(6)
            self.bufferData.IMUMat = np.append([zerosVecVelMat], [zerosVecVelMat + 1], axis=0)

            self.bufferData.freqTempVecFull = self.bufferData.freqTempVecFull[1:]
            f["freq_sin"].resize(f["freq_sin"].shape[0] + self.bufferData.freqTempVecFull.shape[0], axis=0)
            f["freq_sin"][-self.bufferData.freqTempVecFull.shape[0]:] = self.bufferData.freqTempVecFull

            self.bufferData.volLeftTempVecFull = self.bufferData.volLeftTempVecFull[1:]
            # outputfile.writeToFile(self, "volLeftVec", self.bufferData.volLeftTempVecFull,counter)
            f["volLeftVec"].resize(f["volLeftVec"].shape[0] + self.bufferData.volLeftTempVecFull.shape[0], axis=0)
            f["volLeftVec"][-self.bufferData.volLeftTempVecFull.shape[0]:] = self.bufferData.volLeftTempVecFull

            self.bufferData.timeVec = self.bufferData.timeVec[1:]
            # outputfile.writeToFile(self, "timeVec", self.bufferData.timeVec,counter)
            f["timeVec"].resize(f["timeVec"].shape[0] + self.bufferData.timeVec.shape[0], axis=0)
            f["timeVec"][-self.bufferData.timeVec.shape[0]:] = self.bufferData.timeVec

            self.bufferData.rollVelTemp = self.bufferData.rollVelTemp[1:]
            # outputfile.writeToFile(self, "pitchVelVec", self.bufferData.pitchVelTemp,counter)
            f["pitchVelVec"].resize(f["pitchVelVec"].shape[0] + self.bufferData.rollVelTemp.shape[0], axis=0)
            f["pitchVelVec"][-self.bufferData.rollVelTemp.shape[0]:] = self.bufferData.rollVelTemp

            self.bufferData.yawVelTemp = self.bufferData.yawVelTemp[1:]
            # outputfile.writeToFile(self, "rollVelVec", self.bufferData.rollVelTemp,counter)
            f["rollVelVec"].resize(f["rollVelVec"].shape[0] + self.bufferData.yawVelTemp.shape[0], axis=0)
            f["rollVelVec"][-self.bufferData.yawVelTemp.shape[0]:] = self.bufferData.yawVelTemp

            self.bufferData.yy = self.bufferData.yy[1:]
            # outputfile.writeToFile(self, "rollVelVec", self.bufferData.rollVelTemp,counter)
            f["yy"].resize(f["yy"].shape[0] + self.bufferData.yy.shape[0], axis=0)
            f["yy"][-self.bufferData.yy.shape[0]:] = self.bufferData.yy
            
            self.bufferData.trialType = self.bufferData.trialType[1:]
            # outputfile.writeToFile(self, "rollVelVec", self.bufferData.rollVelTemp,counter)
            f["trialType"].resize(f["trialType"].shape[0] + self.bufferData.trialType.shape[0], axis=0)
            f["trialType"][-self.bufferData.trialType.shape[0]:] = self.bufferData.trialType
            # print(self.bufferData.trialType)

        self.bufferData.init_vec()

    def writeSoundFiles(self):
        with h5py.File(self.filenameHdf, "r") as f:
            fulldataL = f['fulldataL'][:]
            fulldataR = f['fulldataR'][:]
        # filenameSound = 'Output\\Sound_' + self.timestr + '.wav'
        filenameSound = os.path.join('Output' + os.sep, 'Sound_' + self.timestr + '.wav')
        fulldata = np.append([fulldataL], [fulldataR], axis=0)
        scipy.io.wavfile.write(filenameSound, IMUtosound.RATE, fulldata.transpose())
        print(filenameSound)

    def printFile(self):
        with h5py.File(self.filenameHdf,"r") as f:
            print(f['pitchVelVec'][:])
            # for ii in datasetNames:
                # print(ii,f[ii][:])

    def getLastYY(self):
        print("outputfile.getLastYY")
        maxYY = 0
        print(OutputFile.getFilenameDir(self))
        for file in os.listdir(self.filenmameDir):
            if file.endswith(".hdf5"):
                currfilename = (os.path.join(self.filenmameDir, file))
                with h5py.File(currfilename, "r") as f:
                    if (f['timeVec'][0:10] == f['yy'][0:10]).all():
                        if f['yy'][-1]>maxYY:
                            print(f['yy'][-1])
                            maxYY = f['yy'][-1]
                    else:
                        print("Files Already Ready To Analyze")
        return maxYY

    def checkIfNeedToBeUpdated(self):
        # going over all the output file in folder and checks
        # if updateOuputfile already done.
        print("outputfile.checkIfNeedToBeUpdated")
        needToBeUpdated = 1
        print(OutputFile.getFilenameDir(self))
        for file in os.listdir(self.filenmameDir):
            if file.endswith(".hdf5"):
                currfilename = (os.path.join(self.filenmameDir, file))
                with h5py.File(currfilename, "r") as f:
                    if not((f['timeVec'][0:10] == f['yy'][0:10]).all()):
                        needToBeUpdated=0
                        print(currfilename,needToBeUpdated)
                    else:
                        print(currfilename,needToBeUpdated)
        return needToBeUpdated
