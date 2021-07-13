import numpy as np


# clean a participant's trials data
def clean_trials_data(participant_num, data_mat):
    if participant_num == 11:
        # 609 rows
        start_idx_10 = 6227
        end_idx_10 = 6835
        # 705 rows
        start_idx_29 = 19461
        end_idx_29 = 20165
        # saving the data of the trials that are needed to be swapped
        ten = data_mat[start_idx_10:end_idx_10 + 1, :]
        twenty_nine = data_mat[start_idx_29:end_idx_29 + 1, :]
        ten[:, 0] = 29
        twenty_nine[:, 0] = 10
        # deleting those trials from the data matrix
        data_mat = np.delete(data_mat, np.s_[start_idx_10:end_idx_10 + 1], 0)
        new_start_idx_29 = start_idx_29 - 609
        data_mat = np.delete(data_mat, np.s_[new_start_idx_29:new_start_idx_29 + 705], 0)
        # adding each trial data (sub matrix) in the other's position in the data matrix
        data_mat = np.insert(data_mat, start_idx_10, twenty_nine, 0)
        new_start_idx_29 = new_start_idx_29 + 705
        data_mat = np.insert(data_mat, new_start_idx_29, ten, 0)

    return data_mat


#  clean a participant's errors data
def clean_errors_data(participant, data_mat):
    participant_num = participant.num

    if participant_num == 9:
        # Trial 33 is a miss trial
        data_mat = np.delete(data_mat, 32, 0)
        participant.trial_type_short_list.pop(32)

    elif participant_num == 11:
        # Trial 10 was 'C no sound' but the subject performed 'A no sound', so I switched it with trial 29
        data_mat[[9, 28]] = data_mat[[28, 9]]
        participant.trial_type_short_list[9], participant.trial_type_short_list[28] = \
            participant.trial_type_short_list[28], participant.trial_type_short_list[9]

    elif participant_num == 17:
        # Trial 26 is a miss trial
        data_mat = np.delete(data_mat, 25, 0)
        participant.trial_type_short_list.pop(25)

    elif participant_num == 32:
        # Trial 17 is a miss trial
        data_mat = np.delete(data_mat, 16, 0)
        participant.trial_type_short_list.pop(16)

    # 1) convert backward errors from string to int
    # 2) determine whether a row (trial) is a wiasl task or a homing task
    # 3) determine whether a row (trial) is a task with or without sound
    is_homing = False
    homing_indx = np.zeros(len(data_mat))
    with_sound_indx = np.zeros(len(data_mat))
    for row in range(len(data_mat)):
        for col in range(len(data_mat[0])):
            val = data_mat[row][col]
            if val == '-':
                data_mat[row][col] = -1
                is_homing = True
            else:
                data_mat[row][col] = int(data_mat[row][col])
        if is_homing:
            homing_indx[row] = 1
        is_homing = False

        if participant.trial_type_short_list[row] % 2 != 0:
            # this trial is with sound
            with_sound_indx[row] = 1

    participant.set_homing_indexes_flag(homing_indx)
    participant.set_with_sound_indexes_flag(with_sound_indx)

    return data_mat
