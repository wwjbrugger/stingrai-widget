# main script to calculate the integrated gradients
import logging

from tqdm import tqdm

import code_of_project.helper_methods as helper
from code_of_project.calculate_ig.IG_Controller_Classes.IgControllerTensorflow import IgControllerTensorflow
from code_of_project.calculate_ig.IG_Controller_Classes.IGControllerPytorch import IGControllerPytroch

from code_of_project.calculate_ig.calculate_ig_args import get_arguments
from project_settings import ROOT_PATH


def run(arguments):
    helper.set_logger_properties(arguments=arguments)
    helper.save_obj_as_txt(obj=vars(arguments),
                           path=ROOT_PATH / arguments.path_to_model / arguments.time_string_of_model /
                                'integrated_gradients' / arguments.dic_with_index_time_string / arguments.folder_name_index /
                                'settings' / f'{arguments.interval_name}')

    logging.info(f'Interval {arguments.interval_name} is processed')

    dic_with_index_of_interesting_data = \
        helper.load_obj(ROOT_PATH / arguments.path_to_model /
                        arguments.time_string_of_model / 'dic_with_index_of_interesting_data' /
                        arguments.dic_with_index_time_string / arguments.folder_name_index / f'{arguments.interval_name}')

    model_to_explain = helper.open_model(path=ROOT_PATH / arguments.path_to_model /
                                              arguments.time_string_of_model,
                                         arguments=arguments)

    scaled_data = helper.load_obj(path=ROOT_PATH / arguments.path_to_model /
                                       arguments.time_string_of_model / 'scaled_data.pkl')
    if  arguments.framework == 'tensorflow':
        ig_controller = IgControllerTensorflow(model_to_explain=model_to_explain,
                                           data=scaled_data,
                                           arguments=arguments,
                                           )
    elif arguments.framework == 'pytorch':
        ig_controller = IGControllerPytroch(model_to_explain=model_to_explain,
                                               data=scaled_data,
                                               arguments=arguments,
                                               )
    explanation_transition_dic = {}
    for transition_name in arguments.transitions_to_calculate:
        transition_dic = dic_with_index_of_interesting_data[transition_name]
        explanation_transition = explain_paths_in_transition(
            ig_controller=ig_controller,
            transition_dic=transition_dic)
        explanation_transition_dic[transition_name] = explanation_transition
    explanation_transition_dic['feature_names'] = list(scaled_data.columns)


    helper.save_obj_as_pkl(obj=explanation_transition_dic,
                           path=ROOT_PATH / arguments.path_to_model /
                                arguments.time_string_of_model / 'integrated_gradients' /
                                arguments.dic_with_index_time_string / arguments.folder_name_index / f'{arguments.interval_name}')


def explain_paths_in_transition(ig_controller,
                                transition_dic):
    """
    Calculate all IG between data points in Data to Explain interval and data points in Baseline interval
    :param ig_controller:
    :param transition_dic:
    :return:
    """
    baseline_indices = transition_dic['baseline']
    data_to_explain_indices = transition_dic['data_to_explain']
    transition_explanation_dic = {}

    for data_to_explain_index in tqdm(data_to_explain_indices):
        explanation_dic_single_data = ig_controller.explain_single_data_to_explain(
            data_to_explain_index=data_to_explain_index,
            baseline_indices=baseline_indices)
        transition_explanation_dic[data_to_explain_index] = explanation_dic_single_data

    return transition_explanation_dic


if __name__ == '__main__':

    args = get_arguments()
    run(arguments=args)
