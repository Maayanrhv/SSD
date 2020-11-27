import csv
import wave

import numpy as np
import pygame as pg
import time
import pyaudio

# samples per second
import scipy.io.wavfile

import IMUComponent

RATE = 44100
# Duration in seconds
DURATION = 0.05  # 50ms
# Minimum velocity to play sound
# MIN_VEL = 6


def initiate():
    # Initiate py-game mixer to create sound object later
    pg.mixer.init()
    pg.init()

    p = pyaudio.PyAudio()
    pyaudiostream = p.open(format=pyaudio.paFloat32,
                           channels=2,
                           rate=44100,
                           frames_per_buffer=1024,
                           output=True,
                           output_device_index=3
                           )

    # imu_component = initiate_IMU()
    # return imu_component, pyaudiostream
    return pyaudiostream, p


def initiate_IMU():
    # Create an IMU Component
    imu_component = IMUComponent.IMUComponent(port_num='COM4',
                                              baud_rate=921600,
                                              parity='None',
                                              num_of_bits=8,
                                              stop_bit=1,
                                              time_out_in_ms=100)
    # Connect to the IMU and make it operational
    imu_component.MakeOperational()

    return imu_component


# Read the file in which there are the velocities of the pitch head-rotations.
def read_csv(filename):
    with open(filename, newline='') as f_input:
        return [list(map(float, row)) for row in csv.reader(f_input)]


def frequency_to_sound(frequency):
    each_sample_number = np.arange(DURATION * RATE)
    waveform = np.sin(2 * np.pi * each_sample_number * frequency / RATE)
    waveform_quiet = waveform * 0.3
    # waveform_integers = np.int16(waveform_quiet * 32767)
    # return waveform_integers
    return waveform_quiet

def velocity_to_frequency(velocity):
    frequency = round(velocity) * 10 + 440
    # Frequency / pitch of the sine wave
    # frequency = 440.0
    return frequency


def play_sound(waveform):
    two_ears_sound = np.array([waveform, ] * 2)
    two_ears_sound = np.reshape(two_ears_sound, (np.size(waveform), 2))
    sound_obj = pg.sndarray.make_sound(two_ears_sound)
    sound_obj.play()


def read_velocity_from_csv(pyaudioStream, p):
    # Read velocity input from Data#.csv
    velocity_input = np.asarray(read_csv('Data5.csv'))

    # Take only the velocity data from Gy column
    # (that represents the pitch head-rotation)
    pitch_velocity = velocity_input[:, 1]

    for vel in pitch_velocity:
        # Compute velocity-to-frequency feature
        freq = velocity_to_frequency(vel)
        # Compute frequency-to-sound waveform
        waveform = frequency_to_sound(freq)
        # play sound of this wave
        # scipy.io.wavfile.write('wf.wav', RATE, waveform.astype(np.float32))
        # wf = wave.open('C:\\Users\\user\\PycharmProjects\\SSD\\wf.wav', 'rb')
        # # define callback (2)
        # def callback(in_data, frame_count, time_info, status):
        #     data = wf.readframes(frame_count)
        #     return data, pyaudio.paContinue
        # # open stream using callback (3)
        # stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
        #                 channels=wf.getnchannels(),
        #                 rate=wf.getframerate(),
        #                 output=True,
        #                 stream_callback=callback)
        #
        # # start the stream (4)
        # stream.start_stream()
        # # wait for stream to finish (5)
        # while stream.is_active():
        #     time.sleep(0.1)
        #
        # # stop stream (6)
        # stream.stop_stream()
        # stream.close()
        # wf.close()

        pyaudioStream.write(waveform.astype(np.float32).tostring())
        # play_sound(waveform)


def read_velocity_from_imu(imu_component):
    while True:
        # get current velocities vector
        # gy = vec[0]
        # gz = vec[1]
        # gx = vec[2]
        # ay = vec[4]
        # az = vec[5]
        # ax = vec[6]
        vec = imu_component.GetPacket()
        # Compute velocity-to-frequency feature
        freq = velocity_to_frequency(vec[0])
        # Compute frequency-to-sound waveform
        waveform = frequency_to_sound(freq)
        # play sound of this wave
        play_sound(waveform)
        # Sleep
        # time.sleep(0.1)


def main():
    # Initiate program
    # imu_component = initiate()
    pyaudiostream, p = initiate()

    # Read velocity information
    read_velocity_from_csv(pyaudiostream, p)
    # read_velocity_from_imu(imu_component)

    # close PyAudio
    p.terminate()
    pyaudiostream.close()


if __name__ == '__main__':
    main()
