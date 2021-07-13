import time
import wave

import pyaudio
import numpy as np


p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer, Record at 44100 samples per second
duration = 3   # in seconds, may be float
# sine frequency, Hz, may be float
# f = 103.8262
# f = 329.0892
f = 554.3522

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paFloat32  # 32 bits per sample
np_format = np.float32
channels = 2

# name = str(int(f))
# filename = name + ".wav"

# device_index = 2
#
# print("----------------------record device list---------------------")
# info = p.get_host_api_info_by_index(0)
# numdevices = info.get('deviceCount')
# for i in range(0, numdevices):
#         if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
#             print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
# print("-------------------------------------------------------------")
#
# index = int(input())
# print("recording via index "+str(index))


# generate samples, note conversion to float32 array
samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np_format)

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                # input_device_index=index,
                input=True,
                output=True)

frames = []  # Initialize array to store frames

# play. May repeat with different volume values (if done interactively)
start_time = time.time()
elpasedtime = 0

while elpasedtime < 4:
    elpasedtime = (round((time.time() - start_time), 3))
    # stream.write(volume * samples)
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np_format)

    stereo_signal = np.zeros([len(samples), 2])
    # 1 for right speaker, 0 for left
    stereo_signal[:, 0] = samples[:]  # only left ear
    # stereo_signal[:, 1] = samples[:]  # only right ear

    stereo_signal = stereo_signal.flatten()
    stream.write(stereo_signal.astype(np_format).tostring())

# # Store data in chunks for 3 seconds
# for i in range(0, int(fs / chunk * duration)):
#     data = stream.read(chunk)
#     frames.append(data)

stream.stop_stream()
stream.close()

p.terminate()

# # Save the recorded data as a WAV file
# wf = wave.open(filename, 'wb')
# wf.setnchannels(channels)
# wf.setsampwidth(p.get_sample_size(sample_format))
# wf.setframerate(fs)
# wf.writeframes(b''.join(frames))
# wf.close()
