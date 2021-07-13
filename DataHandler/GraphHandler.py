# Plotting all graphs
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import matplotlib.ticker as ticker

sound = {
    0: "both with and without sound",
    1: "with sound only",
    2: "without sound only"
}


class GraphHandler:
    HALF = 17
    SL_LIMIT = -400
    PAD = 13.

    def __init__(self, participants, take_half_trials=False):
        # Participants
        self.participants = participants

        # Distance Errors - means
        # Both with and without sound
        # homing
        self.err_means_diag = []
        self.err_means_hor = []
        self.err_means_ver = []
        # wiasl - forward
        self.err_means_diag_for = []
        self.err_means_hor_for = []
        self.err_means_ver_for = []
        # wiasl - backward
        self.err_means_diag_back = []
        self.err_means_hor_back = []
        self.err_means_ver_back = []

        # With sound only
        # homing
        self.err_means_diag_with_sound = []
        self.err_means_hor_with_sound = []
        self.err_means_ver_with_sound = []
        # wiasl - forward
        self.err_means_diag_for_with_sound = []
        self.err_means_hor_for_with_sound = []
        self.err_means_ver_for_with_sound = []
        # wiasl - backward
        self.err_means_diag_back_with_sound = []
        self.err_means_hor_back_with_sound = []
        self.err_means_ver_back_with_sound = []

        # Without sound only
        # homing
        self.err_means_diag_without_sound = []
        self.err_means_hor_without_sound = []
        self.err_means_ver_without_sound = []
        # wiasl - forward
        self.err_means_diag_for_without_sound = []
        self.err_means_hor_for_without_sound = []
        self.err_means_ver_for_without_sound = []
        # wiasl - backward
        self.err_means_diag_back_without_sound = []
        self.err_means_hor_back_without_sound = []
        self.err_means_ver_back_without_sound = []

        # Diffs
        self.diffs_homing_horizontal = []
        self.diffs_homing_vertical = []
        self.diffs_for_horizontal = []
        self.diffs_for_vertical = []
        self.diffs_back_horizontal = []
        self.diffs_back_vertical = []

        # both with and without sound
        # self.set_mean_errors()

        #self.set_mean_errors_with_and_without_sound()
        self.set_mean_errors_with_and_without_sound_per_trials()
        # self.set_mean_errors_with_and_without_sound_for_half_the_trials(take_half_trials)

        self.set_diffs()

        self.set_all_err_to_cm()

    def set_all_err_to_cm(self):
        # Distance Errors - means
        # Both with and without sound
        # homing
        self.err_means_diag = self.mm_to_cm(self.err_means_diag)
        self.err_means_hor = self.mm_to_cm(self.err_means_hor)
        self.err_means_ver = self.mm_to_cm(self.err_means_ver)
        # wiasl - forward
        self.err_means_diag_for = self.mm_to_cm(self.err_means_diag_for)
        self.err_means_hor_for = self.mm_to_cm(self.err_means_hor_for)
        self.err_means_ver_for = self.mm_to_cm(self.err_means_ver_for)
        # wiasl - backward
        self.err_means_diag_back = self.mm_to_cm(self.err_means_diag_back)
        self.err_means_hor_back = self.mm_to_cm(self.err_means_hor_back)
        self.err_means_ver_back = self.mm_to_cm(self.err_means_ver_back)

        # With sound only
        # homing
        self.err_means_diag_with_sound = self.mm_to_cm(self.err_means_diag_with_sound)
        self.err_means_hor_with_sound = self.mm_to_cm(self.err_means_hor_with_sound)
        self.err_means_ver_with_sound = self.mm_to_cm(self.err_means_ver_with_sound)
        # wiasl - forward
        self.err_means_diag_for_with_sound = self.mm_to_cm(self.err_means_diag_for_with_sound)
        self.err_means_hor_for_with_sound = self.mm_to_cm(self.err_means_hor_for_with_sound)
        self.err_means_ver_for_with_sound = self.mm_to_cm(self.err_means_ver_for_with_sound)
        # wiasl - backward
        self.err_means_diag_back_with_sound = self.mm_to_cm(self.err_means_diag_back_with_sound)
        self.err_means_hor_back_with_sound = self.mm_to_cm(self.err_means_hor_back_with_sound)
        self.err_means_ver_back_with_sound = self.mm_to_cm(self.err_means_ver_back_with_sound)

        # Without sound only
        # homing
        self.err_means_diag_without_sound = self.mm_to_cm(self.err_means_diag_without_sound)
        self.err_means_hor_without_sound = self.mm_to_cm(self.err_means_hor_without_sound)
        self.err_means_ver_without_sound = self.mm_to_cm(self.err_means_ver_without_sound)
        # wiasl - forward
        self.err_means_diag_for_without_sound = self.mm_to_cm(self.err_means_diag_for_without_sound)
        self.err_means_hor_for_without_sound = self.mm_to_cm(self.err_means_hor_for_without_sound)
        self.err_means_ver_for_without_sound = self.mm_to_cm(self.err_means_ver_for_without_sound)
        # wiasl - backward
        self.err_means_diag_back_without_sound = self.mm_to_cm(self.err_means_diag_back_without_sound)
        self.err_means_hor_back_without_sound = self.mm_to_cm(self.err_means_hor_back_without_sound)
        self.err_means_ver_back_without_sound = self.mm_to_cm(self.err_means_ver_back_without_sound)

        # Diffs
        self.diffs_homing_horizontal = self.mm_to_cm(self.diffs_homing_horizontal)
        self.diffs_homing_vertical = self.mm_to_cm(self.diffs_homing_vertical)
        self.diffs_for_horizontal = self.mm_to_cm(self.diffs_for_horizontal)
        self.diffs_for_vertical = self.mm_to_cm(self.diffs_for_vertical)
        self.diffs_back_horizontal = self.mm_to_cm(self.diffs_back_horizontal)
        self.diffs_back_vertical = self.mm_to_cm(self.diffs_back_vertical)

    def mm_to_cm(self, x):
        return [val/10.0 for val in x]

    # Calculates the mean error of each type (diagonal, horizontal, vertical) for each participant in each task type.
    # Example:
    # Let's look at err_means_ver_for.
    # In each cell, it contains the mean of the vertical error in the WiaSL-forward task of a single participant.
    # To get this info, we:
    #   - go to each participant
    #   - take only the vertical errors in the trials that are marked as homing task trials
    #   - calculate the mean of these errors
    #   - add this mean to err_means_ver_for array
    #   so now this array contains this mean of this specific participant in index i.
    def set_mean_errors(self):
        for participant in self.participants:
            # calculate mean error values for homing task
            self.err_means_diag.append(np.mean([participant.error_1_diagonal[i] for i in
                                                range(len(participant.error_1_diagonal[:-2]))
                                                if participant.homing_indexes_flag[i] == 1]))
            self.err_means_hor.append(np.mean([participant.error_2_horizontal[i] for i in
                                               range(len(participant.error_2_horizontal[:-2]))
                                               if participant.homing_indexes_flag[i] == 1]))
            self.err_means_ver.append(np.mean([participant.error_3_vertical[i] for i in
                                               range(len(participant.error_3_vertical[:-2]))
                                               if participant.homing_indexes_flag[i] == 1]))

            # calculate mean error values for wiasl task - forward
            self.err_means_diag_for.append(np.mean([participant.error_1_diagonal[i] for i in
                                                    range(len(participant.error_1_diagonal[:-2]))
                                                    if participant.homing_indexes_flag[i] == 0]))
            self.err_means_hor_for.append(np.mean([participant.error_2_horizontal[i] for i in
                                                   range(len(participant.error_2_horizontal[:-2]))
                                                   if participant.homing_indexes_flag[i] == 0]))
            self.err_means_ver_for.append(np.mean([participant.error_3_vertical[i] for i in
                                                   range(len(participant.error_3_vertical[:-2]))
                                                   if participant.homing_indexes_flag[i] == 0]))

            # calculate mean error values for wiasl task - backward
            self.err_means_diag_back.append(np.mean([participant.error_1_diagonal_backward[i] for i in
                                                     range(len(participant.error_1_diagonal_backward[:-2]))
                                                     if participant.homing_indexes_flag[i] == 0]))
            self.err_means_hor_back.append(np.mean([participant.error_2_horizontal_backward[i] for i in
                                                    range(len(participant.error_2_horizontal_backward[:-2]))
                                                    if participant.homing_indexes_flag[i] == 0]))
            self.err_means_ver_back.append(np.mean([participant.error_3_vertical_backward[i] for i in
                                                    range(len(participant.error_3_vertical_backward[:-2]))
                                                    if participant.homing_indexes_flag[i] == 0]))

    # Calculates the mean error of each type (diagonal, horizontal, vertical) for each participant
    # in each task type and each contidion type (with or without sound).
    # Example:
    # Let's look at err_means_ver_with_sound.
    # In each cell, it contains the mean of the vertical error in the homing task of a single participant
    # while she hears sound.
    # To get this info, we:
    #   - go to each participant
    #   - take only the vertical errors in the trials that are marked as:
    #       homing task trials
    #       and
    #       with-sound trials
    #   - calculate the mean of these errors
    #   - add this mean to err_means_ver_with_sound array
    #   so now this array contains this mean of this specific participant in index i.
    def set_mean_errors_with_and_without_sound(self):
        for participant in self.participants:
            # With sound
            # calculate mean error values for homing task
            self.err_means_diag_with_sound.append(np.mean(
                [participant.error_1_diagonal[i] for i in range(len(participant.error_1_diagonal[:-2]))
                 if participant.homing_indexes_flag[i] == 1 and participant.with_sound_indexes_flag[i] == 1]))
            self.err_means_hor_with_sound.append(np.mean(
                [participant.error_2_horizontal[i] for i in range(len(participant.error_2_horizontal[:-2]))
                 if participant.homing_indexes_flag[i] == 1 and participant.with_sound_indexes_flag[i] == 1]))
            self.err_means_ver_with_sound.append(np.mean(
                [participant.error_3_vertical[i] for i in range(len(participant.error_3_vertical[:-2]))
                 if participant.homing_indexes_flag[i] == 1 and participant.with_sound_indexes_flag[i] == 1]))

            # calculate mean error values for wiasl task - forward
            self.err_means_diag_for_with_sound.append(np.mean(
                [participant.error_1_diagonal[i] for i in range(len(participant.error_1_diagonal[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 1]))
            self.err_means_hor_for_with_sound.append(np.mean(
                [participant.error_2_horizontal[i] for i in range(len(participant.error_2_horizontal[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 1]))
            self.err_means_ver_for_with_sound.append(np.mean(
                [participant.error_3_vertical[i] for i in range(len(participant.error_3_vertical[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 1]))

            # calculate mean error values for wiasl task - backward
            self.err_means_diag_back_with_sound.append(np.mean(
                [participant.error_1_diagonal_backward[i] for i in range(len(participant.error_1_diagonal_backward[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 1]))
            self.err_means_hor_back_with_sound.append(np.mean(
                [participant.error_2_horizontal_backward[i] for i in range(len(participant.error_2_horizontal_backward[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 1]))
            self.err_means_ver_back_with_sound.append(np.mean(
                [participant.error_3_vertical_backward[i] for i in range(len(participant.error_3_vertical_backward[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 1]))

            # Without sound
            # calculate mean error values for homing task
            self.err_means_diag_without_sound.append(np.mean(
                [participant.error_1_diagonal[i] for i in range(len(participant.error_1_diagonal[:-2]))
                 if participant.homing_indexes_flag[i] == 1 and participant.with_sound_indexes_flag[i] == 0]))
            self.err_means_hor_without_sound.append(np.mean(
                [participant.error_2_horizontal[i] for i in range(len(participant.error_2_horizontal[:-2]))
                 if participant.homing_indexes_flag[i] == 1 and participant.with_sound_indexes_flag[i] == 0]))
            self.err_means_ver_without_sound.append(np.mean(
                [participant.error_3_vertical[i] for i in range(len(participant.error_3_vertical[:-2]))
                 if participant.homing_indexes_flag[i] == 1 and participant.with_sound_indexes_flag[i] == 0]))

            # calculate mean error values for wiasl task - forward
            self.err_means_diag_for_without_sound.append(np.mean(
                [participant.error_1_diagonal[i] for i in range(len(participant.error_1_diagonal[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 0]))
            self.err_means_hor_for_without_sound.append(np.mean(
                [participant.error_2_horizontal[i] for i in range(len(participant.error_2_horizontal[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 0]))
            self.err_means_ver_for_without_sound.append(np.mean(
                [participant.error_3_vertical[i] for i in range(len(participant.error_3_vertical[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 0]))

            # calculate mean error values for wiasl task - backward
            self.err_means_diag_back_without_sound.append(np.mean(
                [participant.error_1_diagonal_backward[i] for i in range(len(participant.error_1_diagonal_backward[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 0]))
            self.err_means_hor_back_without_sound.append(np.mean(
                [participant.error_2_horizontal_backward[i] for i in range(len(participant.error_2_horizontal_backward[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 0]))
            self.err_means_ver_back_without_sound.append(np.mean(
                [participant.error_3_vertical_backward[i] for i in range(len(participant.error_3_vertical_backward[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 0]))

    def set_diffs(self):
        # Horizontal error
        # Homing task
        for i in range(len(self.err_means_hor_with_sound)):
            ws_mean = self.err_means_hor_with_sound[i]
            wos_mean = self.err_means_hor_without_sound[i]
            diff = np.abs(wos_mean) - np.abs(ws_mean)
            self.diffs_homing_horizontal.append(diff)
        # WiaSL Forward task
        for i in range(len(self.err_means_hor_for_with_sound)):
            ws_mean = self.err_means_hor_for_with_sound[i]
            wos_mean = self.err_means_hor_for_without_sound[i]
            diff = np.abs(wos_mean) - np.abs(ws_mean)
            self.diffs_for_horizontal.append(diff)
        # WiaSL Backward task
        for i in range(len(self.err_means_hor_back_with_sound)):
            ws_mean = self.err_means_hor_back_with_sound[i]
            wos_mean = self.err_means_hor_back_without_sound[i]
            diff = np.abs(wos_mean) - np.abs(ws_mean)
            self.diffs_back_horizontal.append(diff)

        # Vertical error
        # Homing task
        for i in range(len(self.err_means_ver_with_sound)):
            ws_mean = self.err_means_ver_with_sound[i]
            wos_mean = self.err_means_ver_without_sound[i]
            diff = np.abs(wos_mean) - np.abs(ws_mean)
            self.diffs_homing_vertical.append(diff)
        # WiaSL Forward task
        for i in range(len(self.err_means_ver_for_with_sound)):
            ws_mean = self.err_means_ver_for_with_sound[i]
            wos_mean = self.err_means_ver_for_without_sound[i]
            diff = np.abs(wos_mean) - np.abs(ws_mean)
            self.diffs_for_vertical.append(diff)
        # WiaSL Backward task
        for i in range(len(self.err_means_ver_back_with_sound)):
            ws_mean = self.err_means_ver_back_with_sound[i]
            wos_mean = self.err_means_ver_back_without_sound[i]
            diff = np.abs(wos_mean) - np.abs(ws_mean)
            self.diffs_back_vertical.append(diff)

    # Plot the errors histograms of a given task.
    # That is, how does the participants' distribution look like for a given error type?
    def error_histograms(self, hist_array_0, hist_array_1, hist_array_2, sound_type, task_name, task_type=None):
        fig, axs = plt.subplots(1, 3)
        fig.suptitle("Pooling trials " + sound[sound_type])

        axs[0].hist(hist_array_0)
        axs[1].hist(hist_array_1)
        axs[2].hist(hist_array_2)

        if task_type is None:
            axs[0].set_title(task_name + ' Task - Diagonal Error')
            axs[1].set_title(task_name + ' Task - Horizontal Error')
            axs[2].set_title(task_name + ' Task - Vertical Error')
        else:
            axs[0].set_title(task_name + ' Task - Diagonal Error - ' + task_type)
            axs[1].set_title(task_name + ' Task - Horizontal Error - ' + task_type)
            axs[2].set_title(task_name + ' Task - Vertical Error - ' + task_type)

        for ax in axs.flat:
            ax.set(xlabel='Error Mean (cm)', ylabel='#Participants')
            ax.set_xlim([-270, 270])
            ax.set_ylim([0, 16])
            ylim = ax.get_ylim()
            ax.axvline(x=0, ymin=ylim[0], ymax=ylim[1], color='black', dashes=(5, 3))

        # # Hide x labels and tick labels for top plots and y ticks for right plots.
        # for ax in axs.flat:
        #     ax.label_outer()

        plt.show()

    def twoD_gaussian(self, xx, yy, task_name, task_type, show_SL):
        def multivariate_gaussian(pos, mu, sigma):
            """Return the multivariate Gaussian distribution on array pos."""
            n = mu.shape[0]
            sigma_det = np.linalg.det(sigma)
            sigma_inv = np.linalg.inv(sigma)
            N = np.sqrt((2 * np.pi) ** n * sigma_det)
            # this einsum call calculates (x-mu)T.Sigma-1.(x-mu) in a vectorized
            # way across all the input variables.
            fac = np.einsum('...k,kl,...l->...', pos - mu, sigma_inv, pos - mu)

            return np.exp(-fac / 2) / N

        # mean vector and covariance matrix
        mu = np.array([np.mean(xx), np.mean(yy)])
        sigma = np.cov(np.vstack((xx, yy)))

        x, y = np.meshgrid(xx, yy)

        # pack x and y into a single 3-dimensional array
        pos = np.empty(x.shape + (2,))
        pos[:, :, 0] = x
        pos[:, :, 1] = y

        # the distribution on the variables x, y packed into pos.
        z = multivariate_gaussian(pos, mu, sigma)

        fig, ax = plt.subplots()
        ax.set_aspect('equal')

        # for all trials, per participant
        levels = np.linspace(0.0, 0.00016, 7)
        map = ax.contourf(x, y, z, zdir='z', offset=0, cmap=cm.viridis, levels=levels, vmin=0, vmax=0.00016)
        # for all trials, per trial
        # levels = np.linspace(0.0, 0.000064, 7)
        # map = ax.contourf(x, y, z, zdir='z', offset=0, cmap=cm.viridis, levels=levels, vmin=0, vmax=0.000064)
        # map = ax.contourf(x, y, z, zdir='z', offset=0, cmap=cm.viridis)

        ax.grid(True)

        plt.scatter(xx, yy, color='hotpink', facecolors='none')

        # ticks for all trials, per participant
        ticks = (-200, 201, 50)
        # ticks for half of trials, per participant
        # ticks = (-250, 251, 50)
        # for all trials, per trial
        # ticks = (-450, 451, 100)
        ax.set_xticks(list(range(ticks[0], ticks[1], ticks[2])))
        if show_SL:
            if task_type == 'Forward':
                ax.set_yticks(list(range(self.SL_LIMIT, ticks[1], ticks[2])))
            elif task_type == 'Backward':
                ax.set_yticks(list(range(ticks[0], -1*self.SL_LIMIT+1, ticks[2])))
        else:
            ax.set_yticks(list(range(ticks[0], ticks[1], ticks[2])))

        for tick in ax.get_xaxis().get_major_ticks():
            tick.set_pad(self.PAD)
            tick.label1 = tick._get_text1()
        for tick in ax.get_yaxis().get_major_ticks():
            tick.set_pad(self.PAD)
            tick.label1 = tick._get_text1()

        ax.set_xlabel(r'$Horizontal(cm)$')
        ax.set_ylabel(r'$Vertical(cm)$')

        # title
        ax.set_title(task_name + " Task " + task_type + " - 2D Gaussian Distribution")

        # v = np.linspace(.0, 0.0001, 8, endpoint=True)
        # fig.colorbar(map, ticks=v)

        # def fmt(x, pos):
        #     a, b = '{:.2e}'.format(x).split('e')
        #     b = int(b)
        #     return r'${} \times 10^{{{}}}$'.format(a, b)
        # fig.colorbar(map, format=ticker.FuncFormatter(fmt))

        fmt = ticker.ScalarFormatter(useMathText=True)
        fmt.set_powerlimits((0, 0))
        cbar = fig.colorbar(map, format=fmt)
        # cbar.ax.set_title('PDF')
        # cbar.set_label(label='PDF', weight='bold')

        cbar.ax.yaxis.offsetText.set_visible(False)
        offset = cbar.ax.yaxis.get_major_formatter().get_offset()
        cbar.ax.yaxis.set_label_text("Probability Density Function (PDF)" + " " + offset)

        plt.tight_layout()
        plt.axhline(0, color='k')
        plt.axvline(0, color='k')

        plt.show()

    # Plot the diffs of a given error type in a given task as a histogram.
    # That is, how does the participants' diff distribution look like for a given error type of a given task?
    def error_diff_histograms(self, diffs, error_type, task_name, task_type,per_participant):
        plt.hist(diffs)
        plt.title('Improvement with sound distribution\n\n' + task_name + ' ' + task_type + ' Task - ' + error_type + ' Error')
        plt.xlabel('Error Means Difference Between Trials Without and With Sound (cm)')
        if per_participant:
            plt.ylabel('#Participants')
            # limits for all trials, per participant
            plt.xlim([-140, 140])
            plt.ylim([0, 14])
            # limits for half of trials, per participant
            # plt.xlim([-350, 350])
            # plt.ylim([0, 18])
        else:
            plt.ylabel('#Trials')
            # limits for all trials, per trial
            plt.xlim([-400, 400])
            plt.ylim([0, 140])
        plt.show()

    # The same calculations as set_mean_errors_with_and_without_sound method,
    # only this function allows either analyzing all trials (take_half=False)
    # or only the second half of them (take_half=True).
    def set_mean_errors_with_and_without_sound_for_half_the_trials(self, take_half=False):
        if take_half:
            start = self.HALF
        else:
            start = 0

        for participant in self.participants:
            # With sound
            # calculate mean error values for homing task
            self.err_means_diag_with_sound.append(np.mean(
                [participant.error_1_diagonal[i] for i in range(start, len(participant.error_1_diagonal)-2)
                 if participant.homing_indexes_flag[i] == 1 and participant.with_sound_indexes_flag[i] == 1]))
            self.err_means_hor_with_sound.append(np.mean(
                [participant.error_2_horizontal[i] for i in range(start, len(participant.error_2_horizontal)-2)
                 if participant.homing_indexes_flag[i] == 1 and participant.with_sound_indexes_flag[i] == 1]))
            self.err_means_ver_with_sound.append(np.mean(
                [participant.error_3_vertical[i] for i in range(start, len(participant.error_3_vertical)-2)
                 if participant.homing_indexes_flag[i] == 1 and participant.with_sound_indexes_flag[i] == 1]))

            # calculate mean error values for wiasl task - forward
            self.err_means_diag_for_with_sound.append(np.mean(
                [participant.error_1_diagonal[i] for i in range(start, len(participant.error_1_diagonal)-2)
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 1]))
            self.err_means_hor_for_with_sound.append(np.mean(
                [participant.error_2_horizontal[i] for i in range(start, len(participant.error_2_horizontal) - 2)
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 1]))
            self.err_means_ver_for_with_sound.append(np.mean(
                [participant.error_3_vertical[i] for i in range(start, len(participant.error_3_vertical)-2)
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 1]))

            # calculate mean error values for wiasl task - backward
            self.err_means_diag_back_with_sound.append(np.mean(
                [participant.error_1_diagonal_backward[i] for i in
                 range(start, len(participant.error_1_diagonal_backward)-2)
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 1]))
            self.err_means_hor_back_with_sound.append(np.mean(
                [participant.error_2_horizontal_backward[i] for i in
                 range(start, len(participant.error_2_horizontal_backward)-2)
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 1]))
            self.err_means_ver_back_with_sound.append(np.mean(
                [participant.error_3_vertical_backward[i] for i in
                 range(start, len(participant.error_3_vertical_backward)-2)
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 1]))

            # Without sound
            # calculate mean error values for homing task
            self.err_means_diag_without_sound.append(np.mean(
                [participant.error_1_diagonal[i] for i in range(start, len(participant.error_1_diagonal)-2)
                 if participant.homing_indexes_flag[i] == 1 and participant.with_sound_indexes_flag[i] == 0]))
            self.err_means_hor_without_sound.append(np.mean(
                [participant.error_2_horizontal[i] for i in range(start, len(participant.error_2_horizontal)-2)
                 if participant.homing_indexes_flag[i] == 1 and participant.with_sound_indexes_flag[i] == 0]))
            self.err_means_ver_without_sound.append(np.mean(
                [participant.error_3_vertical[i] for i in range(start, len(participant.error_3_vertical)-2)
                 if participant.homing_indexes_flag[i] == 1 and participant.with_sound_indexes_flag[i] == 0]))

            # calculate mean error values for wiasl task - forward
            self.err_means_diag_for_without_sound.append(np.mean(
                [participant.error_1_diagonal[i] for i in range(start, len(participant.error_1_diagonal)-2)
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 0]))
            self.err_means_hor_for_without_sound.append(np.mean(
                [participant.error_2_horizontal[i] for i in range(start, len(participant.error_2_horizontal)-2)
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 0]))
            self.err_means_ver_for_without_sound.append(np.mean(
                [participant.error_3_vertical[i] for i in range(start, len(participant.error_3_vertical)-2)
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 0]))

            # calculate mean error values for wiasl task - backward
            self.err_means_diag_back_without_sound.append(np.mean(
                [participant.error_1_diagonal_backward[i] for i in
                 range(start, len(participant.error_1_diagonal_backward)-2)
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 0]))
            self.err_means_hor_back_without_sound.append(np.mean(
                [participant.error_2_horizontal_backward[i] for i in
                 range(start, len(participant.error_2_horizontal_backward)-2)
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 0]))
            self.err_means_ver_back_without_sound.append(np.mean(
                [participant.error_3_vertical_backward[i] for i in
                 range(start, len(participant.error_3_vertical_backward)-2)
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 0]))

    # Same as set_mean_errors_with_and_without_sound, only per trials
    # (that is, without averaging per participant).
    def set_mean_errors_with_and_without_sound_per_trials(self):
        for participant in self.participants:
            # With sound
            # calculate mean error values for homing task
            self.err_means_diag_with_sound.extend(
                [participant.error_1_diagonal[i] for i in range(len(participant.error_1_diagonal[:-2]))
                 if participant.homing_indexes_flag[i] == 1 and participant.with_sound_indexes_flag[i] == 1])
            self.err_means_hor_with_sound.extend(
                [participant.error_2_horizontal[i] for i in range(len(participant.error_2_horizontal[:-2]))
                 if participant.homing_indexes_flag[i] == 1 and participant.with_sound_indexes_flag[i] == 1])
            self.err_means_ver_with_sound.extend(
                [participant.error_3_vertical[i] for i in range(len(participant.error_3_vertical[:-2]))
                 if participant.homing_indexes_flag[i] == 1 and participant.with_sound_indexes_flag[i] == 1])

            # calculate mean error values for wiasl task - forward
            self.err_means_diag_for_with_sound.extend(
                [participant.error_1_diagonal[i] for i in range(len(participant.error_1_diagonal[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 1])
            self.err_means_hor_for_with_sound.extend(
                [participant.error_2_horizontal[i] for i in range(len(participant.error_2_horizontal[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 1])
            self.err_means_ver_for_with_sound.extend(
                [participant.error_3_vertical[i] for i in range(len(participant.error_3_vertical[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 1])

            # calculate mean error values for wiasl task - backward
            self.err_means_diag_back_with_sound.extend(
                [participant.error_1_diagonal_backward[i] for i in
                 range(len(participant.error_1_diagonal_backward[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 1])
            self.err_means_hor_back_with_sound.extend(
                [participant.error_2_horizontal_backward[i] for i in
                 range(len(participant.error_2_horizontal_backward[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 1])
            self.err_means_ver_back_with_sound.extend(
                [participant.error_3_vertical_backward[i] for i in
                 range(len(participant.error_3_vertical_backward[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 1])

            # Without sound
            # calculate mean error values for homing task
            self.err_means_diag_without_sound.extend(
                [participant.error_1_diagonal[i] for i in range(len(participant.error_1_diagonal[:-2]))
                 if participant.homing_indexes_flag[i] == 1 and participant.with_sound_indexes_flag[i] == 0])
            self.err_means_hor_without_sound.extend(
                [participant.error_2_horizontal[i] for i in range(len(participant.error_2_horizontal[:-2]))
                 if participant.homing_indexes_flag[i] == 1 and participant.with_sound_indexes_flag[i] == 0])
            self.err_means_ver_without_sound.extend(
                [participant.error_3_vertical[i] for i in range(len(participant.error_3_vertical[:-2]))
                 if participant.homing_indexes_flag[i] == 1 and participant.with_sound_indexes_flag[i] == 0])

            # calculate mean error values for wiasl task - forward
            self.err_means_diag_for_without_sound.extend(
                [participant.error_1_diagonal[i] for i in range(len(participant.error_1_diagonal[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 0])
            self.err_means_hor_for_without_sound.extend(
                [participant.error_2_horizontal[i] for i in range(len(participant.error_2_horizontal[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 0])
            self.err_means_ver_for_without_sound.extend(
                [participant.error_3_vertical[i] for i in range(len(participant.error_3_vertical[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 0])

            # calculate mean error values for wiasl task - backward
            self.err_means_diag_back_without_sound.extend(
                [participant.error_1_diagonal_backward[i] for i in
                 range(len(participant.error_1_diagonal_backward[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 0])
            self.err_means_hor_back_without_sound.extend(
                [participant.error_2_horizontal_backward[i] for i in
                 range(len(participant.error_2_horizontal_backward[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 0])
            self.err_means_ver_back_without_sound.extend(
                [participant.error_3_vertical_backward[i] for i in
                 range(len(participant.error_3_vertical_backward[:-2]))
                 if participant.homing_indexes_flag[i] == 0 and participant.with_sound_indexes_flag[i] == 0])
