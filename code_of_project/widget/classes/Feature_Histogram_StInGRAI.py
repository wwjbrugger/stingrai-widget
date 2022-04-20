import logging

import numpy as np
from code_of_project.exceptions import NoValuesInIntervalError
from code_of_project.widget.helper_for_widget import check_if_data_corrupted, get_files_between_start_and_stop_point
from code_of_project.widget.classes.TransitionToUseController import TransitionToUseController
from code_of_project.helper_methods import check_if_list_contain_values


class Feature_Histogram_StInGRAI:
    def __init__(self, ig_dics, arguments, structure_widget):
        self.transition_list = arguments.transitions_to_calculate.copy()
        self.transition_list_static = arguments.transitions_to_calculate.copy()
        self.start_point = structure_widget['slider_baseline']['args']['valinit']
        self.stop_point = structure_widget['slider_data_to_explain']['args']['valinit']
        self.feature_to_plot = structure_widget['feature_button']['initial']
        self.plot_args = structure_widget['hist']['args']
        self.fraction_change_transition = structure_widget['slider_when_to_change_transition']['args']['valinit']
        self.show_mean_in_histogram = structure_widget['hist']['show_mean_in_histogram']
        self.ig_dics = ig_dics
        self.intervals_in_explanation = 0


        self.arguments = arguments
        self.color = {
            'signal->signal': 'b',
            'background->signal': 'tab:orange',
            'signal->background': 'g',
            'background->background': 'tab:red'
        }
        self.label = {
            'signal->signal': 'pos -> pos',
            'background->signal': 'neg -> pos',
            'signal->background': ' pos -> neg',
            'background->background': 'neg -> neg'
        }

    def get_all_paths_of_one_feature(self):
        self.all_explanation = {}
        for transition in self.transition_list:
            try:
                all_ig_of_feature, all_ig_of_feature_weights = self.get_all_paths_of_one_feature_in_transition(
                    self.feature_to_plot, transition)
                self.all_explanation[transition] = {}
                self.all_explanation[transition]['data'] = all_ig_of_feature
                self.all_explanation[transition]['weights'] = all_ig_of_feature_weights
            except NoValuesInIntervalError:
                logging.warning(f'Transition: {transition} is skipped for histogram')

    def get_all_paths_of_one_feature_in_transition(self, feature_to_plot, transition):
        all_ig_of_feature = [[]]
        all_ig_of_feature_weights = [[]]
        folder_in_interval = get_files_between_start_and_stop_point(list_with_folder=self.ig_dics.keys(),
                                                                    start_point=self.start_point,
                                                                    stop_point=self.stop_point)
        self.intervals_in_explanation = len(folder_in_interval)
        TransitionToUseController_obj = TransitionToUseController(num_of_transition=len(folder_in_interval),
                                                                  fraction_change_transition=self.fraction_change_transition)
        for folder_name in folder_in_interval:
            transition_to_use = TransitionToUseController_obj.choose_transition_to_use(transition)
            dic = self.ig_dics[folder_name]
            check_if_data_corrupted(array=dic[transition_to_use], foldername=folder_name,
                                    transition=transition, source='histogram StInGRAI')
            temp = dic[transition_to_use].loc[:, feature_to_plot]
            all_ig_of_feature.append(temp)
            all_ig_of_feature_weights.append(calculate_weights_for_histogram(temp))
        return np.concatenate(all_ig_of_feature), np.concatenate(all_ig_of_feature_weights)

    def plot_histograms(self, ax_list):
        for i, ax in enumerate(ax_list):
            ax.clear()
            if i > 0:
                w = ax.get_xaxis()
                w.set_visible(False)
        x_limits = []
        y_limits = []
        means={}

        for i, transition in enumerate(self.transition_list_static):
            if transition in list(self.all_explanation.keys()):
                self.add_histogram_to_ax(ax_list, i, transition, x_limits, y_limits, means)

        if len(x_limits) == 0:
            return
        new_x_limits, new_y_limits = self.get_extrem_values_from_ax(x_limits, y_limits)
        new_x_limits = self.make_xaxis_symmetric(new_x_limits)

        for i, ax in enumerate(ax_list):
            ax.set_xlim(new_x_limits)
            ax.set_ylim(new_y_limits)
            ax.vlines(x=0, ymin=0, ymax=new_y_limits[1], colors='k', linestyles='dashed')
            if i in means.keys() and self.show_mean_in_histogram:
                ax.vlines(x=means[i], ymin=0, ymax=new_y_limits[1], colors='k', linestyles='solid')

    def add_histogram_to_ax(self, ax_list, i, transition, x_limits, y_limits, means):
        feature_igs = self.all_explanation[transition]['data']
        weights = self.all_explanation[transition]['weights']
        mean = np.sum(feature_igs * weights)

        means[i] = mean
        ax = ax_list[i]
        try:
            check_if_list_contain_values(feature_igs)
            ax.hist(x=feature_igs,
                    label=self.label[transition],
                    color=self.color[transition],
                    weights=weights,
                    **self.plot_args)

            ax.legend()
            ax.set_ylabel('percent' if self.plot_args['density'] else 'count')
            ax.set_xlabel(f"{self.feature_to_plot} \n Data to Explain IG \n distribution")
            x_limits.append(ax.get_xlim())
            y_limits.append(ax.get_ylim())
        except IndexError:
            logging.warning(f'list with values for histogram {transition} is empty')

    def make_xaxis_symmetric(self, new_x_limits):
        bigger_abs_x_value = max(abs(new_x_limits[0]), abs(new_x_limits[1]))
        new_x_limits = (- bigger_abs_x_value, bigger_abs_x_value)
        return new_x_limits

    def get_extrem_values_from_ax(self, x_limits, y_limits):
        x_pos_min, x_pos_max = list(zip(*x_limits))
        y_pos_min, y_pos_max = list(zip(*y_limits))
        new_x_limits = (min(x_pos_min), max(x_pos_max))
        new_y_limits = (min(y_pos_min), max(y_pos_max))
        return new_x_limits, new_y_limits

def calculate_weights_for_histogram(array):
    """
     When adding up the StInGRAI explanations, it can happen,
    that some intervals does not contain as many explanations as the others.
    Therefore, in order for each explanation to have the same weight in the histogram, each interval has a weight of
    1, which is distributed to all explanations in this interval.
    :param array:
    :return:
    """
    weight_for_explanation = 1 / len(array)
    weights = np.ones(shape=array.shape[0]) * weight_for_explanation
    return weights
