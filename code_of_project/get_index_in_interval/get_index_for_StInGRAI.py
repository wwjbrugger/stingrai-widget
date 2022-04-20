import logging

import numpy as np
from project_settings import ROOT_PATH
from scipy import stats
from code_of_project.helper_methods import load_obj, set_logger_properties, save_obj_as_pkl, \
    check_if_at_least_one_transition_is_complete
from code_of_project.get_index_in_interval.get_index_in_interval_args import get_arguments
from pathlib import Path


def run(arguments):
    prediction = load_obj(ROOT_PATH / arguments.path_to_model /
                          arguments.time_string_of_model / arguments.name_of_prediction_file)
    flatten_prediction = prediction.flatten()
    true_label_array = load_obj(ROOT_PATH / arguments.path_to_model /
                          arguments.time_string_of_model / arguments.name_of_true_label_file)

    count, bin_edges, binnumber_array = stats.binned_statistic(x=flatten_prediction,
                                                               values= flatten_prediction,
                                                               statistic='count',
                                                               bins=arguments.number_bins,
                                                               range=(arguments.start_point_interval,arguments.stop_point_interval))
    interval_names_dic = get_interval_names(bin_edges, count)

    interval_dic=populate_interval_dic_with_empty_list(interval_names_dic=interval_names_dic, first_keys = ['signal', 'background'])

    fill_interval_dic(arguments, binnumber_array, interval_dic, interval_names_dic, true_label_array)

    interval_dic = sample_requested_number_of_elements(interval_dic = interval_dic ,first_keys = ['signal', 'background'], arguments=arguments)
    save_index_intervals(arguments, interval_dic, mode_signal_interval='next_interval')
    if arguments.compare_values_in_same_interval == 'true':
        save_index_intervals(arguments, interval_dic, mode_signal_interval='same_interval_as_baseline')


def save_index_intervals(arguments, interval_dic, mode_signal_interval):
    logging.info('Save intervals')
    interval_name_keys = list(interval_dic['signal'].keys())
    for i in range(0, len(interval_name_keys) - 1, 1):
        baseline_interval = interval_name_keys[i]
        if mode_signal_interval == 'same_interval_as_baseline':
            signal_interval = interval_name_keys[i]
        elif mode_signal_interval =='next_interval':
            signal_interval = interval_name_keys[i + 1]
        interval_name = f'{baseline_interval}->{signal_interval}'
        index_dic = {}
        for Baseline_region in ['signal', 'background']:
            for Signal_region in ['signal', 'background']:
                transition = f'{Baseline_region}->{Signal_region}'
                index_dic[transition] = {}
                index_dic[transition]['baseline'] = interval_dic[Baseline_region][baseline_interval]
                index_dic[transition]['data_to_explain'] = interval_dic[Signal_region][signal_interval]
        path_to_save = Path(ROOT_PATH / arguments.path_to_model / arguments.time_string_of_model / \
                       'dic_with_index_of_interesting_data' / arguments.dic_with_index_time_string / \
                       'StInGRAI' / f'{interval_name}.pkl')
        if check_if_at_least_one_transition_is_complete(dic=index_dic, file_name=path_to_save.stem):
            save_obj_as_pkl(path=path_to_save, obj=index_dic)


def fill_interval_dic(arguments, binnumber_array, interval_dic, interval_names_dic, true_label_array):
    signal_label = np.where(true_label_array == arguments.signal_label, True, False)
    for index, true_label in enumerate(true_label_array):
        bin_number = binnumber_array[index] - 1
        try:
            interval_name = interval_names_dic[bin_number]
            if signal_label[index]:
                interval_dic['signal'][interval_name].append(index)
            else:
                interval_dic['background'][interval_name].append(index)
        except KeyError:
            logging.warning(f'Data point {index} with bin_number {bin_number} '
                            f'is not in the set prediction limits.')


def populate_interval_dic_with_empty_list(interval_names_dic, first_keys):
    interval_dic = {}
    for key in first_keys:
        interval_dic[key] = {}
        for interval_names in interval_names_dic.values():
            interval_dic[key][interval_names] = []
    return interval_dic



def get_interval_names(bin_edges, count):
    interval_names = {}
    for bin_number in range(len(count)):
        interval_names[bin_number] = f'{bin_edges[bin_number]:.6}-{bin_edges[bin_number + 1]:.6}'
    return interval_names


def count_empty_intervals(dic_with_lists):
    error_code = 0
    for key, values in dic_with_lists.items():
        if len(values)==0:
            logging.info(f'Interval {key} is empty')
            error_code +=1
    return error_code

def sample_requested_number_of_elements(interval_dic, first_keys, arguments):
    logging.info('sample the requested number of elements for each index region')
    for key in first_keys:
        for interval_name, interval in interval_dic[key].items():
            temp = np.random.choice(a=interval,
                             size=min(len(interval),
                                      arguments.number_elements_in_intervals),
                             replace=False)
            interval_dic[key][interval_name] = temp
    return interval_dic

if __name__ == '__main__':
    arguments = get_arguments()
    set_logger_properties(arguments)
    run(arguments)