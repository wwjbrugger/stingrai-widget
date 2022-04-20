import logging
import math
import matplotlib.pyplot as plt
import code_of_project.helper_methods as helper
from project_settings import ROOT_PATH


def visualize_Spearman_correlation_and_abs_error(spearman_correlation_dic, explanation_difference_dic, arguments):
    fig = plt.figure(figsize=(12, 12))  #
    gs = fig.add_gridspec(math.ceil(len(arguments.transitions_to_calculate)**0.5),math.ceil(len(arguments.transitions_to_calculate)**0.5))
    for i, transition in enumerate(spearman_correlation_dic.keys()):
        scatter_radius, end_intervals_label, \
        spearman_correlation, start_intervals_label = get_data_for_plot(explanation_difference_dic,
                                                                        spearman_correlation_dic,
                                                                        transition)

        im = add_plot_to_ax(end_intervals_label, fig, gs, i, scatter_radius, spearman_correlation,
                            start_intervals_label, transition)
    add_colourbar(explanation_difference_dic, fig, im)

    path_to_save = ROOT_PATH / arguments.path_to_model / arguments.time_string_of_model /\
                      'integrated_gradients' / arguments.dic_with_index_time_string /\
                      f'{arguments.explanations_to_compare}_Spearman_correlation_and_abs_error.png'
    fig.savefig(fname=path_to_save)
    logging.info(f'Figures are saved to {path_to_save}')


def add_colourbar(explanation_difference_dic, fig, im):
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.1, top=0.9, left=0.1, right=0.8,
                        wspace=0.5, hspace=0.5)
    cb_ax = fig.add_axes([0.83, 0.1, 0.02, 0.8])
    cbar = fig.colorbar(im, cax=cb_ax)
    cbar.set_label(
        f"Colour = Spearman correlation coefficent \n biggest circle represents an absolute error of {explanation_difference_dic['max_abs_difference_experiment']:.2f}  ",
        loc='top')


def add_plot_to_ax(end_intervals_label, fig, gs, i, scatter_radius, spearman_correlation, start_intervals_label,
                   transition):
    ax = fig.add_subplot(gs[int(i / 2), i % 2])
    im = ax.scatter(x=start_intervals_label,
                    y=end_intervals_label,
                    c=spearman_correlation,
                    s=scatter_radius,
                    alpha=0.5,
                    cmap='RdYlGn',
                    vmin=-1,
                    vmax=1)
    for i, _ in enumerate(start_intervals_label):
        ax.text(start_intervals_label[i],end_intervals_label[i], f'{spearman_correlation [i]:.2}',
                fontdict=dict(color='k', size=10, horizontalalignment='center',
     verticalalignment='center'))
    ax.set_title(transition)
    ax.set_xlabel('Start interval', fontsize=15)
    ax.set_ylabel('End interval', fontsize=15)
    return im


def get_data_for_plot(explanation_difference_dic, spearman_correlation_dic, transition):
    start_intervals_label = []
    end_intervals_label = []
    spearman_correlation = []
    absolute_difference = []
    for file in sorted(spearman_correlation_dic[transition].keys(),
                       key=lambda x: (helper.get_interval_border_from_string(x))):
        start_point_B, end_point_B, start_point_D, end_point_D = helper.get_interval_border_from_string(file)

        start_intervals_label.append(f'{start_point_B}-{end_point_B}')
        end_intervals_label.append(f'{start_point_D}-{end_point_D}')

        spearman_correlation.append(spearman_correlation_dic[transition][file]['correlation'])

        absolute_difference.append(explanation_difference_dic[transition][file]['absolute_difference'])
        scatter_radius = (absolute_difference / explanation_difference_dic['max_abs_difference_experiment']) * 500
    return scatter_radius, end_intervals_label, spearman_correlation, start_intervals_label
