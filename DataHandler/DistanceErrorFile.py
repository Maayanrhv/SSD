import os
import csv

# This script creates a CSV of each trial's distances error data.

# Error - The distances errors after the navigational tasks (irrelevant for Balance)
titled_trials_counter = []  # the trial's serial number - to keep track of the trial that is related to the errors.
diagonal_error = []  # error 1 - the distance from where the subject stopped to the goal point.
horizontal_error = []  # error 2 - the horizontal distance from where the subject stopped to the straight line.
vertical_error = []  # error 3 - the vertical distance from where the subject stopped to the straight line.

# Distance Errors in the task of Walking in a Straight Line when the subject walks back to the starting point.
# The errors are the same as before, only relative to the starting point instead of the goal point.
back_diagonal_error = []  # error 1
back_horizontal_error = []  # error 2
back_vertical_error = []  # error 3


# Accept the errors from GUI and add them to the lists of errors.
# Input: - diagonal_dist_err - the diagonal distance error value of a specific trial (double type)
#        - horizontal_err - the horizontal distance error value of a specific trial (double type)
#        - vertical_err - the vertical distance error value of a specific trial (double type)
def set_distance_errors(diagonal_dist_err, horizontal_err, vertical_err, back_diag, back_horiz, back_vert):
    global diagonal_error, horizontal_error, vertical_error
    global back_diagonal_error, back_horizontal_error, back_vertical_error

    diagonal_error.append(diagonal_dist_err)
    horizontal_error.append(horizontal_err)
    vertical_error.append(vertical_err)

    if not back_diag:
        back_diag = '-'
    if not back_horiz:
        back_horiz = '-'
    if not back_vert:
        back_vert = '-'
    back_diagonal_error.append(back_diag)
    back_horizontal_error.append(back_horiz)
    back_vertical_error.append(back_vert)


# Create a matrix that will be saved as a csv file later on.
# The matrix will include all the error data we collected and organized in the global lists for each trial.
def create_mat():
    titled_trials_counter = list(range(1, len(diagonal_error) + 1))
    titled_trials_counter.insert(0, "Trial Number")

    titled_diagonal = diagonal_error
    titled_diagonal.insert(0, "Error 1 - Diagonal Distance")

    titled_horizontal = horizontal_error
    titled_horizontal.insert(0, "Error 2 - Horizontal Distance")

    titled_vertical = vertical_error
    titled_vertical.insert(0, "Error 3 - Vertical Distance")

    titled_backwards_diagonal = back_diagonal_error
    titled_backwards_diagonal.insert(0, "Backwards Error 1")

    titled_backwards_horizontal = back_horizontal_error
    titled_backwards_horizontal.insert(0, "Backwards Error 2")

    titled_backwards_vertical = back_vertical_error
    titled_backwards_vertical.insert(0, "Backwards Error 3")

    return [p for p in zip(titled_trials_counter, titled_diagonal, titled_horizontal, titled_vertical,
                           titled_backwards_diagonal, titled_backwards_horizontal, titled_backwards_vertical)]


# Create a csv file containing the error data organized by trials.
def create_CSV(dir_path):
    mat = create_mat()
    csv_name = "Distance Errors.csv"
    # keep the csv file in the current experiment's directory
    csv_path = os.path.join(dir_path, csv_name)
    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerows(mat)
