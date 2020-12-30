import numpy as np
import RTdata as rt
import GUI
from enum import Enum
import random
from random import randint, choice

# All trial types
# Even - No sound
# Odd - With sound

# # For Balance Experiment
# trialTypes = {
#   0: "No Trial",
#   1: "Beam 5' EOP With Sound",
#   2: "Beam 5' EOP No Sound",
#   3: "OLS EOP With Sound R",
#   4: "OLS EOP No Sound R",
#   5: "Beam 5' ECL With Sound",
#   6: "Beam 5' ECL No Sound",
#   7: "OLS ECL With Sound R",
#   8: "OLS ECL No Sound R",
#   9: "OLS ECL With Sound L",
#   10: "OLS ECL No Sound L",
#   11: "OLS EOP With Sound L",
#   12: "OLS EOP No Sound L",
# }

# For Navigation Experiment
trialTypes = {
  0: "No Trial",
  1: "WiaSL EOP With Sound",  # task 1 EOP sound
  2: "WiaSL EOP No Sound",  # task 1 EOP no sound
  3: "Homing EOP With Sound",  # task 2 EOP sound (For training only)
  4: "Homing EOP No Sound",  # task 2 EOP no sound (For training only)
  5: "WiaSL ECL With Sound",  # task 1 ECL sound
  6: "WiaSL ECL No Sound",  # task 1 ECL no sound
  7: "Homing ECL With Sound A",  # task 2 ECL sound Shape A
  8: "Homing ECL No Sound A",  # task 2 ECL no sound Shape A
  9: "Homing ECL With Sound B",  # task 2 ECL sound Shape B
  10: "Homing ECL No Sound B",  # task 2 ECL no sound Shape B
  11: "Homing ECL With Sound C",  # task 2 ECL sound Shape C
  12: "Homing ECL No Sound C",  # task 2 ECL no sound Shape C
  13: "Homing ECL With Sound D",  # task 2 ECL sound Shape D
  14: "Homing ECL No Sound D",  # task 2 ECL no sound Shape D
}

trialStatus = {
  1: "Pending",
  2: "Ready",
  3: "Ongoing",
  4: "Finished",
}

# The colors match the trial status by the number
# Ex: pending trial will be red
#     ongoing trial will be blue
trialStatusColor = {
  1: "red",
  2: "orange",
  3: "blue",
  4: "green",
}


class ExpMode(Enum):
    Training = 0
    Test = 1
    Manual = 2

# Function for Balance Experiment
# def updateTrialListRightLeft():
#     # OLS
#     trialsRep[np.where(trialsRep == 7)] = 8
#     trialsRep[np.where(trialsRep == 9)] = 8
#     trialsRep[np.where(trialsRep == 10)] = 8
#
#     OLSIndexs = np.where(trialsRep == 8)[0]
#     # Start with R/L
#     RLchoice = np.random.choice([0, 1])
#     RLOrder = np.array([[0, 1], [1, 0]])
#     # create the R/L Vector
#     RLVec = (np.tile(RLOrder[RLchoice], int(len(OLSIndexs) / 2))) * 2
#     # add the vector to the current trials
#     trialsRep[OLSIndexs] = trialsRep[OLSIndexs] + RLVec
#     # With Sound/No Sound
#
#     # Right Leg
#     OLSIndexsRight = np.where(trialsRep == 8)[0]
#     soundCondVec = np.repeat([1, 0], len(OLSIndexsRight) / 2)
#     np.random.shuffle(soundCondVec)
#     trialsRep[OLSIndexsRight] = trialsRep[OLSIndexsRight] - soundCondVec
#
#     # Left Leg
#     OLSIndexsLeft = np.where(trialsRep == 10)[0]
#     soundCondVec = np.repeat([1, 0], len(OLSIndexsLeft) / 2)
#     np.random.shuffle(soundCondVec)
#     trialsRep[OLSIndexsLeft] = trialsRep[OLSIndexsLeft] - soundCondVec


# At program start, the trials to run are set to be test trials.
expMode = ExpMode.Test  # initialized to test mode

