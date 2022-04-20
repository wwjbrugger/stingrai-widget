import code_of_project.helper_methods as helper
from code_of_project.widget.widget_args import get_arguments
from code_of_project.widget.helper_for_widget import get_all_ig_dics
from code_of_project.widget.classes.StInGRAI import StInGRAI
from code_of_project.widget.classes.IG_Unsegmented import IG_Unsegmented
from code_of_project.widget.classes.Feature_Histogram_StInGRAI import Feature_Histogram_StInGRAI
from code_of_project.widget.classes.Feature_Histogram_IG_Unsegmented import Feature_Histogram_IG_Unsegmented
from code_of_project.widget.controll_widget.settings_structur_widget import get_settings_structur_widget
from code_of_project.widget.controll_widget.create_and_update_Widget import Widget

from project_settings import ROOT_PATH

if __name__ == '__main__':
    args = get_arguments()
    helper.set_logger_properties(args)
    structure_widget = get_settings_structur_widget(arguments=args)

    ig_dics_StInGRAI = get_all_ig_dics(arguments=args,
                                          path_to_ig_dics=ROOT_PATH / args.path_to_model /
                                                          args.time_string_of_model / 'integrated_gradients' /
                                                          args.dic_with_index_time_string / args.path_to_ig_dic_StInGRAI)

    ig_dics_unsegmented = get_all_ig_dics(arguments=args,
                                            path_to_ig_dics=ROOT_PATH / args.path_to_model /
                                                            args.time_string_of_model / 'integrated_gradients' /
                                                            args.dic_with_index_time_string / args.path_to_ig_dic_unsegmented)

    bar_plot_obj_StInGRAI = StInGRAI(ig_dics=ig_dics_StInGRAI,
                                            arguments=args,
                                            structure_widget=structure_widget)

    bar_plot_obj_unsegmented = IG_Unsegmented(ig_dics=ig_dics_unsegmented, arguments=args,
                                            structure_widget=structure_widget)

    feature_histogram_obj_StInGRAI = Feature_Histogram_StInGRAI(ig_dics=ig_dics_StInGRAI,
                                                                    arguments=args,
                                                                    structure_widget=structure_widget)
    feature_histogram_obj_unsegmented = Feature_Histogram_IG_Unsegmented(ig_dics=ig_dics_unsegmented,
                                                                    arguments=args,
                                                                    structure_widget=structure_widget)
    widget_obj = Widget(arguments=args,
                        structure_widget=structure_widget,
                        bar_plot_obj_StInGRAI=bar_plot_obj_StInGRAI,
                        feature_histogram_obj_StInGRAI=feature_histogram_obj_StInGRAI,
                        bar_plot_obj_unsegmented=bar_plot_obj_unsegmented,
                        feature_histogram_obj_unsegmented=feature_histogram_obj_unsegmented)
