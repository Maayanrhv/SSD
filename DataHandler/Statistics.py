import numpy as np
from scipy import stats
import random


def one_sample_ttest(diff_vec):
    return stats.ttest_1samp(diff_vec, 0.0)


def paired_ttest(diff_vec1, diff_vec2):
    diff_len = len(diff_vec1) - len(diff_vec2)
    if diff_len != 0:
        if diff_len > 0:
            diff_vec1 = diff_vec1[:len(diff_vec1) - diff_len]
        else:
            diff_len = np.abs(diff_len)
            diff_vec2 = diff_vec2[:len(diff_vec2) - diff_len]
    return stats.ttest_rel(diff_vec1, diff_vec2)


def bootstrap_sd(means_vec):
    sds = []
    # repeat 1000 times
    for i in range(1000):
        # take len(means_vec) random values from means_vec (with repetitions)
        resample_vec = random.choices(means_vec, k=len(means_vec))
        # calculate their SD
        curr_sd = np.std(resample_vec)
        sds.append(curr_sd)
    # calculate the mean of all 1000 SD's - the resulted averaged SD should be similar to the real SD
    sds_mean = np.mean(sds)
    return sds_mean, sds
