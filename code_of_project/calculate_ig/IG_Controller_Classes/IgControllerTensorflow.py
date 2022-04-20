import numpy as np
import tensorflow as tf
from code_of_project.calculate_ig.IG_Controller_Classes.IGControllerAbstract import IgControllerAbstract


class IgControllerTensorflow(IgControllerAbstract):
    '''

    '''


    def calculate_integrated_gradient(self, baseline, data_to_explain):
        data_to_explain = tf.cast(data_to_explain, tf.float32)
        baseline = tf.cast(baseline, tf.float32)
        current_m_steps = self.num_steps_to_calculate_path_integral
        error_approximation = self.allowed_error_approximation + 1
        while error_approximation > self.allowed_error_approximation:
            alphas = tf.linspace(start=0.0,
                                 stop=1.0,
                                 num=current_m_steps + 1)

            interpolation = interpolate(data_to_explain=data_to_explain,
                                        baseline=baseline,
                                        alphas=alphas)

            path_gradients, pred_interpolation = compute_gradients(interpolation=interpolation,
                                                                   model=self.prediction_object)

            pred_baseline = pred_interpolation[0]
            pred_data_to_explain = pred_interpolation[-1]

            ig = integral_approximation(gradients=path_gradients)
            ig_weight, dif = weighted_ig(data_to_explain.numpy(), baseline, ig)
            error_approximation, current_m_steps = self.error_of_approximation(ig_weight=ig_weight,
                                                                               dif_pred=np.abs(
                                                                                   pred_baseline - pred_data_to_explain),
                                                                               m_steps=current_m_steps,
                                                                               )
        result_integrated_gradient = {'pred_data_to_explain': pred_data_to_explain,
                                      'pred_baseline': pred_baseline,
                                      'ig_weight': ig_weight,
                                      'ig': ig,
                                      'dif': dif
                                      }
        return result_integrated_gradient


def interpolate(data_to_explain, baseline, alphas):
    alphas_x = alphas[:, tf.newaxis]  # alphas[:, tf.newaxis, tf.newaxis, tf.newaxis]
    baseline_x = tf.expand_dims(baseline, axis=0)
    input_x = tf.expand_dims(data_to_explain, axis=0)
    delta = input_x - baseline_x
    interpolation = baseline_x + alphas_x * delta
    return interpolation


def compute_gradients(interpolation, model):
    with tf.GradientTape() as tape:
        tape.watch(interpolation)
        probs = model.predict_proba(interpolation)
    return tape.gradient(target=probs, sources=interpolation), probs.numpy().flatten()


def integral_approximation(gradients):
    # riemann_trapezoidal
    grads = (gradients[:-1] + gradients[1:]) / tf.constant(2.0)
    integrated_gradients = tf.math.reduce_mean(grads, axis=0)
    return integrated_gradients.numpy()


def weighted_ig(data_to_explain, baseline, ig):
    dif = data_to_explain - baseline
    ig_weight = ig * dif
    return ig_weight.numpy(), dif

