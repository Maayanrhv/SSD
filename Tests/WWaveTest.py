import time

import pyaudio
import numpy as np

p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 0.4   # in seconds, may be float
f = 880.0        # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)


# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# play. May repeat with different volume values (if done interactively)
start_time = time.time()
elpasedtime = 0
increaseFreqToMiddle = False
increaseFreqToEnd = False

while elpasedtime < 4:
    elpasedtime = (round((time.time() - start_time), 3))
    stream.write(volume*samples)
    print(f)

    if increaseFreqToMiddle:
        if f < 740 or increaseFreqToEnd:
            f = f + 20.0
            if f == 880:
                break
        else:
            increaseFreqToEnd = True
            increaseFreqToMiddle = False
            f = f - 20.0
    else:
        if f > 600:
            f = f - 20.0
        else:
            increaseFreqToMiddle = True
            f = f + 20.0

    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

stream.stop_stream()
stream.close()

p.terminate()
