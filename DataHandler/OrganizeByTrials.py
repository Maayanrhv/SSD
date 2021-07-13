import h5py
import os
import csv

# This script creates a csv file that contains all the data that was collected during an experiment, such that
# the data can be easily read per trial. Namely, the sound, velocities, volume, time and other features are presented
# per trial.


# a class to contain the information about one trial's indexes across all hdf5 files.
# For a specific trial, this class keeps the following details:
#   - two indexes - the trial's start and end indexes.
#   - a list of the files' numbers (the number that appears at the beginning of each file's name).
#   - a list of the trial's length in each file. The trial's length is the amount of indexes it spread through in the
#     trialType list in one file. So, for each file there kept the length of the trial (in case it spread across
#     multiple files.
#   - a list of lists, where each sublist contains the indexes in which the trial took place.
# Example: Let's assume one trial spread across two files, where each file contains 600 sized lists, the trial started
# in index 400 of the first trial and in the second file the trial ended after 100 indexes.
# Thus, this class' parameters will be:
#   - self.start = 400
#   - self.end = 99
#   - self.file_num = [0, 1]
#   - self.indexes_length_per_file = [200, 100]
#   - self.indexes_per_file = [[400, 401, 402,..., 598, 599], [0, 1, 2,..., 98, 99]]
import numpy as np


class TrialIndexInfo:
    def __init__(self, type, start, end=None):
        self.trial_type = type
        self.start = start
        self.end = end
        self.file_num = []
        self.indexes_length_per_file = []
        self.indexes_per_file = []

    def get_trial_type(self):
        return self.trial_type

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_file_num(self):
        return self.file_num

    def get_indexes_length(self):
        return self.indexes_length_per_file

    def get_indexes_per_file(self):
        return self.indexes_per_file

    def set_start(self, value):
        self.start = value

    def set_end(self, value):
        self.end = value

    def add_file_details(self, file_num, indexes_length, start_in_file, end_in_file):
        self.file_num.append(file_num)
        self.indexes_length_per_file.append(indexes_length)
        self.indexes_per_file.append(list(range(start_in_file, end_in_file+1)))


# Global lists that contain the data for each trial
trials_indexes = []  # a list of all trials' indexes info described in TrialIndexInfo class
freq_sin_values = []  # a list of all trials' frequency values
full_data_L = []  # a list of all trials' sound played in left ear
full_data_R = []  # a list of all trials' sound played in right ear
time_vec = []  # a list of all trials' time array
vol_left_vec = []  # a list of all trials' volumes in left ear
yy = []  # a list of all trials' yy values
IMUMat = []  # a matrix of all trials' IMU velocities
remaining_error = []  # a list of each trial's remaining distance error value
straying_error = []  # a list of each trial's straying distance error value
paths_list = []  # a list of all the data files created during the experiment
splitted_trial = False  # a flag indicating whether a trial is splitted to multiple files
trial_to_handle = 0
increase_trial_counter_by = 0
global dir_path  # the directory path (is used to reach the relevant directory that contains the relevant data files)
global tii  # one trial's TrialIndexInfo class (is used for splitted trials)

trial_type_short_list = []

# Read all files one by one in order to take the needed information from each of them.
def read_files():
    file_num = 0
    # read data from each h5py file
    for name in paths_list:
        full_path = os.path.join(dir_path, name)
        f = h5py.File(full_path, 'r')
        # print(list(f.keys()))
        # organize this file's data by trials
        organize_data_by_trials(f, file_num)
        file_num += 1


# Organize the given file's data by trials.
# Input: - f - the file
#        - file_num - the given file's number
def organize_data_by_trials(f, file_num):
    global trials_indexes, freq_sin_values, full_data_L, full_data_R, time_vec, vol_left_vec, yy, IMUMat
    global trial_to_handle
    # get all trials' indexes info
    couple_trials_start_and_end_indexes(f, file_num)

    # get all trials' frequency sine wave value
    freq_sin_values.extend(get_trials_frequency_value(f))

    # get all trials' sound values in left ear
    # full_data_L.extend(get_trials_full_data_L(f))

    # get all trials' sound values in right ear
    # full_data_R.extend(get_trials_full_data_R(f))

    # get all trials' time period
    time_vec.extend(get_trials_time_vec(f))

    # get all trials' sound volume on left ear (the corresponding right ear is 1-left)
    vol_left_vec.extend(get_trials_vol_left_vec(f))

    # get all trials' yy values
    yy.extend(get_trials_yy(f))

    # get all trials' velocities data (IMUMat)
    IMUMat.extend(get_trials_IMU_velocities(f))

    trial_to_handle += increase_trial_counter_by