# Prepare trials to run
# in case of test mode
if expMode == ExpMode.Test:
    # updateTrialListRightLeft()  # for Balance Experiment
    numberOfTrialsPerType_W = 5  # each trial type repeats numberOfTrialsPerType times (for WiaSL task)
    TrialTypesToRun_W = [5, 6]  # trial types to run (set to be test trial types, not training)
    numberOfTrialsPerType_H = 3  # each trial type repeats numberOfTrialsPerType times (for Homing task)
    TrialTypesToRun_H = [7, 8, 9, 10, 11, 12, 13, 14]  # trial types to run (set to be test trial types, not training)

    # duplicate each trial numberOfTrialsPerType times
    trialsRep_temp_W = np.repeat(TrialTypesToRun_W, numberOfTrialsPerType_W)
    trialsRep_temp_H = np.repeat(TrialTypesToRun_H, numberOfTrialsPerType_H)
    trialsRep = np.append(trialsRep_temp_W, trialsRep_temp_H)
    np.random.shuffle(trialsRep)  # shuffle the trials randomly
    trialsRep = np.append(trialsRep, [1, 2])
    trialNum = len(trialsRep)  # total amount of test trials
    trialsIndexes = np.arange(0, trialNum)  # list of trials' indexes

# in case of training mode
elif expMode == ExpMode.Training:
    TrialTypesToRun = [1, 2, 3, 4, 5, 6]  # trial types to run are set to be training trial types (not test)
    EOPIndexes = [1, 2, 3, 4, 11, 12]  # opened-eyes trials indexes
    ECLIndexes = [5, 6, 7, 8, 9, 10]  # closed-eyes trials indexes
    trialsRep = EOPIndexes + ECLIndexes  # all training trials types are all types
    np.random.shuffle(trialsRep)  # shuffle the trials randomly
    trialNum = len(trialsRep)  # amount of trials in training mode
    trialsIndexes = np.arange(0, trialNum)   # list of trials' indexes

# in case of manual mode
else:
    trialsRep = [7, 9, 7, 9, 8, 6]  # trial types to run are set to be training trial types (not test)
    trialNum = len(trialsRep)  # amount of trials in training mode
    trialsIndexes = np.arange(0, trialNum)  # list of trials' indexes


trialsStatVec = np.ones(trialNum)  # setting all trials statuses to 'Pending'
trialsStatVec[0] += 1  # change the first trial to 'Ready'

global trials_displayed_list  # strings list where each string contains details of a trial to be displayed later

# End trial manually (end-trial button value)
# global endTrialByClick
endTrial = False  # initialize to a not-ended trial status

# trial Time
# global trialOngoing, trialStatusLast, trialTime, startTrialTime, afterBeep, trialCounter, trialType
trialOngoing = False  # is-trial-ongoing indicator
trialPrevStatus = False  # keep track on previous status to prevent overly-calling start-trial condition in trial func
trialTime = 0  # how much time the trial lasted in seconds
startTrialTime = 0  # when the trial starts
playBeep = False  # a flag to determine whether to play beep sound or not
trialCounter = 0  # to keep track on the current trial and its details
trialType = 0  # the current trial type


