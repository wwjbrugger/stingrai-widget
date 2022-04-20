from pathlib import Path

import pandas as pd

import code_of_project.helper_methods as helper
import numpy as np
from tqdm import tqdm
import logging
from code_of_project.exceptions import NoValuesInIntervalError


def get_all_ig_dics(arguments, path_to_ig_dics):
    ig_dic = {}
    logging.info('Start loading IG')
    for folder in tqdm(list(Path(path_to_ig_dics).iterdir())):
        if folder.name != 'settings':
            start_point_B, end_point_B, start_point_D, end_point_D = helper.get_interval_border_from_string(folder.name)
            if check_if_StInGRAI_interval_is_relevant(arguments, end_point_D, start_point_B):
                ig_dic[folder.name] = {}
                integrated_gradient_dic = helper.load_obj(path=folder)
                for transition_name in arguments.transitions_to_calculate:
                    get_all_explanation_in_transition(arguments, folder, ig_dic, integrated_gradient_dic, transition_name)
    logging.info('Done loading IG')
    return ig_dic


def check_if_StInGRAI_interval_is_relevant(arguments, end_point_D, start_point_B):
    return arguments.ig_dic_StInGRAI_start_point <= start_point_B and end_point_D <= arguments.ig_dic_StInGRAI_stop_point


def get_all_explanation_in_transition(arguments, folder, ig_dic, integrated_gradient_dic, transition_name):
    transition_dic = integrated_gradient_dic[transition_name]
    all_ig = []
    for data_to_explain_index, data_to_explain_dic in transition_dic.items():
        data_to_explain_ig = get_all_explanations_of_a_data_to_explain(data_to_explain_dic)
        all_ig=add_average_data_to_explain_explanation_or_all_ig(all_ig, arguments, data_to_explain_ig)
    ig_dic[folder.name][transition_name] = pd.DataFrame(all_ig, columns=integrated_gradient_dic['feature_names'])



def add_average_data_to_explain_explanation_or_all_ig(all_ig, arguments, data_to_explain_ig):
    if data_to_explain_ig:
        if arguments.use_avrg_explanation_of_data_points:
            all_ig.append(np.mean(data_to_explain_ig.copy(), axis=0))
        else:
            all_ig.append(np.array(data_to_explain_ig.copy()))
    return all_ig


def get_all_explanations_of_a_data_to_explain(data_to_explain_dic):
    data_to_explain_ig = []
    for baseline_index, baseline_dic in data_to_explain_dic.items():
        data_to_explain_ig.append(baseline_dic['ig_weight'])
    return data_to_explain_ig

def check_if_data_corrupted(array, foldername, transition, source):
    if  array.ndim != 2 or array.empty:
        logging.info('-')
        logging.info(
            f'warning source is {source}\n'
            f'Integrated gradient array for the folder {foldername} and transition {transition} is not 2 dimensional and can\'t be used \n'
            f'Missing data points in the interval can be a reason for this massage. The array values are: {array}'
        )
        raise NoValuesInIntervalError()

def get_files_between_start_and_stop_point(list_with_folder, start_point, stop_point):
    files_in_interval = []
    files_in_interval_with_start_and_end_in_same_interval = []
    start_points_B_list = []
    for folder_name in list_with_folder:
        start_point_B, end_point_B, start_point_D, end_point_D = helper.get_interval_border_from_string(folder_name)
        if start_point <= start_point_B and end_point_D <= stop_point:
            if start_point_D != start_point_B:
                files_in_interval.append(folder_name)
                start_points_B_list.append(start_point_B)
            elif start_point_D == start_point_B:
                files_in_interval_with_start_and_end_in_same_interval.append(folder_name)

    if len(files_in_interval) == 0:
        return files_in_interval_with_start_and_end_in_same_interval
    index_array_for_sort = np.argsort(start_points_B_list)
    folder_in_interval_sort = np.array(files_in_interval)[index_array_for_sort]
    return folder_in_interval_sort