# Find all the indexes that contain trials' data.
# Input: - f - the file
#        - file_num - the given file's number
def couple_trials_start_and_end_indexes(f, file_num):
    global trials_indexes, splitted_trial, tii

    # check if a trial is splitted to determine whether to look for a starting index or not
    if splitted_trial:
        is_start_index = False
    else:
        is_start_index = True

    start_index = 0
    values_counter = 0  # counts the indexes in the file
    max_index = len(f["trialType"]) - 1  # the maximal index in the file

    # go over each value in the trialType list that stores which trial type was run in each cell/sample.
    # a value of 0 represent 'no trial' mode.
    for val in f["trialType"]:
        # in case we're looking for a new trial in the file
        if is_start_index:
            # in case we reached some kind of trial
            if val != 0:
                # store its starting index
                start_index = values_counter
                # declare we no longer are searching for a new trial (until we'll end handling it)
                is_start_index = False
                # initiate the TrialIndexInfo global variable to store the starting index and value
                tii = TrialIndexInfo(val, start_index)
        # in case we already have a trial to handle, we need to find its ending index
        else:
            # in case we reached the current trial's ending index
            if val == 0:
                # if the current val is 0, then the previous val was the last trial value, so we store the previous
                # val' index as the end index
                end_index = values_counter - 1
                # the length of the trial in this specific file (if it's splitted, start_index = 0 as it should be)
                index_length = end_index-start_index + 1
                # since we reached the trial's end, we can now search for the next trial, so we reset the relevant flag
                is_start_index = True
                # in case the trial is splitted
                if splitted_trial:
                    # reset the splitted flag to indicate we're no longer handling a splitted trial
                    splitted_trial = False
                    # set our global TrialIndexInfo start, end, length and file number variables
                    tii.set_end(end_index)
                    tii.add_file_details(file_num, index_length, start_index, end_index)
                    trials_indexes.append(tii)
                    del tii
                # in case the trial is not splitted (and is contained completely in the given file)
                else:
                    # set our global TrialIndexInfo start, end, length and file number variables
                    tii.set_end(end_index)
                    tii.add_file_details(file_num, index_length, start_index, end_index)
                    trials_indexes.append(tii)
                    del tii
            elif values_counter == max_index:
                # if val isn't 0 and we reached the end of the list, it mean that:
                # there's a start index but no end index, and that mean the trial continues in next file
                # and it needs to be handled
                splitted_trial = True
                tii.add_file_details(file_num, values_counter - start_index + 1, start_index, max_index)

        values_counter += 1


# Get all trials' frequencies
# Input: - f - the file
def get_trials_frequency_value(f):
    global trial_to_handle, increase_trial_counter_by

    freq_sin_values = []

    # Go over each trial and add its frequencies to list

    # in case we have a complete trial data (we reached the trial's end)
    if trials_indexes:
        temp_counter = trial_to_handle
        temp_i = 0
        for i in range(temp_counter, len(trials_indexes)):
            pair = trials_indexes[i]
            freq_sin_values.extend(f["freq_sin"][pair.get_indexes_per_file()[-1]])
            temp_i += 1
        increase_trial_counter_by = temp_i
    # in case there's a a splitted trial which didn't end yet
    if "tii" in globals():
        indexes_of_data = tii.get_indexes_per_file()[-1]
        freq_sin_values.extend(f["freq_sin"][indexes_of_data])

    return freq_sin_values


# Get all trials' sound values in the left ear
# Input: - f - the file
def get_trials_full_data_L(f):
    global trial_to_handle

    full_data_L = []

    # Go over each trial and add its sound values in the left ear to list

    # in case we have a complete trial data (we reached the trial's end)
    if trials_indexes:
        temp_counter = trial_to_handle
        for i in range(temp_counter, len(trials_indexes)):
            pair = trials_indexes[i]
            full_data_L.extend(f["fulldataL"][pair.get_indexes_per_file()[-1]])
    # in case there's a a splitted trial which didn't end yet
    if "tii" in globals():
        indexes_of_data = tii.get_indexes_per_file()[-1]
        full_data_L.extend(f["fulldataL"][indexes_of_data])

    return full_data_L


