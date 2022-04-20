import argparse
import code_of_project.helper_methods as helper
from project_settings import ROOT_PATH
def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("--interval_name", type=str, required=True,
                        help="Specify which Interval should be processed")

    parser.add_argument('--framework', type=str, nargs='?', const=1, default='tensorflow',
                        help='Framework which was used for training the net choose between >tensorflow< or >pytorch<')

    parser.add_argument('--path_to_model', type=str, nargs='?', const=1, default=f'{ROOT_PATH}/models/test_dataset/Test',
                        help='Path from project root to model which should be explained')

    parser.add_argument('--model_to_explain_name', type=str, nargs='?', const=1, default='Test',
                        help='Name of the model for the prediction object')


    parser.add_argument('--import_statment_to_load_net', type=str, nargs='?', const=1,
                        default='code_of_project.train_models.Churn_modelling_pytorch.churn_modelling_using_ann_with_hyperparameters',
                        help='File name from where the architecture of the net can be loaded.'
                             'Only needed if pytorch is used')

    parser.add_argument('--arguments_to_load_model', type=str, nargs='?', const=1, default="{'n_inputs' : 11}",
                        help='Arguments to load neural net. Only needed when pytorch is used'
                             'argument string has to be written as dictionary. '
                             'For the parsing ast.literal_eval is used'
                             )

    parser.add_argument('--time_string_of_model', type=str, nargs='?', const=1, default='2022:04:20-10:52:35',
                        help='Time string of model which should be explained')

    parser.add_argument('--dic_with_index_time_string', type=str, nargs='?', const=1, default="2022:04:20-10:58:50",
                        help='Time string of index dictionary')

    parser.add_argument('--folder_name_index', type=str, nargs='?', const=1, default='StInGRAI',
                        help='Path from time string when integrated gradient are calculated to dictionaries with indices')

    parser.add_argument('--allowed_error_approximation', type=float, nargs='?', const=1, default="0.001",
                        help='Maximal allowed difference between (F(DtE)-F(B))- Sum IG(DtE, B)'
                             'if difference is bigger IG is calculated again with better approximation')

    parser.add_argument('--num_steps_to_calculate_path_integral', type=int, nargs='?', const=1, default=300,
                        help='Time string of index dictionary')

    parser.add_argument('--logging_level', type=str, nargs='?', const=1, default='INFO',
                        help='Level of logging. Possible values: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET ')

    parser.add_argument('--print_model_summary', type=helper.str2bool, nargs='?',
                        const=1, default=False,
                        help="Show structure of model to be explained")

    parser.add_argument('transitions_to_calculate', type=str, nargs='*',
                        default=['signal->signal', 'background->signal', 'signal->background', 'background->background'],
                        help='Name of transitions to calculate IG for')
    args = parser.parse_args()
    return args