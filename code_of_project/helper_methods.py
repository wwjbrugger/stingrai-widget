# Collection of helpful methods
import json
from pathlib import Path
import pickle
import keras as k
import pandas as pd
import torch as torch
import numpy as np
import tensorflow as tf
import logging
import argparse
import re
from importlib import import_module
from project_settings import ROOT_PATH
import ast



def save_obj_as_pkl(obj, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    pickle.dump(obj, open(path.with_suffix('.pkl'),'wb'))


def save_obj_as_txt(obj,path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path.with_suffix('.txt'), "w") as f:
        f.write(json.dumps(obj, indent=4, sort_keys=True))


def load_obj(path):
    with open(path, 'rb') as f:
        obj = pickle.load(f)
    return obj


def open_model(path, arguments):
    if arguments.framework == 'tensorflow':
        model = k.models.load_model(path / 'trained_model/best_model')
        if arguments.print_model_summary:
            model.summary()
    elif arguments.framework == 'pytorch':
        folder = arguments.import_statment_to_load_net
        module = import_module(name=folder)
        args_load_model = ast.literal_eval(arguments.arguments_to_load_model)
        model = module.NeuralNet(**args_load_model)
        model.load_state_dict(torch.load(path / 'trained_model_state_dic.pkl'))
        model.eval()
    else:
        raise ValueError(f'The framework {arguments.framework} is not implemented')
    return model





def set_logger_properties(arguments):
    # assuming loglevel is bound to the string value obtained from the
    # command line argument. Convert to upper case to allow the user to
    # specify --log=DEBUG or --log=debug
    loglevel = arguments.logging_level
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level)

def str2bool(v):
    '''
    Translate command line input into boolean value
    :param v:
    :return:
    '''
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def get_interval_border_from_string(folder_name):

    start_point_B, end_point_B, start_point_D, end_point_D = find_all_floats(folder_name)
    #re.split('intr_region_dic_|->|-|.pkl', folder_name)
    return float(start_point_B), float(end_point_B), float(start_point_D), float(end_point_D)


def find_all_floats(folder_name):
    # example of folder name  '0.93-0.94->0.94-0.95.pkl'
    # meaning regular expresion
    # * zero or more
    # + one or mor
    # | or
    # ?: zero or one
    # \. match with .
    # \d  any one digit
    return re.findall(r" *(?:\d+(?:\.\d*)?|\.\d+)", folder_name)




def check_if_at_least_one_transition_is_complete(dic, file_name):
    # e.g. transition signal->signal
    transitions_are_complete = []
    for transition in dic.keys():
        boolean=check_if_both_regions_in_transition_are_filled(dic, file_name, transition)
        transitions_are_complete.append(boolean)
    if not all(transitions_are_complete):
        logging.warning('-' * 1)
    return any(transitions_are_complete)


def check_if_both_regions_in_transition_are_filled(dic, file_name, transition):
    # e.g.
    for region in dic[transition].keys():
        interval_name = f'{transition} : {region}'
        interval = dic[transition][region]
        list_populated_bool = check_if_interval_is_populated(interval, interval_name=interval_name,
                                                                    key=file_name)
        if not list_populated_bool:
            return False
    return True

def check_if_interval_is_populated (interval, interval_name, key):
    if len(interval) == 0:
            logging.warning(f'Interval {key} {interval_name} is empty')
            return False
    return True


def check_if_list_contain_values(list):
    list[0]

def cast_to_pandas(arrays_list, features):
    pd_objects=[]
    for array in arrays_list:
        if array.ndim == 1:
            pd_object = pd.Series(array, index=features)
        else:
            pd_object = pd.DataFrame(array, columns=features)
        pd_objects.append(pd_object)
    return pd_objects

