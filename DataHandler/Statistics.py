import numpy as np
from scipy import stats


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