# Get all trials' sound values in the right ear
# Input: - f - the file
def get_trials_full_data_R(f):
    global trial_to_handle

    full_data_R = []

    # Go over each trial and add its sound values in the right ear to list

    # in case we have a complete trial data (we reached the trial's end)
    if trials_indexes:
        temp_counter = trial_to_handle
        for i in range(temp_counter, len(trials_indexes)):
            pair = trials_indexes[i]
            full_data_R.extend(f["fulldataR"][pair.get_indexes_per_file()[-1]])
    # in case there's a a splitted trial which didn't end yet
    if "tii" in globals():
        indexes_of_data = tii.get_indexes_per_file()[-1]
        full_data_R.extend(f["fulldataR"][indexes_of_data])

    return full_data_R


# Get all trials' time vector
# Input: - f - the file
def get_trials_time_vec(f):
    global trial_to_handle

    time_vec = []

    # Go over each trial and add its time vector to list

    # in case we have a complete trial data (we reached the trial's end)
    if trials_indexes:
        temp_counter = trial_to_handle
        for i in range(temp_counter, len(trials_indexes)):
            pair = trials_indexes[i]
            time_vec.extend(f["timeVec"][pair.get_indexes_per_file()[-1]])
    # in case there's a a splitted trial which didn't end yet
    if "tii" in globals():
        indexes_of_data = tii.get_indexes_per_file()[-1]
        time_vec.extend(f["timeVec"][indexes_of_data])

    return time_vec


# Get all trials' volume vector in left ear
# Input: - f - the file
def get_trials_vol_left_vec(f):
    global trial_to_handle

    vol_left_vec = []

    # Go over each trial and add its volume vector in left ear to list

    # in case we have a complete trial data (we reached the trial's end)
    if trials_indexes:
        temp_counter = trial_to_handle
        for i in range(temp_counter, len(trials_indexes)):
            pair = trials_indexes[i]
            vol_left_vec.extend(f["volLeftVec"][pair.get_indexes_per_file()[-1]])
    # in case there's a a splitted trial which didn't end yet
    if "tii" in globals():
        indexes_of_data = tii.get_indexes_per_file()[-1]
        vol_left_vec.extend(f["volLeftVec"][indexes_of_data])

    return vol_left_vec


# Get all trials' yy values
# Input: - f - the file
def get_trials_yy(f):
    global trial_to_handle

    yy = []

    # Go over each trial and add its yy values to list

    # in case we have a complete trial data (we reached the trial's end)
    if trials_indexes:
        temp_counter = trial_to_handle
        for i in range(temp_counter, len(trials_indexes)):
            pair = trials_indexes[i]
            yy.extend(f["yy"][pair.get_indexes_per_file()[-1]])
    # in case there's a a splitted trial which didn't end yet
    if "tii" in globals():
        indexes_of_data = tii.get_indexes_per_file()[-1]
        yy.extend(f["yy"][indexes_of_data])

    return yy


# Get all trials' velocities data (IMUMat)
# Input: - f - the file
def get_trials_IMU_velocities(f):
    global trial_to_handle

    IMUMat = []

    # Go over each trial and add its IMUMat values to list

    # in case we have a complete trial data (we reached the trial's end)
    if trials_indexes:
        temp_counter = trial_to_handle
        for i in range(temp_counter, len(trials_indexes)):
            pair = trials_indexes[i]
            IMUMat.extend(f["IMUMat"][pair.get_indexes_per_file()[-1]])
    # in case there's a a splitted trial which didn't end yet
    if "tii" in globals():
        indexes_of_data = tii.get_indexes_per_file()[-1]
        IMUMat.extend(f["IMUMat"][indexes_of_data])

    return IMUMat


