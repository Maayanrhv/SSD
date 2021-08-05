import numpy as np
from DataHandler import Participant


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


# clean wiasl marks
def clean_wiasl_marks(participant, wiasl_mark):
    if participant.num == 7:
        # trial 27 includes only the goal point without any marks.
        ti = participant.trials_info_list[26]
        participant.wiasl_mark_forward[26] = Participant.Pair(ti.start, ti.end)
        participant.wiasl_mark_backward[26] = Participant.Pair()

    elif participant.num == 8:
        # trial 35 includes only the goal point without any marks.
        ti = participant.trials_info_list[34]
        participant.wiasl_mark_forward[34] = Participant.Pair(ti.start, ti.end)
        participant.wiasl_mark_backward[34] = Participant.Pair()

    elif participant.num == 9:
        # Trial 33 is a miss trial so it needs to be disregarded
        participant.wiasl_mark_forward[32] = Participant.Pair()
        participant.wiasl_mark_backward[32] = Participant.Pair()

    elif participant.num == 10:
        # in trial 18, backward mark (2) started too late (when trial ended). Should be ~3 seconds earlier.
        pair = participant.wiasl_mark_backward[17]
        participant.wiasl_mark_backward[17] = Participant.Pair(pair.start - 60, pair.end)

    elif participant.num == 12:
        # trial 7 includes only the goal point without any marks.
        ti = participant.trials_info_list[6]
        participant.wiasl_mark_forward[6] = Participant.Pair(ti.start, ti.end)
        participant.wiasl_mark_backward[6] = Participant.Pair()

    elif participant.num == 13:
        # trial 10 includes only the goal point without any marks.
        ti = participant.trials_info_list[9]
        participant.wiasl_mark_forward[9] = Participant.Pair(ti.start, ti.end)
        participant.wiasl_mark_backward[9] = Participant.Pair()

    elif participant.num == 17:
        # Trial 26 is a miss trial so it needs to be disregarded
        participant.wiasl_mark_forward[25] = Participant.Pair()
        participant.wiasl_mark_backward[25] = Participant.Pair()

        # trial 29 includes only the goal point without any marks.
        ti = participant.trials_info_list[28]
        participant.wiasl_mark_forward[28] = Participant.Pair(ti.start, ti.end)
        participant.wiasl_mark_backward[28] = Participant.Pair()

        # trial 30 includes only the goal point without any marks.
        ti = participant.trials_info_list[29]
        one_found = False
        for i in range(ti.start, ti.end + 1):
            if wiasl_mark[i] == 2.0 and not one_found:
                participant.wiasl_mark_forward[29] = Participant.Pair(ti.start, i)
                one_found = True
            elif wiasl_mark[i] == 1.0 and one_found:
                participant.wiasl_mark_backward[29] = Participant.Pair(i, ti.end)
                break

    elif participant.num == 32:
        # Trial 17 is a miss trial so it needs to be disregarded
        participant.wiasl_mark_forward[16] = Participant.Pair()
        participant.wiasl_mark_backward[16] = Participant.Pair()


# clean homing marks
def clean_homing_marks(participant):
    if participant.num == 9:
        # Trial 33 is a miss trial so it needs to be disregarded
        participant.homing_mark_indexes[32] = Participant.Pair()

    if participant.num == 17:
        # Trial 26 is a miss trial so it needs to be disregarded
        participant.homing_mark_indexes[25] = Participant.Pair()

    elif participant.num == 23:
        # trial 15 ended earlier than specified,
        # but we don't know how early, so we can't use this trial for swaying calculations.
        participant.homing_mark_indexes[14] = Participant.Pair()

        # trial 19 ended earlier than specified,
        # but we don't know how early, so we can't use this trial for swaying calculations.
        participant.homing_mark_indexes[18] = Participant.Pair()

    elif participant.num == 27:
        # trial 25 is a wiasl mark but homing mark was mistakenly pressed, so we remove this homing mark.
        participant.homing_mark_indexes[24] = Participant.Pair()

    elif participant.num == 31:
        # trial 26 is a wiasl mark but homing mark was mistakenly pressed, so we remove this homing mark.
        participant.homing_mark_indexes[25] = Participant.Pair()

    elif participant.num == 32:
        # Trial 17 is a miss trial so it needs to be disregarded
        participant.homing_mark_indexes[16] = Participant.Pair()
