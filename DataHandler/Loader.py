import os

import h5py
import pandas as pd
from DataHandler.Participant import Participant
import DataHandler.Cleaner as Cleaner


class Loader:
    def __init__(self):
        self.participants = []  # all participants
        self.files_dirs_paths = self.set_files_paths()  # paths to all the participants directories of data
        self.read_files()  # load all files and read the data from them

    # Create a list of paths to all the participants directories of data
    def set_files_paths(self):
        dirs_paths = []
        # parent_dir_path = "C:\\Users\\user\\PycharmProjects\\SSD\\Output"
        parent_dir_path = os.path.join(os.path.split(os.getcwd())[0], "Output")
        parent_listdir = os.listdir(parent_dir_path)

        for dir in parent_listdir:
            dir_path = os.path.join(parent_dir_path, dir)
            dirs_paths.append(dir_path)

        return dirs_paths

    # Read the files of each participant
    def read_files(self):
        for participant_dir in self.files_dirs_paths:
            # save participant meta data (details)
            without_extra_slash = os.path.normpath(participant_dir)
            participant_dir_name = os.path.basename(without_extra_slash)
            participant_num = int(participant_dir_name[:2])

            # For loading only one participant's data
            # if participant_num != 19:
            #     continue

            participant_id = participant_dir_name[-9:]
            participant = Participant(participant_num, participant_id)

            # Read trials_data.csv
            self.read_trials_data_file(participant_dir, participant)
            self.read_trial_type_short_list(participant_dir, participant)
            # Read *.hdf5 files
            # self.read_hdf5_files(participant_dir, participant)
            # Read Distance Errors.csv
            self.read_distance_errors_file(participant_dir, participant)

            self.participants.append(participant)

    # Read the trials_data.csv file of a single participant
    def read_trials_data_file(self, participant_dir, participant):
        path = os.path.join(participant_dir, 'trials_data.csv')
        td_f = pd.read_csv(path)
        mat_td_f = Cleaner.clean_trials_data(participant.num, td_f.to_numpy())
        participant.set_data_from_trials_data(mat_td_f[:, 0], mat_td_f[:, 1], mat_td_f[:, 2], mat_td_f[:, 3],
                                              mat_td_f[:, 4], mat_td_f[:, 5], mat_td_f[:, 6], mat_td_f[:, 7],
                                              mat_td_f[:, 8], mat_td_f[:, 9], mat_td_f[:, 10], mat_td_f[:, 11],
                                              mat_td_f[:, 12], mat_td_f[:, 13], mat_td_f[:, 14], mat_td_f[:, 15])

    # Read the trial_type_short_list.csv file of a single participant
    def read_trial_type_short_list(self, participant_dir, participant):
        path = os.path.join(participant_dir, 'trial_type_short_list.csv')
        td_f = pd.read_csv(path)
        trial_type_list = list(td_f['trial_type'])
        participant.set_trial_type_short_list(trial_type_list)

    # Read all files one by one in order to take the needed information from each of them.
    def read_hdf5_files(self, participant_dir, participant):
        path_listdir = os.listdir(participant_dir)
        for name in path_listdir:
            if name.endswith(".hdf5"):
                full_path = os.path.join(participant_dir, name)
                f = h5py.File(full_path, 'r')
                if "WiaSLMark" in f:
                    participant.set_wiasl_mark(f['WiaSLMark'])
                if "HomingMark" in f:
                    participant.set_homing_mark(f['HomingMark'])

    def read_distance_errors_file(self, participant_dir, participant):
        path = os.path.join(participant_dir, 'Distance Errors.csv')
        de_f = pd.read_csv(path)
        mat_de_f = Cleaner.clean_errors_data(participant, de_f.to_numpy()[:, 1:7])
        # participant.set_distance_errors(list(de_f['Error 1 - Diagonal Distance']),
        #                                 list(de_f['Error 2 - Horizontal Distance']),
        #                                 list(de_f['Error 3 - Vertical Distance']),
        #                                 list(de_f['Backwards Error 1']),
        #                                 list(de_f['Backwards Error 2']),
        #                                 list(de_f['Backwards Error 3']))
        participant.set_distance_errors(mat_de_f[:, 0], mat_de_f[:, 1], mat_de_f[:, 2], mat_de_f[:, 3],
                                        mat_de_f[:, 4], mat_de_f[:, 5])