# Create a matrix that will be saved as a csv file later on.
# The matrix will include all the data we collected and organized in the global lists for each trial.
def create_mat():
    trials_counter = 1
    titled_trials_counter = []
    titled_trial_all_indexes = []
    titled_trial_file_num = []
    titled_trial_type = []

    for trial_info in trials_indexes:
        trial_type = trial_info.get_trial_type()
        files_num = trial_info.get_file_num()
        indexes_length_per_file = trial_info.get_indexes_length()
        indexes_per_file = trial_info.get_indexes_per_file()

        # add trial type to shortened list to keep in a seperate file
        trial_type_short_list.append(trial_type)

        titled_trials_counter.extend([trials_counter]*sum(indexes_length_per_file))

        temp_files_num = [[fn] * l for fn, l in zip(files_num, indexes_length_per_file)]
        titled_trial_file_num.extend([num for sublist in temp_files_num for num in sublist])  # flatten the list

        temp_indexes = [indexes for indexes in indexes_per_file]
        titled_trial_all_indexes.extend([num for sublist in temp_indexes for num in sublist])  # flatten the list

        titled_trial_type.extend([trial_type] * sum(indexes_length_per_file))

        # titled_trials_counter.extend([trials_counter]*indexes_counter)
        # titled_trial_all_indexes.extend(list(range(start, end+1)))
        # titled_trial_file_num.extend([pair.get_file_num()]*indexes_counter)

        trials_counter += 1

    titled_trials_counter.insert(0, "Trial Number")
    titled_trial_file_num.insert(0, "Trial File Number")
    titled_trial_all_indexes.insert(0, "Trial Indexes")
    titled_trial_type.insert(0, "Trial Type")

    titled_freq_sin_values = freq_sin_values
    titled_freq_sin_values.insert(0, "Freq Sin Values")

    # titled_full_data_L = full_data_L
    # titled_full_data_L.insert(0, "Full Data Left")
    #
    # titled_full_data_R = full_data_R
    # titled_full_data_R.insert(0, "Full Data Right")

    titled_time_vec = time_vec
    titled_time_vec.insert(0, "Time Vec")

    titled_vol_left_vec = vol_left_vec
    titled_vol_left_vec.insert(0, "Volume Left Vec")

    titled_yy = yy
    titled_yy.insert(0, "yy")

    titled_gy = [row[0] for row in IMUMat]
    titled_gy.insert(0, "Pitch gy")

    titled_gz = [row[1] for row in IMUMat]
    titled_gz.insert(0, "Yaw gz")

    titled_gx = [row[2] for row in IMUMat]
    titled_gx.insert(0, "Roll gx")

    titled_y = [row[3] for row in IMUMat]
    titled_y.insert(0, "y axis Left-Right")

    titled_z = [row[4] for row in IMUMat]
    titled_z.insert(0, "z axis Up-Down")

    titled_x = [row[5] for row in IMUMat]
    titled_x.insert(0, "x axis Forward-Backward")

    # return [p for p in zip(titled_trials_counter, titled_trial_file_num, titled_trial_all_indexes,
    #                        titled_freq_sin_values, titled_full_data_L, titled_full_data_R, titled_time_vec,
    #                        titled_vol_left_vec, titled_yy)]
    return [p for p in zip(titled_trials_counter, titled_trial_file_num, titled_trial_all_indexes, titled_trial_type,
                           titled_freq_sin_values, titled_time_vec, titled_vol_left_vec, titled_yy, titled_gy,
                           titled_gz, titled_gx, titled_y, titled_z, titled_x)]


# Create a csv file containing the data organized by trials.
def create_CSV(mat):
    csv_name = "trials_data.csv"
    # keep the csv file in the current experiment's directory
    csv_path = os.path.join(dir_path, csv_name)
    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerows(mat)


def create_CSV_for_trial_type_short_list():
    csv_name = "trial_type_short_list.csv"
    titled_list = trial_type_short_list
    titled_list.insert(0, "trial_type")
    # keep the csv file in the current experiment's directory
    csv_path = os.path.join(dir_path, csv_name)
    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerows(zip(trial_type_short_list))


# Main function to run this script.
def main():
# def run(exp_dir):
    global paths_list, dir_path

    # if this function is run from this script:
    # Count how many data files there are (of type: '.hdf5')
    parent_directory = os.path.split(os.getcwd())[0]
    dir_path = os.path.join(parent_directory, "Output\\33 - 2021-03-16-09-03-02 - Manar Mahamid - 208217406")

    # else: if this function is run from RTIMUToSound script:
    # dir_path = exp_dir

    path = os.listdir(dir_path)

    # file_num = 0
    # for name in path:
    #     if name.endswith(".hdf5"):
    #         file_num += 1
    #         paths_list.append(name)

    count = 0
    for name in path:
        if name.endswith(".hdf5"):
            count += 1
    temp = list(np.zeros(count))
    for name in path:
        if name.endswith(".hdf5"):
            file_num = int(name[:2])
            temp[file_num] = name
    paths_list = temp

    # print(paths_list)
    # file_num = len([name for name in path if name.endswith(".hdf5")])

    read_files()
    mat = create_mat()
    # create_CSV(mat)
    create_CSV_for_trial_type_short_list()


if __name__ == "__main__":
    main()
