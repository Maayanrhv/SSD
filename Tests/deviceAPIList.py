
import numpy as np
#import pyaudioexclusive as pyaudio
import pyaudio

p=pyaudio.PyAudio()

print("Devices:")
ii=0
while (ii<(p.get_device_count())):
    print(p.get_device_info_by_index(ii))
    ii=ii+1

print("Host Api:")
ii=0
while(ii<(p.get_host_api_count())):
    print(p.get_host_api_info_by_index(ii))
    ii = ii + 1

isSupported=p.is_format_supported(rate=44100,output_channels=2,output_device=2,output_format=pyaudio.paInt32)
print(isSupported)
#isSupported = p.is_format_supported(input_format=pyaudio.paInt8, input_channels=1, rate=22050, input_device=0)
