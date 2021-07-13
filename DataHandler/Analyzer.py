import numpy as np

import DataHandler.Loader as Loader
import DataHandler.GraphHandler as GraphHandler
import DataHandler.Statistics as Statistics


def plot_histograms(gh):
    # Both with and without sound
    # plot homing task histogram for each error type
    # gh.error_histograms(gh.err_means_diag, gh.err_means_hor, gh.err_means_ver, 0, 'Homing')
    # plot wiasl-forward task histogram for each error type
    # gh.error_histograms(gh.err_means_diag_for, gh.err_means_hor_for, gh.err_means_ver_for, 0, 'WiaSL', 'Forward')
    # plot wiasl-backward task histogram for each error type
    # gh.error_histograms(gh.err_means_diag_back, gh.err_means_hor_back, gh.err_means_ver_back, 0, 'WiaSL', 'Backward')

    # With sound only
    # plot homing task histogram for each error type
    gh.error_histograms(gh.err_means_diag_with_sound, gh.err_means_hor_with_sound, gh.err_means_ver_with_sound, 1,
                        'Homing')
    # plot wiasl-forward task histogram for each error type
    gh.error_histograms(gh.err_means_diag_for_with_sound, gh.err_means_hor_for_with_sound,
                        gh.err_means_ver_for_with_sound, 1, 'WiaSL', 'Forward')
    # plot wiasl-backward task histogram for each error type
    gh.error_histograms(gh.err_means_diag_back_with_sound, gh.err_means_hor_back_with_sound,
                        gh.err_means_ver_back_with_sound, 1, 'WiaSL', 'Backward')

    # Without sound only
    # plot homing task histogram for each error type
    gh.error_histograms(gh.err_means_diag_without_sound, gh.err_means_hor_without_sound, gh.err_means_ver_without_sound,
                        0, 'Homing')
    # plot wiasl-forward task histogram for each error type
    gh.error_histograms(gh.err_means_diag_for_without_sound, gh.err_means_hor_for_without_sound,
                        gh.err_means_ver_for_without_sound, 0, 'WiaSL', 'Forward')
    # plot wiasl-backward task histogram for each error type
    gh.error_histograms(gh.err_means_diag_back_without_sound, gh.err_means_hor_back_without_sound,
                        gh.err_means_ver_back_without_sound, 0, 'WiaSL', 'Backward')


def plot_2d_gaussian(gh):
    # Both with and without sound
    # homing errors
    # gh.twoD_gaussian(gh.err_means_hor, gh.err_means_ver, 'Homing', '', show_SL=False)
    # wiasl forward errors
    # gh.twoD_gaussian(gh.err_means_hor_for, gh.err_means_ver_for, 'WiaSL', 'Forward', show_SL=True)
    # wiasl backward errors
    # gh.twoD_gaussian(gh.err_means_hor_back, gh.err_means_ver_back, 'WiaSL', 'Backward', show_SL=True)

    # With sound only
    # homing errors
    gh.twoD_gaussian(gh.err_means_hor_with_sound, gh.err_means_ver_with_sound, 'Homing', '', show_SL=False)
    # wiasl forward errors
    gh.twoD_gaussian(gh.err_means_hor_for_with_sound, gh.err_means_ver_for_with_sound, 'WiaSL', 'Forward', show_SL=True)
    # wiasl backward errors
    gh.twoD_gaussian(gh.err_means_hor_back_with_sound, gh.err_means_ver_back_with_sound, 'WiaSL', 'Backward',
                     show_SL=True)

    # Without sound only
    # homing errors
    gh.twoD_gaussian(gh.err_means_hor_without_sound, gh.err_means_ver_without_sound, 'Homing', '', show_SL=False)
    # wiasl forward errors
    gh.twoD_gaussian(gh.err_means_hor_for_without_sound, gh.err_means_ver_for_without_sound, 'WiaSL', 'Forward',
                     show_SL=True)
    # wiasl backward errors
    gh.twoD_gaussian(gh.err_means_hor_back_without_sound, gh.err_means_ver_back_without_sound, 'WiaSL', 'Backward',
                     show_SL=True)


def plot_diff_histograms(gh, per_participant=True):
    # diff for homing task, horizontal error
    gh.error_diff_histograms(gh.diffs_homing_horizontal, 'Horizontal', 'Homing', '', per_participant)

    # diff for wiasl forward task, horizontal error
    gh.error_diff_histograms(gh.diffs_homing_vertical, 'Horizontal', 'WiaSL', 'Forward', per_participant)

    # diff for wiasl backward task, horizontal error
    gh.error_diff_histograms(gh.diffs_for_horizontal, 'Horizontal', 'WiaSL', 'Backward', per_participant)

    # diff for homing task, vertical error
    gh.error_diff_histograms(gh.diffs_for_vertical, 'Vertical', 'Homing', '', per_participant)

    # diff for wiasl forward task, vertical error
    gh.error_diff_histograms(gh.diffs_back_horizontal, 'Vertical', 'WiaSL', 'Forward', per_participant)

    # diff for wiasl backward task, vertical error
    gh.error_diff_histograms(gh.diffs_back_vertical, 'Vertical', 'WiaSL', 'Backward', per_participant)


def one_sample_ttest_statistics(gh):
    # one_sample_ttest on the diffs.
    mean = np.mean(gh.diffs_homing_horizontal)
    result = Statistics.one_sample_ttest(gh.diffs_homing_horizontal)

    mean = np.mean(gh.diffs_homing_vertical)
    result = Statistics.one_sample_ttest(gh.diffs_homing_vertical)

    mean = np.mean(gh.diffs_for_horizontal)
    result = Statistics.one_sample_ttest(gh.diffs_for_horizontal)

    mean = np.mean(gh.diffs_for_vertical)
    result = Statistics.one_sample_ttest(gh.diffs_for_vertical)

    mean = np.mean(gh.diffs_back_horizontal)
    result = Statistics.one_sample_ttest(gh.diffs_back_horizontal)

    mean = np.mean(gh.diffs_back_vertical)
    result = Statistics.one_sample_ttest(gh.diffs_back_vertical)

    bbb = 5


def paired_ttest_statistics(gh):
    # paired_ttest on the diffs.
    result = Statistics.paired_ttest(gh.err_means_hor_with_sound, gh.err_means_hor_without_sound)

    result = Statistics.paired_ttest(gh.err_means_hor_for_with_sound, gh.err_means_hor_for_without_sound)

    result = Statistics.paired_ttest(gh.err_means_hor_back_with_sound, gh.err_means_hor_back_without_sound)

    result = Statistics.paired_ttest(gh.err_means_ver_with_sound, gh.err_means_ver_without_sound)

    result = Statistics.paired_ttest(gh.err_means_ver_for_with_sound, gh.err_means_ver_for_without_sound)

    result = Statistics.paired_ttest(gh.err_means_ver_back_with_sound, gh.err_means_ver_back_without_sound)

    bbb = 5


def main():
    loader = Loader.Loader()  # load, read and clean all data
    gh = GraphHandler.GraphHandler(loader.participants, take_half_trials=True)  # create a graph handler to plot graphs

    # Plot each error type histograms
    # plot_histograms(gh)

    # Plot 2D-Gaussian Distribution
    # plot_2d_gaussian(gh)

    # Plot diff histograms
    # plot_diff_histograms(gh, per_participant=True)

    # Statistics
    # for per participants only
    # one_sample_ttest_statistics(gh)
    # for per trials
    paired_ttest_statistics(gh)



if __name__ == "__main__":
    main()
