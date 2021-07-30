import numpy as np
import scipy.stats as stats

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
    # homing task, horizontal error
    result = Statistics.paired_ttest(gh.err_means_hor_with_sound, gh.err_means_hor_without_sound)

    # wiasl forward task, horizontal error
    result = Statistics.paired_ttest(gh.err_means_hor_for_with_sound, gh.err_means_hor_for_without_sound)

    # wiasl backward task, horizontal error
    result = Statistics.paired_ttest(gh.err_means_hor_back_with_sound, gh.err_means_hor_back_without_sound)

    # homing task, vertical error
    result = Statistics.paired_ttest(gh.err_means_ver_with_sound, gh.err_means_ver_without_sound)

    # wiasl forward task, vertical error
    result = Statistics.paired_ttest(gh.err_means_ver_for_with_sound, gh.err_means_ver_for_without_sound)

    # wiasl backward task, vertical error
    result = Statistics.paired_ttest(gh.err_means_ver_back_with_sound, gh.err_means_ver_back_without_sound)


def bootstrapping_and_ci(gh):
    # homing task, horizontal error
    hom_hor_ws_sd = np.std(gh.err_means_hor_with_sound)  # for comparison with the ws bootstrap calculation
    hom_hor_wos_sd = np.std(gh.err_means_hor_without_sound)  # for comparison with the wos bootstrap calculation
    hom_hor_ws_mean_sd, hom_hor_ws_population = Statistics.bootstrap_sd(gh.err_means_hor_with_sound)
    hom_hor_wos_mean_sd, hom_hor_wos_population = Statistics.bootstrap_sd(gh.err_means_hor_without_sound)
    hom_hor_ws_ci = stats.t.interval(0.95, len(hom_hor_ws_population) - 1,
                                     loc=np.mean(hom_hor_ws_population),
                                     scale=stats.sem(hom_hor_ws_population))
    hom_hor_wos_ci = stats.t.interval(0.95, len(hom_hor_wos_population) - 1,
                                      loc=np.mean(hom_hor_wos_population),
                                      scale=stats.sem(hom_hor_wos_population))

    # wiasl forward task, horizontal error
    for_hor_ws_sd = np.std(gh.err_means_hor_for_with_sound)  # for comparison with the ws bootstrap calculation
    for_hor_wos_sd = np.std(gh.err_means_hor_for_without_sound)  # for comparison with the wos bootstrap calculation
    for_hor_ws_mean_sd, for_hor_ws_population = Statistics.bootstrap_sd(gh.err_means_hor_for_with_sound)
    for_hor_wos_mean_sd, for_hor_wos_population = Statistics.bootstrap_sd(gh.err_means_hor_for_without_sound)
    for_hor_ws_ci = stats.t.interval(0.95, len(for_hor_ws_population) - 1,
                                     loc=np.mean(for_hor_ws_population),
                                     scale=stats.sem(for_hor_ws_population))
    for_hor_wos_ci = stats.t.interval(0.95, len(for_hor_wos_population) - 1,
                                      loc=np.mean(for_hor_wos_population),
                                      scale=stats.sem(for_hor_wos_population))

    # wiasl backward task, horizontal error
    back_hor_ws_sd = np.std(gh.err_means_hor_back_with_sound)  # for comparison with the ws bootstrap calculation
    back_hor_wos_sd = np.std(gh.err_means_hor_back_without_sound)  # for comparison with the wos bootstrap calculation
    back_hor_ws_mean_sd, back_hor_ws_population = Statistics.bootstrap_sd(gh.err_means_hor_back_with_sound)
    back_hor_wos_mean_sd, back_hor_wos_population = Statistics.bootstrap_sd(gh.err_means_hor_back_without_sound)
    back_hor_ws_ci = stats.t.interval(0.95, len(back_hor_ws_population) - 1,
                                      loc=np.mean(back_hor_ws_population),
                                      scale=stats.sem(back_hor_ws_population))
    back_hor_wos_ci = stats.t.interval(0.95, len(back_hor_wos_population) - 1,
                                       loc=np.mean(back_hor_wos_population),
                                       scale=stats.sem(back_hor_wos_population))

    # homing task, vertical error
    hom_ver_ws_sd = np.std(gh.err_means_ver_with_sound)  # for comparison with the ws bootstrap calculation
    hom_ver_wos_sd = np.std(gh.err_means_ver_without_sound)  # for comparison with the wos bootstrap calculation
    hom_ver_ws_mean_sd, hom_ver_ws_population = Statistics.bootstrap_sd(gh.err_means_ver_with_sound)
    hom_ver_wos_mean_sd, hom_ver_wos_population = Statistics.bootstrap_sd(gh.err_means_ver_without_sound)
    hom_ver_ws_ci = stats.t.interval(0.95, len(hom_ver_ws_population) - 1,
                                     loc=np.mean(hom_ver_ws_population),
                                     scale=stats.sem(hom_ver_ws_population))
    hom_ver_wos_ci = stats.t.interval(0.95, len(hom_ver_wos_population) - 1,
                                      loc=np.mean(hom_ver_wos_population),
                                      scale=stats.sem(hom_ver_wos_population))

    # wiasl forward task, vertical error
    for_ver_ws_sd = np.std(gh.err_means_ver_for_with_sound)  # for comparison with the ws bootstrap calculation
    for_ver_wos_sd = np.std(gh.err_means_ver_for_without_sound)  # for comparison with the wos bootstrap calculation
    for_ver_ws_mean_sd, for_ver_ws_population = Statistics.bootstrap_sd(gh.err_means_ver_for_with_sound)
    for_ver_wos_mean_sd, for_ver_wos_population = Statistics.bootstrap_sd(gh.err_means_ver_for_without_sound)
    for_ver_ws_ci = stats.t.interval(0.95, len(for_ver_ws_population) - 1,
                                     loc=np.mean(for_ver_ws_population),
                                     scale=stats.sem(for_ver_ws_population))
    for_ver_wos_ci = stats.t.interval(0.95, len(for_ver_wos_population) - 1,
                                      loc=np.mean(for_ver_wos_population),
                                      scale=stats.sem(for_ver_wos_population))

    # wiasl backward task, vertical error
    back_ver_ws_sd = np.std(gh.err_means_ver_back_with_sound)  # for comparison with the ws bootstrap calculation
    back_ver_wos_sd = np.std(gh.err_means_ver_back_without_sound)  # for comparison with the wos bootstrap calculation
    back_ver_ws_mean_sd, back_ver_ws_population = Statistics.bootstrap_sd(gh.err_means_ver_back_with_sound)
    back_ver_wos_mean_sd, back_ver_wos_population = Statistics.bootstrap_sd(gh.err_means_ver_back_without_sound)
    back_ver_ws_ci = stats.t.interval(0.95, len(back_ver_ws_population) - 1,
                                      loc=np.mean(back_ver_ws_population),
                                      scale=stats.sem(back_ver_ws_population))
    back_ver_wos_ci = stats.t.interval(0.95, len(back_ver_wos_population) - 1,
                                       loc=np.mean(back_ver_wos_population),
                                       scale=stats.sem(back_ver_wos_population))


def main():
    loader = Loader.Loader()  # load, read and clean all data
    gh = GraphHandler.GraphHandler(loader.participants, take_half_trials=False)  # create a graph handler to plot graphs

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
    # paired_ttest_statistics(gh)
    # calculate bootstrap on the SD with sound and without sound separately
    bootstrapping_and_ci(gh)


if __name__ == "__main__":
    main()
