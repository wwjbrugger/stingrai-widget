from code_of_project.widget.classes.Feature_Histogram_StInGRAI import Feature_Histogram_StInGRAI, calculate_weights_for_histogram
from code_of_project.widget.helper_for_widget import check_if_data_corrupted
import numpy as np
class Feature_Histogram_IG_Unsegmented(Feature_Histogram_StInGRAI):
    def __init__(self, ig_dics, arguments, structure_widget):
        Feature_Histogram_StInGRAI.__init__(self, ig_dics, arguments, structure_widget)
        self.key_of_ig_dic = structure_widget['textbox_long_path_to_use']['initial_str_textfield']
        self.intervals_in_explanation = 1



    def get_all_paths_of_one_feature_in_transition(self, feature_index, transition):
        all_ig_of_feature = self.ig_dics[self.key_of_ig_dic][transition]
        check_if_data_corrupted(array=all_ig_of_feature,
                                foldername=self.key_of_ig_dic,
                                transition=transition,
                                source='histogram long step')
        all_ig_of_feature = all_ig_of_feature.loc[:, feature_index]
        all_ig_of_feature_weights = calculate_weights_for_histogram(all_ig_of_feature)
        return all_ig_of_feature, all_ig_of_feature_weights
