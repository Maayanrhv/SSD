import matplotlib.pyplot as plt
import IMUtosound

filename1 = IMUtosound.read_from_file("Output\\FullData_2020-03-23 19-19-56.479.hdf5")

pitchVelVec1 = filename1['IMUMat'][1:, 0]
yawVelVec1 = filename1['IMUMat'][1:, 1]
freqVecShort1 = filename1['freq_sin'][255:]
timeVec1 = filename1['timeVec'][255:]
volLeftVec1 = filename1['volLeftVec'][255:]

# Subplot all signal data and explot it
fig = plt.figure()
gs = fig.add_gridspec(4, 3)

# Pitch Velocity
ax1 = fig.add_subplot(gs[0, 0:2])
ax1.plot(timeVec1, pitchVelVec1)
ax1.set_xlabel("Time")
ax1.set_ylabel("Pitch Velocity")
ax1.set_ylim(-200, 200)

# Pitch Hertz
ax2 = fig.add_subplot(gs[1, 0:2])
ax2.plot(timeVec1, freqVecShort1)
ax2.set_xlabel("Time")
ax2.set_ylabel("Frequency")
ax2.set_ylim(100, 1600)


# Yaw Velocity
ax3 = fig.add_subplot(gs[2, 0:2])
ax3.plot(timeVec1, yawVelVec1)
ax3.set_xlabel("Time")
ax3.set_ylabel("Yaw Velocity")
ax3.set_ylim(-200, 200)


# Volume Level Right
ax4 = fig.add_subplot(gs[3, 0:2])
ax4.plot(timeVec1, volLeftVec1)
ax4.set_xlabel("Time")
ax4.set_ylabel("Volume Left")

rmsPitch1 = IMUtosound.rms(pitchVelVec1)
rmsYaw1 = IMUtosound.rms(yawVelVec1)

tx3 = fig.add_subplot(gs[0, 2])
plt.setp(plt.gca(), frame_on=False, xticks=(), yticks=())
plt.text(0, 0.8, "RMS Pitch Velocity: "+str(round(rmsPitch1, 3)))
plt.text(0, 0.4, "RMS Yaw Velocity: "+str(round(rmsYaw1, 3)))

plt.tight_layout()
plt.show()

