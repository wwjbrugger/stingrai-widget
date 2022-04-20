import collections
import logging

import numpy as np
from scipy import stats

import code_of_project.helper_methods as helper
from code_of_project.compare_IG_Unsegmented_vs_StInGRAI.compare.compare_args import get_arguments
from code_of_project.compare_IG_Unsegmented_vs_StInGRAI.compare.visualize_comparision_results import visualize_Spearman_correlation_and_abs_error
from project_settings import ROOT_PATH


def run():
    args = get_arguments()
    helper.set_logger_properties(arguments=args)
    explanations = helper.load_obj(path=ROOT_PATH / args.path_to_model / args.time_string_of_model /
                                        'integrated_gradients' / args.dic_with_index_time_string / f'{args.explanations_to_compare}.pkl')

    spearman_correlation = calculate_spearman_correlation(args, explanations)

    explanation_difference = calculate_absolute_error(args, explanations)

    visualize_Spearman_correlation_and_abs_error(spearman_correlation_dic=spearman_correlation,
                                                     explanation_difference_dic=explanation_difference,
                                                     arguments=args)


def calculate_absolute_error(args, explanations):
    logging.info('absolute error is calculated')
    explanation_difference = collections.defaultdict(dict)
    explanation_difference['max_abs_difference_experiment'] = 0
    for transition in args.transitions_to_calculate:
        for file in explanations['unsegmented'].keys():
            try:
                exp_StInGRAI, exp_unsegmented = get_unsegmented_and_StInGRAI_explanations(explanations, file, transition)
                add_absolute_error(exp_unsegmented, exp_StInGRAI, explanation_difference, file, transition)
            except KeyError:
                print(f'{file} could not be calculated')

    return explanation_difference


def calculate_spearman_correlation(args, explanations):
    logging.info('spearman correlation is calculated')
    spearman_correlation = collections.defaultdict(dict)
    for transition in args.transitions_to_calculate:
        for file in explanations['unsegmented'].keys():
            try:
                exp_StInGRAI, exp_unsegmented = get_unsegmented_and_StInGRAI_explanations(explanations, file, transition)
                add_spearman_correlation_coefficent(exp_unsegmented, exp_StInGRAI, file, spearman_correlation,
                                                transition)
            except KeyError:
                print(f'{file} could not be calculated')
    return spearman_correlation


def get_unsegmented_and_StInGRAI_explanations(explanations, file, transition):
    exp_unsegmented = explanations['unsegmented'][file]['ig_weight_mean'][transition]
    exp_StInGRAI = explanations['StInGRAI'][file]['ig_weight_mean'][transition]
    return exp_StInGRAI, exp_unsegmented


def add_absolute_error(exp_unsegmented, exp_StInGRAI, explanation_difference, file, transition):
    explanation_difference[transition][file] = {}
    difference = np.array(exp_unsegmented) - np.array(exp_StInGRAI)
    abs_difference = np.sum(np.abs(difference))
    explanation_difference[transition][file]['absolute_difference'] = abs_difference
    if abs_difference > explanation_difference['max_abs_difference_experiment']:
        explanation_difference['max_abs_difference_experiment'] = abs_difference


def add_spearman_correlation_coefficent(exp_unsegmented, exp_StInGRAI, file, spearman_correlation, transition):
    spearman_correlation[transition][file] = {}
    correlation, pvalue = stats.spearmanr(exp_unsegmented, exp_StInGRAI)
    spearman_correlation[transition][file]['correlation'] = correlation
    spearman_correlation[transition][file]['pvalue'] = pvalue



if __name__ == '__main__':
    run()
