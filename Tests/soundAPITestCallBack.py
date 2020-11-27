import pyaudio
import time
import RTdata as rt
import IMUtosound

TT = time.time()  # The current date and time
startTT = TT  # The starting time
yy = 0  # callback counter
IMUtosound.vec_to_freq_function(500) # Initialize the function that transforms velocity to frequency
data, roll_vel, yaw_vel, IMUVec=IMUtosound.init_params() #start values
current_data=rt.RTdata(startTT)

def callback(in_data, frame_count, time_info, status):

    global TT,yy,current_data,left,right

    currentData.set_TT(TT)
    currentData.set_data(roll_vel, yaw_vel, IMUVec)
    left,right=currentData.get_RTdata()
    #print(rollVel)
    # Apply Change
    #print(left[0:10])
    data[0::2] = left  # left ear data
    data[1::2] = right  # right ear data
    TT += IMUtosound.FRAMES / float(IMUtosound.RATE)

    # RT log
    yy += 1
    # add current data to log file
    return data, pyaudio.paContinue


p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
#stream = p.open(format=pyaudio.paInt16,
#stream = p.open(format=pyaudio.paInt32,
                channels=2,
                rate=48000,
                output=True,
                frames_per_buffer=48,
                output_device_index=8,
                stream_callback=callback
                )


ii = 0  # loop counter
start_time = time.time() # set the program starting time
elpasedtime = 0 # how long the program will run
prevtime=0
# main loop that keeps reading velocities from IMU and allows callback to stream sound
while elpasedtime < 5:
    ii += 1
    elpasedtime = (round((time.time() - start_time), 3))
    if elpasedtime-prevtime==1:
        print (elpasedtime)
        prevtime=elpasedtime

# Close PyAudio stream
stream.stop_stream()
stream.close()
p.terminate()