# Runs the trial in callback thread when a trial should start.
# Note: this function's called on each callback iteration, so it is important to play relevant sounds only when needed.
def trial(elpasedtime):
    global trialTime, trialCounter, playBeep, startTrialTime, trialType
    # in case start-trial button was clicked and
    if should_start_trial():
        startTrialTime = elpasedtime  # keep the time at which the trial was started
        print("Trial Started at:", startTrialTime)
        playBeep = True  # allow playing beep sound to indicate the trial's starting
        rt.set_sound_status(rt.Sound.NoSound)  # turn off all sounds when the beep sound is played

    # play beep sound
    if trialTime < 1 and playBeep:  # the first condition ensures that the beep will be played only at trial's start
        # ensure beep sound is played separately for each beep.
        if (int(trialTime * 10) % 3) == 0:
            rt.set_sound_status(rt.Sound.NoSound)
        else:
            rt.set_sound_status(rt.Sound.Beep)

    # start trial after beeps
    if trialTime > 2 and playBeep:
        trialType = get_trial_type(trialCounter)
        print("Trial Type:", trialType, trialTypes[trialType])
        playBeep = False

        # start trial sound by trial type (with sound - 1,3 no sound - 2,4)
        if (trialType % 2) == 0:
            rt.set_sound_status(rt.Sound.NoSound)
        else:
            rt.set_sound_status(rt.Sound.Combined)
        print("Trial is Ongoing")

    # finish trial
    if trialTime > 62 or endTrial:  # end trial automatically after 1 minute (from the second it started)
        print("Trial finished at {:.2f} and lasted {:.2f} seconds".format(elpasedtime, trialTime))
        trialTime = 0  # reset the trial time for the next trial
        end_trial()  # call end-trial function to handle necessary details
        rt.set_sound_status(rt.Sound.Combined)  # replay SSD sound in-between trials
        trialType = 0  # set the trial type state to no-trial
        set_end_trial(False)  # change ending-trial flag to false for next trial

    # keep track on the how much time had passed since the trial has started until this current callback iteration
    if trialOngoing:
        trialTime = elpasedtime - startTrialTime
        set_trial_time(trialTime)

    # set previous status = ongoing to know that the last status was 'ongoing'
    set_trial_prev_status()

    return trialType


# Return trials list
def get_trials_list():
    return trialsRep


# Determine whether to start the trial or not
# Logic: start trial only if the trial status was changed.
def should_start_trial():
    global trialPrevStatus, trialOngoing
    start_trial = False
    # compare the trial's previous status to the current one
    # if its status was changes - then the trial should be started
    if trialPrevStatus != trialOngoing:
        start_trial = True
    return start_trial


# This function's called when the start-trial button is clicked.
# It prepares the trial before it starts.
def start_trial_by_click():
    # changing this flag will start the trial
    set_trial_ongoing(True)

    global trialCounter
    # change the trial status from 'Ready' to 'Ongoing'
    if trialsStatVec[trialCounter] == 2:  # if trial is in 'Ready' status
        trialsStatVec[trialCounter] += 1  # then change its status to 'Ongoing'
    else:
        print("Can't change trial's status to 'Ongoing' since it is not in 'Ready' state.")


# Set the ending-trial details when trial needs to end (upon end-trial button click for example)
def end_trial():
    set_trial_ongoing(False)
    print("end Trial setTrialOngoing {}".format(is_trial_ongoing()))
    global trialCounter

    # changing trial from 'Ongoing' to 'Finished'
    if trialsStatVec[trialCounter] == 3:
        trialsStatVec[trialCounter] += 1
        trialCounter += 1
        if trialCounter < trialNum:
            trialsStatVec[trialCounter] += 1
        # update gui
        GUI.win.showTrials()


# Reset previous status to ongoing
def set_trial_prev_status():
    global trialPrevStatus, trialOngoing
    trialPrevStatus = trialOngoing


# Determine whether to end trial or not according to the given value
def set_end_trial(boolean_val):
    global endTrial
    endTrial = boolean_val


# Set how much time the trial lasted
def set_trial_time(time):
    global trialTime
    trialTime = time


# Return the trial type index according to the requested index in the trials list
def get_trial_type(index):
    return trialsRep[index]


# Set trial-ongoing status on/off
def set_trial_ongoing(boolean_val):
    global trialOngoing
    trialOngoing = boolean_val
    if trialOngoing:
        print("Trial's status changed to Ongoing")


# Return boolean - whether the trial is ongoing or not
def is_trial_ongoing():
    global trialOngoing
    return trialOngoing


# Creating a list of trials to display
def update_rows():
    global trials_displayed_list
    trials_displayed_list = []  # initialize to an empty list
    # create each trial's string (that represents its details)
    for index in trialsIndexes:
        row = str(trialsIndexes[index] + 1)  # trial's string starts with its serial number
        row += ".  " + trialTypes[trialsRep[index]]  # then add to the string the trial type's title
        row += "\t" + trialStatus[trialsStatVec[index]]  # finally add to the string the trial's current status
        trials_displayed_list.append(row)  # add string to the matrix of strings that will be displayed on screen
