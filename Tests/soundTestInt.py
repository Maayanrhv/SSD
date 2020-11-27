import pyaudio
import numpy as np
import time
from math import pi, sin, log, exp
import matplotlib.pyplot as plt


p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
# duration = 5.0   # in seconds, may be float
duration = 0.5   # in seconds, may be float
f = 200.0        # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
#samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32).tobytes()

samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs))*32768.0
# plt.plot(np.arange(fs*duration), samples.T)
# plt.show()
# print(samples)

#samples=samples.astype(np.int32)
samples=samples.astype(np.int16)
#samples=samples.astype(np.float32)
samples=samples.tobytes()

# for paFloat32 sample values must be in range [-1.0, 1.0]
#stream = p.open(format=pyaudio.paFloat32,
stream = p.open(format=pyaudio.paInt16,
                channels=2,
                output_device_index=3,
                rate=fs,
                output=True)

elpasedtime = 0  # how long the program will run
prevtime=0
ii=0
start_time = time.time() # set the program starting time


#  a function that goes from 1 to 10Hz in 5 seconds using 1000 samples:
def sweep(f_start, f_end, interval, n_steps):
    b = log(f_end/f_start) / interval
    a = 2 * pi * f_start / b
    # samples = []
    for i in range(n_steps):
        delta = i / float(n_steps)
        t = interval * delta
        g_t = a * exp(b * t)
        # samples.append(g_t)
        # print(t, 3 * sin(g_t))
    # return samples


# samples = np.array(sweep(200, 400, 5, 1000)).astype(np.int16).tobytes()

while elpasedtime < 10:
    ii += 1
    elpasedtime = (round((time.time() - start_time), 3))
    stream.write(samples)
    # print(elpasedtime)

    # samples = (np.sin(2 * np.pi * np.arange(fs * duration) * (f - 10.0) / fs)) * 32768.0

    # if elpasedtime-prevtime == 1:
    #     print(elpasedtime)
    #     prevtime = elpasedtime
# play. May repeat with different volume values (if done interactively)


stream.stop_stream()
stream.close()

p.terminate()
