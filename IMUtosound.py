import numpy as np
import h5py
import math


"""
Globals
"""
# The array length of each wave.
# Needs to be short as possible to keep the sound changes congruent with the velocity changes,
# but not too short to keep the sound changes smooth.
RATE = 44100  # The sound sampling rate for one second (44.1ms)
FRAMES = 256  # 256 frames = 256*1000/44100 = 5.8ms ~ 6ms

CHANNELS = 2
vecStart = 10

global a, b, shift, y0, yf, x0, xf  # parameters for the velocity-to-frequency function

"""
Velocity To Volume Section
"""


# Determine the volume changes ratio.
# Input: vel - yaw velocity
#        denominator - determines the range of the velocities.
#        Ex: a velocity of 100 or above will have the highest volume when tha denominator is 100.
# Output: Temporary volume value between 0-1 of the left ear (the right ear will be 1-output respectively)
# Logic: Divide a given yaw velocity by a maximum value to convert it to a value between 0-1 and return that value.
def vel_to_vol(vel, denominator=75):
    vel_vol = round(vel / denominator, 2)  # round the quotient to one decimal. Ex: 0.6
    vel_vol = round(vel_vol, 2)  # round vel_vol to two decimal. Ex: 0.60

    vol_left_temp = 0.5 + vel_vol  # setting the volume to be around 0.5 (or relative to 0.5)
    # ensure the velocity is between 0-1 and round the velocity to three decimal. Ex: 0.600
    current_left_vol = round(float(np.clip(vol_left_temp, 0, 1)), 3)

    return current_left_vol


# Determine the volume changes logic.
# Input: left_vol - temporary yaw left volume
#        prev_left_vol - the previous yaw volume
# Output: left_vol_vec - the left volumes change array
#         right_vol_vec - the right volumes change array
#         current_left_vol - the current left volume.
#         The latter parameter is for the next volume change as a reference (the current volume will become
#         the previous one in the next calling of this function).
# Logic: Gradually change the volume from the previous one to the current one in both ears, by stretching
#        the volume range in each ear across the amount of frames.
#        Ex: an array of volumes change across the range of 0.1 to 0.4 with 4 frames will be: [0.1, 0.2, 0.3, 0.4]
def vol_vec(left_vol, prev_left_vol):
    current_left_vol = left_vol
    diff_vol = prev_left_vol - current_left_vol  # the difference between the current and the previous volumes
    if diff_vol != 0:  # in case there's been a change in the movement
        # gradually change the volumes from the previous one to the current one by stretching this volume range across
        # the amount of frames.
        left_vol_vec = np.arange(prev_left_vol, current_left_vol, (diff_vol / FRAMES) * -1, np.float32)
        prev_right_vol = 1 - prev_left_vol  # the corresponding previous right volume
        current_right_vol = 1 - current_left_vol  # the corresponding current right volume
        right_vol_vec = np.arange(prev_right_vol, current_right_vol,
                                  ((prev_right_vol - current_right_vol) / FRAMES) * -1, np.float32)
    else:  # in case there hasn't been a change in the movement
        # create an array with the same current volume in each frame (its size is thus the number of frames).
        # there's an array like this for each ear with its own current volume.
        left_vol_vec = np.zeros(FRAMES) + current_left_vol
        right_vol_vec = np.zeros(FRAMES) + 1 - current_left_vol

    return left_vol_vec, right_vol_vec, current_left_vol


"""
Velocity To Frequency Section
"""


# Determine the frequency changes logic.
# Input: Range of possible frequencies (between high and low values)
# Logic: Create a logarithmic function that will represent the transformation of velocity to frequency.
#        The function chosen is logarithmic due to human logarithmic hearing of frequencies.
#        f(x) = a * log(x + shifter) + b
#        The head rotation velocities range from about -150 to 150, so that is the range of the X axis of the function
#        (though mathematically there's no limit).
#        The corresponding frequencies range (Y axis) was chosen so that it will be pleasant for human hearing.
def vec_to_freq_function(high=554.3522, low=103.8262):
    global a, b, shift, y0, yf, x0, xf
    yf = high  # the highest frequency allowed
    y0 = low  # the lowest frequency allowed
    x0 = -150  # the lowest velocity
    xf = 150  # the highest velocity
    shift = 440  # a number to add to the velocities to shift the curve in order to avoid negative values
    a = (yf - y0) / (math.log(((xf + shift) / (x0 + shift)), 10))  # find a using 2 points: (x0,y0),(xf,yf)
    b = yf - a * math.log(xf + shift, 10)  # find b using a and one point: (xf,yf)


# Returns the parameters of the frequency function.
def get_vec_to_freq_func_param():
    return round(y0), round(yf), x0, xf


# Determine the frequency value according to a given velocity by using a logarithmic function.
# Input: vel - roll velocity
# Output: freq - frequency value between the high and low limits determined. No difference between ears.
def vel_to_freq(vel):
    # in case the velocity's lower than -shift, change it to be -(shift-1) - that is the lowest value allowed.
    if (vel*-1) > shift:
        vel = (shift-1) * -1

    temp_freq = a * math.log(vel + shift, 10) + b  # use the logarithmic function to find the current frequency
    temp_freq = round(temp_freq)  # round the frequency to lower a bit the frequency changes sensitivity
    freq = np.clip(temp_freq, y0, yf)  # ensure the calculated frequency doesn't exceed the limits determined

    return freq


# Create an array of the n-th previous velocities (to later calculate their average velocity).
# Input: vel_avg_vec - an array containing the last n velocities (this array's length is n).
#        vel - the new velocity to add to this array instead of the oldest one (but with FIFO insert method).
# Output: vel_avg_vec - the given array after the required modification: removing the oldest velocity
#         in it and adding the newest to it.
def vel_avg(vel_avg_vec, vel):
    # move the entire array one index to the left (lose the first value)
    # note: the last value of the array stays unchanged.
    vel_avg_vec[:-1] = vel_avg_vec[1:]
    vel_avg_vec[-1] = vel  # change the last value of the array to be vel (the new velocity)

    return np.average(vel_avg_vec)


"""
Adaptations of Frequencies and Volume to the Produced Complete Sound
"""


# Create a sinus wave of the current frequency that continues the previous frequency's sinus wave.
# Input: phase - the phase of the previous sinus wave
#        freq - the current frequency
#        TT - current time, global parameter
# Output: a sinus wave formed according to the current frequency that continues the previous frequency's sinus wave.
def freq_sin(rtdata):
    phase, freq, TT=rtdata.get_freq_sin_val()
    return np.sin(phase + 2 * np.pi * freq * (TT + np.arange(FRAMES) / float(RATE)))


"""
Output File Section
"""


# Calculate the root mean square of the data. Usable in analysis.
def rms(data):
    return np.sqrt(np.mean(data ** 2))


# Decipher the binary data file and enable reading it.
# Input: path - the file path to read.
# Output: the file object.
def read_from_file(path):
    return h5py.File(path, 'r')


# Initialize the parameters needed for the output file.
def init_params():
    data = np.zeros(FRAMES * 2, np.float32)  # the current sound that is played through callback
    roll_vel = 0  # the pitch velocity given from the IMU
    yaw_vel = 0  # the roll velocity given from the IMU
    IMU_vec = np.zeros(6)  # the IMU data collected in RT (real-time)
    return data, roll_vel, yaw_vel, IMU_vec