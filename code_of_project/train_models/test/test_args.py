import argparse
from project_settings import ROOT_PATH

def parse_arguments():
    # Get argparse configs from user
    parser = argparse.ArgumentParser(description='Train Net for Test')
    parser.add_argument('--experiment_name', type=str, default='Test')
    parser.add_argument('-path_to_dataset', type=str, default=f'{ROOT_PATH}/datasets/test/test_dataset.pkl', help='path to the dataset.')
    parser.add_argument('-batch', '-b', type=int, default=32)
    parser.add_argument('-epochs', '-e', type=int, default=20)

    parser.add_argument('--label_category',  type=str, default='label',
                        help='Label for signal events')


    parser.add_argument('--dense_1_neurons', type=int, default=1)
    parser.add_argument('--dense_1_activation', type=str, default='linear')
    parser.add_argument('--dense_1_dropout_rate', type=float, default=0.0)

    parser.add_argument('--use_dense_2', default=False, action="store_true")
    parser.add_argument('--dense_2_neurons', type=int, default=128)
    parser.add_argument('--dense_2_activation', type=str, default='elu')
    parser.add_argument('--dense_2_dropout_rate', type=float, default=0.4)

    parser.add_argument('--use_dense_3', default=False, action="store_true")
    parser.add_argument('--dense_3_neurons', type=int, default=128)
    parser.add_argument('--dense_3_activation', type=str, default='elu')
    parser.add_argument('--dense_3_dropout_rate', type=float, default=0.4)

    parser.add_argument('--learning_rate', type=float, default=0.001)

    args = parser.parse_args()
    return args
