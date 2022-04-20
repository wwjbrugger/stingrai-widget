from code_of_project.widget.classes.IGPlotsController import IGPlotsController
from code_of_project.widget.helper_for_widget import get_files_between_start_and_stop_point, \
    check_if_data_corrupted
from code_of_project.exceptions import NoValuesInIntervalError
from code_of_project.widget.classes.TransitionToUseController import TransitionToUseController
import pandas as pd
import numpy as np
import logging


def get_explanation_in_file(ig_dics, TransitionToUseController_obj, folder_name, transition, show_std):
    transition_to_use = TransitionToUseController_obj.choose_transition_to_use(transition)
    dic = ig_dics[folder_name]
    check_if_data_corrupted(array=dic[transition_to_use], foldername=folder_name,
                            transition=transition_to_use, source='StInGRAI')
    explanation = np.mean(dic[transition_to_use], axis=0)
    if show_std:
        return explanation, np.std(dic[transition_to_use], axis=0)
    else:
        return explanation, None


class StInGRAI:
    def __init__(self, ig_dics, arguments, structure_widget):
        self.class_name = 'StInGRAI'
        self.transition_list = arguments.transitions_to_calculate.copy()
        self.transition_list_static = arguments.transitions_to_calculate.copy()
        self.start_point = structure_widget['slider_baseline']['args']['valinit']
        self.stop_point = structure_widget['slider_data_to_explain']['args']['valinit']
        self.show_std = structure_widget['check_buttons_std']['args']['actives'][0]
        self.ig_dics = ig_dics
        self.fraction_change_transition = structure_widget['slider_when_to_change_transition']['args']['valinit']
        self.feature_to_show = structure_widget['textbox_feature_to_show']['initial_str_textfield']
        self.feature_in_barplot = []
        self.arguments = arguments
        self.title_explanation_plot = ''

        self.label = {
            'signal->signal': 'pos -> pos',
            'background->signal': 'neg -> pos',
            'signal->background': 'pos -> neg',
            'background->background': 'neg -> neg'
        }

    def calculate_explanations_of_transitions(self):
        logging.info(f'{self.class_name} object is used \n')
        cumulated_explanation = {'ig_weight_mean': {},
                                 'ig_weight_std': {}}
        for transition in self.transition_list_static:
            if transition in self.transition_list:
                try:
                    explanation, std_explanation = self.sum_explanation_in_path(transition)
                    cumulated_explanation['ig_weight_mean'][transition] = explanation
                    cumulated_explanation['ig_weight_std'][transition] = std_explanation
                except NoValuesInIntervalError:
                    logging.info(f'Transition: {transition} is skipped for barplot')

        self.cumulated_explanation = cumulated_explanation
        return cumulated_explanation

    def sum_explanation_in_path(self, transition):

        folder_in_interval_sort = get_files_between_start_and_stop_point(list_with_folder=list(self.ig_dics.keys()),
                                                                         start_point=self.start_point,
                                                                         stop_point=self.stop_point)
        self.construct_title_explanation_plot(folder_in_interval_sort)

        TransitionToUseController_obj = TransitionToUseController(num_of_transition=len(folder_in_interval_sort),
                                                                  fraction_change_transition=self.fraction_change_transition)
        explanation_of_interest = {}
        explanation_of_interest_std = {}
        for folder_name in folder_in_interval_sort:
            explanation_in_file, explanation_in_file_std = \
                get_explanation_in_file(ig_dics=self.ig_dics,
                                        TransitionToUseController_obj=TransitionToUseController_obj,
                                        folder_name=folder_name,
                                        transition=transition,
                                        show_std=self.show_std)

            explanation_of_interest[folder_name] = explanation_in_file
            explanation_of_interest_std[folder_name] = explanation_in_file_std

        explanation_of_interest_df = pd.DataFrame.from_dict(explanation_of_interest, orient='index')
        explanation_of_interest_std_df = pd.DataFrame.from_dict(explanation_of_interest_std, orient='index')

        explanation_of_interest_per_feature = explanation_of_interest_df.sum(axis=0)
        logging.info(f"Cumulated explanation sum for {transition} is {np.sum(explanation_of_interest_per_feature)}")

        if self.show_std:
            return explanation_of_interest_per_feature, explanation_of_interest_std_df.mean(axis=0)
        else:
            return explanation_of_interest_per_feature, self.fill_std_with_zeros(explanation_of_interest_per_feature)

    def fill_std_with_zeros(self, cumulated_explanation):
        return pd.Series(np.zeros(np.array(cumulated_explanation).shape), index=cumulated_explanation.index)

    def construct_title_explanation_plot(self, folder_in_interval_sort_sort):
        first_segment = folder_in_interval_sort_sort[0].replace('.pkl', '')
        last_segment = folder_in_interval_sort_sort[-1].replace('.pkl', '')
        first_interval = first_segment.split('->')[0]
        last_interval = last_segment.split('->')[-1]
        self.title_explanation_plot = f"[{first_interval}] -> [{last_interval}]"

    def plot_cumulated_explanation(self, ax, bar_chart_parameter):
        if self.cumulated_explanation['ig_weight_mean']:
            # we have explanation to plot
            wanted_features = self.get_wanted_features(features_to_show=self.feature_to_show)
            self.select_wanted_features(wanted_features)
            self.set_feature_used_in_barplot(bar_chart_parameter)

            multiple_histograms_controller = IGPlotsController()
            multiple_histograms_controller.add_multiple_bar_plots(ax=ax, parameter=bar_chart_parameter['args'],
                                                                  y_values_list=list(self.cumulated_explanation[
                                                                                         'ig_weight_mean'].values()),
                                                                  std_y_values=list(
                                                                      self.cumulated_explanation['ig_weight_std'].values()),
                                                                  title_bar_plot=self.title_explanation_plot)
        else:
            # we have no values to plot
            logging.info('There is no explanation to plot ')
            ax.clear()
    def get_wanted_features(self, features_to_show):
        try:
            features_to_show = int(features_to_show)
        except ValueError as verr:
            pass

        if features_to_show == 'All':
            key = list(self.cumulated_explanation['ig_weight_mean'].keys())[0]
            wanted_features = list(self.cumulated_explanation['ig_weight_mean'][key].index)
        elif isinstance(features_to_show, int):
            wanted_features = self.get_x_biggest_features(features_to_show)
        elif isinstance(features_to_show, str):
            wanted_features = features_to_show.split(sep=' ')
        wanted_features.sort()
        return wanted_features

    def get_x_biggest_features(self, number_features_to_show):
        # sum abs value of all transitions select n biggest features
        df = pd.concat(self.cumulated_explanation['ig_weight_mean'].values(), axis=1)
        df_abs = df.abs()
        series_sum = df_abs.sum(axis=1)
        wanted_features = list(series_sum.nlargest(number_features_to_show).index)
        return wanted_features

    def select_wanted_features(self, wanted_features):
        for transition in self.cumulated_explanation['ig_weight_mean'].keys():
            self.cumulated_explanation['ig_weight_mean'][transition] \
                = self.cumulated_explanation['ig_weight_mean'][transition].loc[wanted_features]

            self.cumulated_explanation['ig_weight_std'][transition] \
                = self.cumulated_explanation['ig_weight_std'][transition].loc[wanted_features]

    def set_feature_used_in_barplot(self, bar_chart_parameter):
        bar_chart_parameter['args']['legend'] = [self.label[key] for key in self.cumulated_explanation['ig_weight_mean'].keys()]
        key = list(self.cumulated_explanation['ig_weight_mean'].keys())[0]
        features = list(self.cumulated_explanation['ig_weight_mean'][key].index)
        bar_chart_parameter['args']['xtick_label'] = features
        self.feature_in_barplot = features
