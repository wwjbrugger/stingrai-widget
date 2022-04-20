import argparse
import time
from project_settings import ROOT_PATH
def get_arguments():
    parser = argparse.ArgumentParser(
        description='Divides the data into intervals according to their prediction value')

    parser.add_argument('--path_to_model', nargs='?', const=1, default=f'{ROOT_PATH}/models/test_dataset/Test',
                        help='Path from project root to model which should be explained')

    parser.add_argument('--time_string_of_model', nargs='?', const=1, default='2022:04:20-10:52:35',
                        help='Time string of model which should be explained')

    parser.add_argument('--name_of_prediction_file', nargs='?', const=1, default='prediction.pkl',
                        help='Name of prediction file')

    parser.add_argument('--name_of_true_label_file', nargs='?', const=1, default='true_label.pkl',
                        help='Name of true label file')
    
    parser.add_argument('--start_point_interval', type=float, nargs='?', const=1, default=0.0,
                        help='Lower boarder for intervals')

    parser.add_argument('--stop_point_interval', type=float, nargs='?', const=1, default=1,
                        help='Upper boarder for intervals')

    parser.add_argument('--number_bins', type=float, nargs='?', const=1, default=10,
                        help='Width of a interval')

    parser.add_argument('--logging_level', type=str, nargs='?', const=1, default='INFO',
                        help='Level of logging. Possible values: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET ')


    parser.add_argument('--position_to_round_border', type=float, nargs='?', const=1, default=2,
                        help='Position from which the interval limits are rounded')

    

    parser.add_argument('--number_elements_in_intervals', type=int, nargs='?', const=1, default=50,
                        help='How many should be in the interval')

    parser.add_argument('--signal_label', type=int, nargs='?', const=1, default=1,
                        help='Label for signal events')

    parser.add_argument('--background_label', type=int, nargs='?', const=1, default=0,
                        help='Label for background events')

    parser.add_argument('--dic_with_index_time_string', nargs='?', const=1,
                        default=f"{time.strftime('%Y:%m:%d-%H:%M:%S')}",
                        help='Time string for saving the index dictionary')

    parser.add_argument('--compare_values_in_same_interval', nargs='?', const=1,
                        default='true',
                        help='If values in the same interval should be compared with each other')


    arguments = parser.parse_args()
    return arguments
