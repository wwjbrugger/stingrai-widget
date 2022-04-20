import logging
from code_of_project.widget.helper_for_widget import check_if_data_corrupted
from code_of_project.widget.classes.StInGRAI import StInGRAI

import numpy as np
import pandas as pd


class IG_Unsegmented(StInGRAI):
    def __init__(self, ig_dics, arguments, structure_widget):
        StInGRAI.__init__(self, ig_dics, arguments, structure_widget)
        self.class_name = 'BarPlotUnsegmented'
        self.key_of_ig_dic = structure_widget['textbox_long_path_to_use']['initial_str_textfield']
        self.title_explanation_plot = ''

    def sum_explanation_in_path(self, transition):
        # there is only one dic to sum, so the method is pretty short
        if self.key_of_ig_dic in self.ig_dics:
            explanation_of_interest_per_feature, explanation_of_interest_std= self.get_explanation_in_file(transition, foldername=self.key_of_ig_dic)
            logging.info(f"Cumulated explanation sum for {transition} is {np.sum(explanation_of_interest_per_feature)}")
            self.construct_title_explanation_plot(folder_in_interval_sort_sort=[self.key_of_ig_dic])
            return explanation_of_interest_per_feature, explanation_of_interest_std

        else:
            raise ValueError(f'{self.key_of_ig_dic} is not a key in dictionary for IG long step')

    def get_explanation_in_file(self, transition, foldername):

        check_if_data_corrupted(array=self.ig_dics[foldername][transition],
                                foldername=foldername,
                                transition=transition,
                                source=self.class_name)

        avg_data_to_explain_of_one_transition = self.ig_dics[foldername][transition]
        explanation_of_interest = avg_data_to_explain_of_one_transition.mean(axis=0)
        explanation_of_interest_std =avg_data_to_explain_of_one_transition.std(axis=0)
        if self.show_std:
            return explanation_of_interest, explanation_of_interest_std
        else:
            return explanation_of_interest, self.fill_std_with_zeros(
                explanation_of_interest)
