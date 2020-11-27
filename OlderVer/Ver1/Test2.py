import numpy as np

freqByAverageFlag = 0

def velAvg(velAvgVec,vel):
    velAvgVec[:-1] = velAvgVec[1:]
    velAvgVec[-1] = vel
    return velAvgVec


pitchVelVec=np.zeros(10)
count = 0
for i in range(-100, 100):
    pitchVelCurr=i
    pitchVelVec=velAvg(pitchVelVec,pitchVelCurr)
    roll_vel=np.average(pitchVelVec)
    count += 1
