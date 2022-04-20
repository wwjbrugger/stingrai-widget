import numpy as np
import code_of_project.helper_methods as helper
from code_of_project.prediction_object.PredictionObject import PredictionObject
import logging


class IgControllerAbstract:
    '''

    '''
    def __init__(self, model_to_explain, data, arguments, **kwargs):
        self.data = data
        self.prediction_object = PredictionObject(model_to_explain=model_to_explain,
                                                          arguments=arguments)
        self.allowed_error_approximation = arguments.allowed_error_approximation
        self.num_steps_to_calculate_path_integral = arguments.num_steps_to_calculate_path_integral
        self.kwargs = kwargs

    def explain_single_data_to_explain(self, data_to_explain_index, baseline_indices):
        '''
        Calculate IG between a data to explain and a list of baselines
        :param data_to_explain_index: int
                index of the data point to be explained
        :param baseline_indices: [int]
                list with indices of data points used as baseline
        :return: dictionary with IG's between baselines and data to explain
        '''
        results_baselines = {}
        for baseline_index in baseline_indices:
            results_baselines['baseline_index_{}'.format(baseline_index)] = \
                self.calculate_ig_from_baseline_to_data_to_explain(
                    baseline_index=baseline_index,
                    data_to_explain_index=data_to_explain_index
                )
        return results_baselines

    def calculate_ig_from_baseline_to_data_to_explain(self, baseline_index, data_to_explain_index):
        data_to_explain = self.data.iloc[data_to_explain_index]
        baseline = self.data.iloc[baseline_index]

        result_integrated_gradient_dic = \
            self.calculate_integrated_gradient(baseline, data_to_explain)

        result_integrated_gradient_dic['data_to_explain_index'] = data_to_explain_index
        result_integrated_gradient_dic['baseline_index'] = baseline_index

        return result_integrated_gradient_dic

    def calculate_integrated_gradient(self, baseline, data_to_explain):
        raise NotImplementedError('This method has to be defined in child class')

    def error_of_approximation(self, ig_weight, dif_pred, m_steps):
        integral = np.abs(np.sum(ig_weight))
        error = np.abs(dif_pred - integral)
        if error >= self.allowed_error_approximation:
            m_steps_new = m_steps * 2
            logging.debug('f"Integration approximation is with a error of {error}'
                          ' to high, number m_steps = {m_steps} is risen to {m_steps_new} for next try')
            return error, m_steps_new
        else:
            return error, m_steps


def interpolate(data_to_explain, baseline, alphas):
    raise NotImplementedError('This method has to be defined in concrete class')


def compute_gradients(interpolation, model):
    raise NotImplementedError('This method has to be defined in concrete class')


def integral_approximation(gradients):
    raise NotImplementedError('This method has to be defined in concrete class')


def weighted_ig(data_to_explain, baseline, ig):
    raise NotImplementedError('This method has to be defined in concrete class')

