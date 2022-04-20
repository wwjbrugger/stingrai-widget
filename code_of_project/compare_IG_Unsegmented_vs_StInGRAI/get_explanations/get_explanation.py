import code_of_project.helper_methods as helper
from code_of_project.compare_IG_Unsegmented_vs_StInGRAI.get_explanations.get_explanation_args import get_arguments
from code_of_project.widget.helper_for_widget import get_all_ig_dics
from code_of_project.widget.classes.StInGRAI import StInGRAI
from code_of_project.widget.classes.IG_Unsegmented import IG_Unsegmented
from code_of_project.helper_methods import  get_interval_border_from_string
from project_settings import ROOT_PATH
import collections

def run(args):
    ig_dics_StInGRAI = get_all_ig_dics(arguments=args,
                                          path_to_ig_dics=ROOT_PATH / args.path_to_model /
                                                          args.time_string_of_model / 'integrated_gradients' /
                                                          args.dic_with_index_time_string / args.path_to_ig_dic_StInGRAI)

    ig_dics_unsegmented = get_all_ig_dics(arguments=args,
                                            path_to_ig_dics=ROOT_PATH / args.path_to_model /
                                                            args.time_string_of_model / 'integrated_gradients' /
                                                            args.dic_with_index_time_string / args.path_to_ig_dic_unsegmented)

    bar_plot_obj_StInGRAI = get_bar_plot_obj_StInGRAI(args=args, ig_dics_StInGRAI=ig_dics_StInGRAI)

    IG_unsegmented_obj = get_IG_unsegmented_obj(args=args,
                                                          ig_dics_unsegmented=ig_dics_unsegmented)

    explanations = collections.defaultdict(dict)
    explanations['feature_names'] = args.feature_names
    for file_name in ig_dics_unsegmented.keys():
        add_explanations_for_file(IG_unsegmented_obj, bar_plot_obj_StInGRAI, explanations, file_name)

    helper.save_obj_as_pkl(obj=explanations,
                           path=ROOT_PATH / args.path_to_model / args.time_string_of_model /
                                'integrated_gradients' / args.dic_with_index_time_string / 'explanations_to_compare'
                           )


def add_explanations_for_file(IG_unsegmented_obj, bar_plot_obj_StInGRAI, explanations, file_name):
    start_point_B, end_point_B, start_point_D, end_point_D = get_interval_border_from_string(file_name)
    exp_StInGRAI = StInGRAI_explantion(StInGRAI_obj=bar_plot_obj_StInGRAI,
                                               start_point=start_point_B,
                                               stop_point=end_point_D)
    explanations['StInGRAI'][file_name] = exp_StInGRAI
    exp_unsegmented = ig_unsegmented_step_explantion(IG_unsegmented_obj=IG_unsegmented_obj,
                                             key_of_ig_dic=file_name)
    explanations['unsegmented'][file_name] = exp_unsegmented


def get_bar_plot_obj_StInGRAI(args, ig_dics_StInGRAI):
    # The structur_widget dictionary is not needed so we fill it with dummy variables
    nested_dict = lambda: collections.defaultdict(nested_dict)
    structure_widget = nested_dict()
    structure_widget ['slider_baseline']['args']['valinit'] = 0
    structure_widget ['slider_data_to_explain']['args']['valinit'] = 1
    structure_widget['check_buttons_std']['args']['actives'][0] = True
    structure_widget['slider_when_to_change_transition']['args']['valinit'] = args.fraction_change_transition

    bar_plot_obj_StInGRAI=StInGRAI(ig_dics=ig_dics_StInGRAI,
                                          arguments=args,
                                          structure_widget=structure_widget)
    return bar_plot_obj_StInGRAI

def get_IG_unsegmented_obj(args, ig_dics_unsegmented):
    # The structur_widget dictionary is not needed so we fill it with dummy variables
    nested_dict = lambda: collections.defaultdict(nested_dict)
    structure_widget = nested_dict()
    structure_widget['slider_baseline']['args']['valinit'] = 0
    structure_widget['slider_data_to_explain']['args']['valinit'] = 1
    structure_widget['check_buttons_std']['args']['actives'][0] = True
    structure_widget['textbox_long_path_to_use']['initial_str_textfield'] = None

    IG_unsegmented_obj = IG_Unsegmented(ig_dics=ig_dics_unsegmented,
                                         arguments=args,
                                         structure_widget=structure_widget)
    return IG_unsegmented_obj


def StInGRAI_explantion(StInGRAI_obj, start_point, stop_point):
    StInGRAI_obj.start_point = start_point
    StInGRAI_obj.stop_point = stop_point
    exp = StInGRAI_obj.calculate_explanations_of_transitions()
    return exp

def ig_unsegmented_step_explantion(IG_unsegmented_obj, key_of_ig_dic):
    IG_unsegmented_obj.key_of_ig_dic = key_of_ig_dic

    exp = IG_unsegmented_obj.calculate_explanations_of_transitions()
    return exp



if __name__ == '__main__':
    args = get_arguments()
    helper.set_logger_properties(args)
    run(args)

