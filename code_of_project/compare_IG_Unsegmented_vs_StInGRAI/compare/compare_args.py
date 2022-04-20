import argparse
import code_of_project.helper_methods as helper
from project_settings import ROOT_PATH

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_to_model', type=str, nargs='?', const=1, default=f'{ROOT_PATH}/models/test_dataset/Test',
                        help='Path from project root to model which should be explained')

    parser.add_argument('--time_string_of_model', type=str, nargs='?', const=1, default='2022:04:20-10:52:35',
                        help='Time string of model which should be explained')

    parser.add_argument('--dic_with_index_time_string', type=str, nargs='?', const=1, default="2022:04:20-10:58:50",
                        help='Time string of index dictionary')

    parser.add_argument('--explanations_to_compare', type=str, nargs='?', const=1, default="explanations_to_compare",
                        help='Time string of index dictionary')

    parser.add_argument('--path_to_ig_dic_StInGRAI', type=str, nargs='?', const=1, default='StInGRAI',
                        help='Path from time string integrated gradient to dictionaries with precalculated ig_StInGRAI')

    parser.add_argument('--path_to_ig_dic_unsegmented', type=str, nargs='?', const=1, default='unsegmented',
                        help='Path from time string integrated gradient to dictionaries with precalculated ig_unsegmented_steps')

    parser.add_argument('--feature_names', nargs='*', type=str,
                       default=['A', 'B', 'C', 'D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'],
                        help='Column name of the features in the dataset')

    parser.add_argument('transitions_to_calculate', type=str, nargs='*',
                        default=['signal->signal', 'background->signal', 'signal->background', 'background->background'],
                        help='Name of transitions to calculate IG for')

    parser.add_argument('--ig_dic_StInGRAI_start_point', type=float, nargs='?', const=1, default="0.0",
                        help='Starting point from which the IG dics of the StInGRAI approach are loaded')

    parser.add_argument('--ig_dic_StInGRAI_stop_point', type=float, nargs='?', const=1, default="1",
                        help='Stop point from which the IG dics of the StInGRAI approach are loaded')

    parser.add_argument('--use_avrg_explanation_of_data_points', type=helper.str2bool, nargs='?',
                        const=1, default=True,
                        help="After reading the IG_StInGRAI from files the IG has to be hold in RAM. \n"
                             "Two modes are supported.\n"
                             " If the variable is set to False, all IG are loaded in the RAM.\n"
                             "If the variable is set to True,"
                             " the average explanation for the Data to Explain is calculated and stored in the RAM.")

    parser.add_argument('--logging_level', type=str, nargs='?', const=1, default='INFO',
                        help='Level of logging. Possible values: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET ')

    parser.add_argument('--calculate_Spearman_correlation_coefficent', type=helper.str2bool, nargs='?',
                        const=1, default=True,
                        help="Should the Spearman correlation coefficient between the ig_StInGRAI"
                             " and ig_unsegmented_steps be calculated?")

    parser.add_argument('--visualize_Spearman_correlation_and_abs_error', type=helper.str2bool, nargs='?',
                        const=1, default=True,
                        help="Should the Spearman correlation coefficient and the absolute error be visualized together?")

    parser.add_argument('--calculate_absolute_error', type=helper.str2bool, nargs='?',
                        const=1, default=True,
                        help="Calculate the absolute error between ig_StInGRAI and ig_unsegmented_steps")

    args = parser.parse_args()
    return args
