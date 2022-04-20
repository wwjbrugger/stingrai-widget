import code_of_project.helper_methods as helper
import copy
from pathlib import Path
from code_of_project.helper_methods import check_if_at_least_one_transition_is_complete
from project_settings import ROOT_PATH
from code_of_project.get_index_in_interval.construct_ig_unsegmented_paths_args import get_arguments



def set_long_path_together(args):
    for start_point in args.start_point_list:
        for end_point in args.end_point_list:
            start_point_B, end_point_B, _, _ = helper.get_interval_border_from_string(start_point)
            _, _, start_point_D, end_point_D = helper.get_interval_border_from_string(end_point)
            if start_point_B <= start_point_D:
                paths = get_paths(start_point = start_point,
                                  end_point=end_point,
                                  start_point_B=start_point_B,
                                  end_point_B=end_point_B,
                                  start_point_D=start_point_D,
                                  end_point_D=end_point_D)

                new_dic = create_long_path_dic(args, paths)
                if check_if_at_least_one_transition_is_complete(dic = new_dic, file_name=paths['path_to_save'].stem):
                    helper.save_obj_as_pkl(obj=new_dic, path=paths['path_to_save'])

def get_paths(start_point, end_point, start_point_B, end_point_B, start_point_D, end_point_D):
    paths = {
        'path_for_baseline': Path(f'{args.path_to_model}/{args.time_string_of_model}/'
                             f'dic_with_index_of_interesting_data/{args.time_string_dic_with_index_of_interesting_data}/'
                             f'{args.path_to_ig_dic_StInGRAI}/{start_point}'),
        'path_for_data_to_explain': Path(f'{args.path_to_model}/{args.time_string_of_model}/'
                                    f'dic_with_index_of_interesting_data/{args.time_string_dic_with_index_of_interesting_data}/'
                                    f'{args.path_to_ig_dic_StInGRAI}/{end_point}'),
        'path_to_save': Path(f'{args.path_to_model}/{args.time_string_of_model}/'
                        f'dic_with_index_of_interesting_data/{args.time_string_dic_with_index_of_interesting_data}/'
                        f'{args.path_to_ig_dic_unsegmented}/'
                        f'{start_point_B}-{end_point_B}->{start_point_D}-{end_point_D}.pkl')
    }
    return paths


def create_long_path_dic(args, paths):
    baseline_dic = helper.load_obj(paths['path_for_baseline'])
    data_to_explain_dic = helper.load_obj(paths['path_for_data_to_explain'])
    new_dic = copy.deepcopy(baseline_dic)
    for transition in args.transitions_to_use:
        new_dic[transition]['data_to_explain'] = data_to_explain_dic[transition]['data_to_explain']
    return new_dic


if __name__ == '__main__':
    args=get_arguments()
    set_long_path_together(args)
