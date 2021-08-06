from DataHandler import Cleaner


class TrialInfo:
    def __init__(self, num, type, start, end, length):
        self.trial_num = num
        self.trial_type = type
        self.start = start
        self.end = end
        self.trial_indexes_length = length


# a pair of indexes that represent the start and end of each part of a task where the participant walked by herself.
class Pair:
    def __init__(self, start=-1, end=-1):
        self.start = start
        self.end = end


# Holds all the data of a single participant
class Participant:
    def __init__(self, participant_num, participant_id):
        # Dependencies
        self.trials_to_ignore = []  # some trials could not be used due to different reasons

        # Flags
        self.wiasl_mark_exists = False  # some trials didn't have wiasl mark
        self.homing_mark_exists = False  # some trials didn't have homing mark
        self.homing_indexes_flag = []  # indicating where were homing trials in Distance Errors.csv file
        self.with_sound_indexes_flag = []  # indicating where were trials with sound in Distance Errors.csv file

        # Meta Data
        self.num = participant_num  # serial number of the participant

        # Data
        # Data that's organized per trial
        # taken from read_trials_data_file.csv
        self.trial_num = []
        self.trial_file_num = []
        self.trial_index = []
        self.trial_type = []
        self.freq_sin = []
        self.time = []
        self.vol_left = []
        self.yy = []
        self.pitch_gy = []
        self.yaw_gz = []
        self.roll_gx = []
        self.y_left_right = []
        self.z_up_down = []
        self.x_forward_backward = []

        self.trials_info_list = []  # keeping all trials data in a list of TrialsInfo-s
        # a list of Pair-s indicating for each trial:
        # the index when the trial started (when the participant started walking alone)
        # and the index when the wiasl-forward mark was on (when the participant reached the goal point)
        self.wiasl_mark_forward = []
        # a list of Pair-s indicating for each trial:
        # the index when the wiasl-backward mark was on (when the participant started walking back to the goal point)
        # and the index when the trial ended (when the participant reached the starting point)
        self.wiasl_mark_backward = []
        # a list of Pair-s indicating for each trial:
        # the index when the homing mark started (when the participant started walking alone)
        # and the index when the trial ended
        self.homing_mark_indexes = []

        self.roll_velocities_hom = []
        self.yaw_velocities_hom = []
        self.roll_velocities_for = []
        self.yaw_velocities_for = []
        self.roll_velocities_back = []
        self.yaw_velocities_back = []

        # taken from read_hdf5_files
        # currently unused
        # self.sound_L = []  # fullDataL
        # self.sound_R = []  # fullDataR
        # self.roll_avg_vel = []  # pitchVelVec
        # self.yaw_avg_vel = []  # rollVelVec

        # taken from read_distance_errors_file
        # Data that's organized per trial
        self.error_1_diagonal = []
        self.error_2_horizontal = []
        self.error_3_vertical = []
        self.error_1_diagonal_backward = []
        self.error_2_horizontal_backward = []
        self.error_3_vertical_backward = []

        self.trial_type_short_list = []

    # Data that's organized per trial and taken from read_trials_data_file.csv
    def set_data_from_trials_data(self, trial_num, file_num, trial_indexes, trial_type, freq, time, vol_left, yy,
                                  pitch_gy, yaw_gz, roll_gx, y_left_right, z_up_down, x_forward_backward, homing_mark,
                                  wiasl_mark):
        self.trial_num = trial_num
        self.trial_file_num = file_num
        self.trial_index = trial_indexes
        self.trial_type = trial_type
        self.freq_sin = freq
        self.time = time
        self.vol_left = vol_left
        self.yy = yy
        self.pitch_gy = pitch_gy
        self.yaw_gz = yaw_gz
        self.roll_gx = roll_gx
        self.y_left_right = y_left_right
        self.z_up_down = z_up_down
        self.x_forward_backward = x_forward_backward

        self.set_trials_start_end_indexes()

        self.set_homing_mark(homing_mark)
        self.set_wiasl_mark(wiasl_mark)

        self.set_roll_velocities()
        self.set_yaw_velocities()

    def set_trials_start_end_indexes(self):
        curr_trial_num = 0

        # collecting data for TrialInfo
        t_num = 0
        t_type = 0
        t_start_idx = 0
        i = 0

        for i in range(len(self.trial_num)):
            if self.trial_num[i] == 1 and curr_trial_num != self.trial_num[i]:
                curr_trial_num += 1
                t_num = self.trial_num[i]
                t_type = self.trial_type[i]
                t_start_idx = i

            elif curr_trial_num != self.trial_num[i]:
                # creating previous trial
                t_end_idx = i - 1
                t_length = t_end_idx - t_start_idx + 1
                self.trials_info_list.append(TrialInfo(t_num, t_type, t_start_idx, t_end_idx, t_length))

                # moving on to current trial
                curr_trial_num = self.trial_num[i]
                t_num = self.trial_num[i]
                t_type = self.trial_type[i]
                t_start_idx = i

        # creating previous trial
        t_end_idx = i
        t_length = t_end_idx - t_start_idx + 1
        self.trials_info_list.append(TrialInfo(t_num, t_type, t_start_idx, t_end_idx, t_length))

    # Data that's organized per trial and taken from read_trials_data_file.csv
    def set_wiasl_mark(self, wiasl_mark):
        if wiasl_mark[0] == -1:
            self.wiasl_mark_exists = False
            return
        self.wiasl_mark_exists = True
        one_found = False
        for ti in self.trials_info_list:
            for i in range(ti.start, ti.end+1):
                if wiasl_mark[i] == 1.0 and not one_found:
                    self.wiasl_mark_forward.append(Pair(ti.start, i))
                    one_found = True
                elif wiasl_mark[i] == 2.0 and one_found:
                    self.wiasl_mark_backward.append(Pair(i, ti.end))
                    break
            if not one_found:
                # this trial is not a wiasl task trial, so we want to add an empty pair to the list (-1,-1)
                self.wiasl_mark_forward.append(Pair())
                self.wiasl_mark_backward.append(Pair())
            one_found = False

        Cleaner.clean_wiasl_marks(self, wiasl_mark)

    # Data that's organized per trial and taken from read_trials_data_file.csv
    def set_homing_mark(self, homing_mark):
        if homing_mark[0] == -1:
            self.homing_mark_exists = False
            return
        self.homing_mark_exists = True
        found_mark = False
        for ti in self.trials_info_list:
            for i in range(ti.start, ti.end+1):
                if homing_mark[i] == 1.0:
                    found_mark = True
                    self.homing_mark_indexes.append(Pair(i, ti.end))
                    break
            if not found_mark:
                # this trial is not a homing task trial, so we want to add an empty pair to the list (-1,-1)
                self.homing_mark_indexes.append(Pair())
            found_mark = False

        Cleaner.clean_homing_marks(self)

    # Data that's organized per trial and taken from read_distance_errors_file
    def set_distance_errors(self, err_1_dia, err_2_hor, err_3_ver, err_1_dia_back, err_2_hor_back, err_3_ver_back):
        self.error_1_diagonal = err_1_dia
        self.error_2_horizontal = err_2_hor
        self.error_3_vertical = err_3_ver
        self.error_1_diagonal_backward = err_1_dia_back
        self.error_2_horizontal_backward = err_2_hor_back
        self.error_3_vertical_backward = err_3_ver_back

    def set_homing_indexes_flag(self, homing_idx):
        self.homing_indexes_flag = homing_idx

    def set_with_sound_indexes_flag(self, with_sound_idx):
        self.with_sound_indexes_flag = with_sound_idx

    def set_trial_type_short_list(self, trial_type_short_list):
        self.trial_type_short_list = trial_type_short_list

    def set_roll_velocities(self):
        if self.homing_mark_exists:
            for pair in self.homing_mark_indexes:
                if pair.start != -1:
                    self.roll_velocities_hom.append(list(self.roll_gx[pair.start:pair.end + 1]))
                else:
                    self.roll_velocities_hom.append([])
        if self.wiasl_mark_exists:
            for pair in self.wiasl_mark_forward:
                if pair.start != -1:
                    self.roll_velocities_for.append(list(self.roll_gx[pair.start:pair.end + 1]))
                else:
                    self.roll_velocities_for.append([])
            for pair in self.wiasl_mark_backward:
                if pair.start != -1:
                    self.roll_velocities_back.append(list(self.roll_gx[pair.start:pair.end + 1]))
                else:
                    self.roll_velocities_back.append([])

    def set_yaw_velocities(self):
        if self.homing_mark_exists:
            for pair in self.homing_mark_indexes:
                if pair.start != -1:
                    self.yaw_velocities_hom.append(list(self.yaw_gz[pair.start:pair.end + 1]))
                else:
                    self.yaw_velocities_hom.append([])
        if self.wiasl_mark_exists:
            for pair in self.wiasl_mark_forward:
                if pair.start != -1:
                    self.yaw_velocities_for.append(list(self.yaw_gz[pair.start:pair.end + 1]))
                else:
                    self.yaw_velocities_for.append([])
            for pair in self.wiasl_mark_backward:
                if pair.start != -1:
                    self.yaw_velocities_back.append(list(self.yaw_gz[pair.start:pair.end + 1]))
                else:
                    self.yaw_velocities_back.append([])
