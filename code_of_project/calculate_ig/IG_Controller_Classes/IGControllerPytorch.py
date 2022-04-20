import numpy as np
import torch
from code_of_project.calculate_ig.IG_Controller_Classes.IGControllerAbstract import IgControllerAbstract
from captum.attr import IntegratedGradients


class IGControllerPytroch(IgControllerAbstract):

    def calculate_integrated_gradient(self, baseline, data_to_explain):

        data_to_explain = torch.tensor([np.float32(data_to_explain)], requires_grad=True)
        baseline = torch.tensor([np.float32(baseline)], requires_grad=True)
        current_m_steps = self.num_steps_to_calculate_path_integral
        error_approximation = self.allowed_error_approximation + 1

        ig = IntegratedGradients(forward_func=self.prediction_object.predict_proba)
        while error_approximation > self.allowed_error_approximation:
            pred_baseline = self.prediction_object.predict_proba(data=data_to_explain)
            pred_data_to_explain = self.prediction_object.predict_proba(data=baseline)
            attributions = ig.attribute((data_to_explain),
                                        baselines=(baseline),
                                        method='gausslegendre',
                                        n_steps=current_m_steps)
            attributions = attributions.detach().numpy()[0]
            pred_baseline = pred_baseline.detach().numpy()[0][0]
            pred_data_to_explain = pred_data_to_explain.detach().numpy()[0][0]
            error_approximation, current_m_steps = self.error_of_approximation(ig_weight=attributions,
                                                                               dif_pred=np.abs(
                                                                                   pred_baseline - pred_data_to_explain),
                                                                               m_steps=current_m_steps,
                                                                               )

        result_integrated_gradient = {'pred_data_to_explain': pred_data_to_explain,
                                      'pred_baseline': pred_baseline,
                                      'ig_weight': attributions,
                                      }
        return result_integrated_gradient

