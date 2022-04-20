import argparse
import time
from project_settings import ROOT_PATH
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_to_model', type=str, nargs='?', const=1,
                        default=f'{ROOT_PATH}/models/test_dataset/Test',
                        help='Path from project root to model which should be explained')

    parser.add_argument('--time_string_of_model', type=str, nargs='?', const=1, default='2022:04:20-10:52:35',
                        help='Time string of model which should be explained')

    parser.add_argument('--time_string_dic_with_index_of_interesting_data', type=str, nargs='?', const=1,
                        default="2022:04:20-10:58:50",
                        help='Time string of index dictionary')

    parser.add_argument('--path_to_ig_dic_StInGRAI', type=str, nargs='?', const=1, default='StInGRAI',
                        help='Path from time string integrated gradient to dictionaries with precalculated ig_StInGRAI')

    parser.add_argument('--path_to_ig_dic_unsegmented', type=str, nargs='?', const=1, default='unsegmented',
                        help='Path from time string integrated gradient to dictionaries with precalculated ig_unsegmented_steps')

    parser.add_argument('--start_point_list', nargs='*', type=str,
                        default=['0.0-0.1->0.1-0.2.pkl', '0.2-0.3->0.3-0.4.pkl', '0.4-0.5->0.5-0.6.pkl',
                                 '0.6-0.7->0.7-0.8.pkl', '0.8-0.9->0.9-1.0.pkl'],
                        help='List of interval names to be used as starting points for the IG.')

    parser.add_argument('--transitions_to_use', nargs='*', type=str,
                        default=['signal->signal', 'background->signal', 'signal->background', 'background->background'],
                        help='transitions to calculate ig_unsegmented_steps ')

    parser.add_argument('--end_point_list', nargs='*', type=str,
                        default=['0.2-0.3->0.3-0.4.pkl', '0.4-0.5->0.5-0.6.pkl', '0.6-0.7->0.7-0.8.pkl',
                                 '0.8-0.9->0.9-1.0.pkl'],
                        help='List of interval names to be used as ends points for the IG.')

    args = parser.parse_args()
    return args