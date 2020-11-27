import csv
from scipy.io import wavfile as wav
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt


# Global Variables
MAXVEL = 120

# For each pitch-rotation velocity (degrees per second) between -120 to 120,
# there's a matching sound between the frequencies 2000-20000 (?),
# with jumps of 10 (?) from one velocity value to the next.
# That is, for example: -120 deg/sec = 2000 Hz
#                       -119 deg/sec = 2100 Hz
#                       -118 deg/sec = 2200 Hz
#                       ...
#                       119 deg/sec = 19900 Hz
#                       120 deg/sec = 20000 Hz
# Formally: pitch_velocity*10 + 2000
def set_sound_from_given_pitch_rotation(pitch_velocity):
    # define the rate with which to create the sound
    # rate = 44100
    # define the frequency of this given pitch velocity
    normalizedVel = pitch_velocity / MAXVEL
    frequency = normalizedVel * 3276700
    # create an array of the generated frequency with the defined rate for 1ms
    # frequency_array = np.array([frequency]*rate)
    # return frequency_array
    return frequency


# Read the file in which there are the velocities of the pitch head-rotations.
def read_csv(filename):
    with open(filename, newline='') as f_input:
        return [list(map(float, row)) for row in csv.reader(f_input)]


def frecuency_generator(pitchVelocity, mono, maxVelocity=None):
    if maxVelocity is None:
        maxVelocity = pitchVelocity.max()
    relativePitchVel = pitchVelocity/maxVelocity
    volumePitchVel = relativePitchVel * mono[0:len(pitchVelocity)]
    return volumePitchVel


def main():
    # Read velocity input from Data#.csv
    velocityInput = np.asarray(read_csv('Data5.csv'))

    # Take only the velocity data from Gy column
    # (that represents the pitch head-rotation)
    pitchVelocity = velocityInput[:, 1]

    # Read the sound values (data) from the given wav file
    # rate=44100
    # rawSound = the sound numeral values (data)
    rate, rawSound = wav.read('500Hz.wav')

    # Create a basic sound window vector
    window = rawSound[0:rate, 2]

    # Compute frequency-velocity feature
    pitchFrequency = frecuency_generator(pitchVelocity, window)
    # pitchFrequency = np.array([])
    # onems = rate / 100
    # limit = len(pitchVelocity)/25
    # for i in range(int(limit)):
    #     prevFreq = set_sound_from_given_pitch_rotation(pitchVelocity[i])
    #     pitchFrequency = np.append(pitchFrequency, np.repeat(prevFreq, onems))

    # play the sound of this given velocity
    sd.play(pitchFrequency, rate)

    # for i in range(120, 0, -1):
    #     set_sound_from_given_pitch_rotation(i)


if __name__ == '__main__':
    # create an array of sound (white noise)
    # data = np.random.uniform(-1, 1, 44100)  # 44100 random samples between -1 and 1
    # scaled = np.int16(data / np.max(np.abs(data)) * 32767)

    # created an array sized 44100 with the same frequency of 32767.
    # pitchFrequency = np.int16(np.repeat(32767, 44100))
    # sd.play(pitchFrequency, 44100)

    rate, rawSound500Clean = wav.read('500HzClean.wav')
    rate, rawSound500 = wav.read('500Hz.wav')
    rate, rawSound1000 = wav.read('1000Hz.wav')
    # plt.plot(rawSound)
    # plt.show()
    # a = a.round().astype('int16')
    a = rawSound1000/rawSound500
    sd.play(rawSound500, 44100)
    sd.play(rawSound1000, 44100)
    main()
