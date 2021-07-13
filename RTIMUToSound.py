import pyaudio
# import pyaudioexclusive as pyaudio  #for windows exclusive mode
import numpy as np
import IMUComponent
import time
import IMUtosound
import OutputFile as opf
import RTdata as rt
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *  
import GUI
import Trials
from DataHandler import OrganizeByTrials, DistanceErrorFile


""" Parameters Initialization """

# Determine the necessary streaming values depending on the used OS
# For Windows OS
if os.name == 'nt':
    outputDeviceIndex = 3  # 11
    portNum = 'COM3'  # 'COM11'
# For Linux OS
if os.name == 'posix':
    outputDeviceIndex = 18
    portNum = '/dev/ttyUSB0'

TT = time.time()  # the current date and time
startTT = TT  # the starting time of the program
yy = 0  # callback counter
trialType = 0  # the trial type
IMUtosound.vec_to_freq_function(600)  # initialize the function that transforms velocity to frequency
data, roll_vel, yaw_vel, IMUVec = IMUtosound.init_params()  # initialize parameters relevant for saved data
current_data = rt.RTdata(startTT)  # initialize RTData object that organizes the saved data per run
output_file = opf.OutputFile()  # initialize OutputFile object that handles the saved data file
WiaSL_mark = 0
Homing_mark = 0


""" Playing Sound """


# Play generated sound in RT (real time).
# Note: PyAudio calls the callback function in a separate thread.
def callback(in_data, frame_count, time_info, status):

    global TT, yy, roll_vel, yaw_vel, IMUVec
    global output_file, current_data, left, right

    current_data.set_TT(TT)  # store current time in RTData object
    current_data.set_data(roll_vel, yaw_vel, IMUVec, trialType, yy, WiaSL_mark, Homing_mark)  # store current data in RTData object
    # check output file, with yy index, if missing something. ?
    left, right = current_data.get_RTdata()  # get each ear's sound
    # Apply Change
    data[0::2] = left  # store left ear data in data's even indexes
    data[1::2] = right  # store right ear data in data's odd indexes
    TT += IMUtosound.FRAMES / float(IMUtosound.RATE)  # update time by adding it frames/rate ratio

    # RT log
    yy += 1  # update callback counter

    return data, pyaudio.paContinue


""" Streaming Initialization """

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open PyAudio's stream
stream = p.open(format=pyaudio.paFloat32,
                channels=IMUtosound.CHANNELS,
                rate=IMUtosound.RATE,
                output=True,
                frames_per_buffer=IMUtosound.FRAMES,
                # output_device_index=outputDeviceIndex,
                stream_callback=callback)

stream.start_stream()

# Connect to the IMU device
imu_component = IMUComponent.IMUComponent(port_num=portNum,
                                          baud_rate=921600,
                                          parity='None',
                                          num_of_bits=8,
                                          stop_bit=1,
                                          time_out_in_ms=100)

imu_component.MakeOperational()

ii = 0  # loop counter
start_time = time.time()  # set the program starting time after opening the stream
elpased_time = 0  # how long the program will run
roll_vel_vec = np.zeros(20)  # last 20 velocities for average
yaw_vel_vec = np.zeros(20)  # last 20 velocities for average
temp_yy = yy


# Main loop that keeps reading velocities from IMU and allows callback to play sound
# while elpased_time < 660:
while GUI.appOngoing():
    ii += 1

    # write to output file whenever yy is changed
    if temp_yy != yy:
        temp_yy = yy
        output_file.appendData(current_data, yy)

    # get the IMU packet (with all the information it collects in RT)
    IMUVec = imu_component.GetPacket()

    # pitch velocity from IMU: IMUVec[0]
    # yaw velocity from IMU: IMUVec[1]
    # roll velocity from IMU: IMUVec[2]

    # get roll velocity from IMU (as pitch)
    roll_vel_curr = round(IMUVec[2])
    # calculate the averaged velocity of last length(roll_vel_vec) velocities
    roll_vel = IMUtosound.vel_avg(roll_vel_vec, roll_vel_curr)

    # get yaw velocity from IMU (as volume)
    yaw_vel_curr = round(IMUVec[1])
    # calculate the averaged velocity of last length(yaw_vel_vec) velocities
    yaw_vel = IMUtosound.vel_avg(yaw_vel_vec, yaw_vel_curr)

    # calculate the time passed
    elpased_time = round((time.time() - start_time), 3)
    trialType = Trials.trial(elpased_time)  # call the trial handler to activate it whenever required
    QCoreApplication.processEvents()  # process all pending events for the calling thread

    # check for marks
    WiaSL_mark = Trials.mark()
    Homing_mark = Trials.Homing_mark()

QCoreApplication.processEvents()  # process all pending events for the calling thread

# Close PyAudio stream
stream.stop_stream()
stream.close()
p.terminate()

# Updating the remaining data
output_file.appendData(current_data, round(yy))

# Update output file
output_file.updateOutputfile(yy)

# Create the Beam CSV containing the collected data regarding the Beam trials (irrelevant for Navigation Experiment)
output_file.createCSVFile()

# Create the CSV containing the collected data during this run, organized by trials
data_dir = output_file.getFilenameDir()
OrganizeByTrials.run(data_dir)

# Create the CSV containing the distance Error data for each trial
DistanceErrorFile.create_CSV(data_dir)
