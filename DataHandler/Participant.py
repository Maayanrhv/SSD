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
        self.id = participant_id  # the participant's identification number

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

        # taken from read_hdf5_files
        self.wiasl_mark_forward_ended_indexes = []
        self.wiasl_mark_backward_started_indexes = []
        self.homing_mark_participant_started_alone_indexes = []
        # currently unused
        self.sound_L = []  # fullDataL
        self.sound_R = []  # fullDataR
        self.roll_avg__vel = []  # pitchVelVec
        self.yaw_avg_vel = []  # rollVelVec

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
                                  pitch_gy, yaw_gz, roll_gx, y_left_right, z_up_down, x_forward_backward):
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

    # Data taken from read_hdf5_files (*.hdf5)
    def set_wiasl_mark(self, wiasl_mark):
        self.wiasl_mark_exists = True
        one_found = False
        two_found = False
        for i in range(len(wiasl_mark)):
            if wiasl_mark[i] == '1.0' and not one_found:
                self.wiasl_mark_forward_ended_indexes.append(i)
                one_found = True
                two_found = False
            elif wiasl_mark[i] == '2.0' and not two_found:
                self.wiasl_mark_backward_started_indexes.append(i)
                one_found = False
                two_found = True

    # Data taken from read_hdf5_files (*.hdf5)
    def set_homing_mark(self, homing_mark):
        self.homing_mark_exists = True
        one_found = False
        for i in range(len(homing_mark)):
            if homing_mark[i] == '1.0':
                if not one_found:
                    self.homing_mark_participant_started_alone_indexes.append(i)
                    one_found = True
            else:
                one_found = False

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
