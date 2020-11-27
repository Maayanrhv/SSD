import os
import csv

# This script creates a CSV of each trial's distances error data.

# Error - The distances errors after the navigational tasks (irrelevant for Balance)
titled_trials_counter = []  # the trial's serial number - to keep track of the trial that is related to the errors.
remaining_distance_error = []  # the distance from where the subject stopped to the horizontal end line.
straying_error = []  # the distance from where the subject stopped to the original straight line.


# Accept the errors from GUI and add them to the lists of errors.
# Input: - remaining_dist_err - the remaining distance error value of a specific trial (double type)
#        - stray_err - the straying distance error value of a specific trial (double type)
def set_distance_errors(remaining_dist_err, stray_err):
    global remaining_distance_error, straying_error
    remaining_distance_error.append(remaining_dist_err)
    straying_error.append(stray_err)


# Create a matrix that will be saved as a csv file later on.
# The matrix will include all the error data we collected and organized in the global lists for each trial.
def create_mat():
    titled_trials_counter = list(range(1, len(remaining_distance_error) + 1))
    titled_trials_counter.insert(0, "Trial Number")

    titled_remaining_distance = remaining_distance_error
    titled_remaining_distance.insert(0, "Remaining Distance Error")

    titled_straying = straying_error
    titled_straying.insert(0, "Straying Distance Error")

    return [p for p in zip(titled_trials_counter, titled_remaining_distance, titled_straying)]


# Create a csv file containing the error data organized by trials.
def create_CSV(dir_path):
    mat = create_mat()
    csv_name = "Distance Errors.csv"
    # keep the csv file in the current experiment's directory
    csv_path = os.path.join(dir_path, csv_name)
    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerows(mat)
