import numpy as np
import pandas as pd
from code_of_project.helper_methods import save_obj_as_txt, save_obj_as_pkl, open_model
from pathlib import  Path
from project_settings import ROOT_PATH
# generate a random dataset which label is calculated with alternating larger and smaller weights

def generate_matrix(num_row, num_column, min_value, max_value):
    dataset = np.random.uniform(min_value, max_value, size=(num_row, num_column))
    return dataset

def sigmoid(z):
    return 1/(1 + np.exp(-z))



if __name__ == '__main__':
    dataset = generate_matrix(num_row=5000, num_column= 26, min_value=-1, max_value=1)
    weights = np.array([(-1)**i*i/26 for i in range(26)])
    weights = np.round(weights,decimals=2)
    label = sigmoid(np.matmul(dataset,weights ))
    df= pd.DataFrame(dataset, columns=['A','B','C','D','E','F','G','H','I','J','K',
                                   'L','M','N','O','P','Q','R','S','T','U','V',
                                   'W','X','Y','Z'])
    df.loc[:,'label']=label

    print(df.head())
    path = Path(f'{ROOT_PATH}/datasets/test/test_dataset')
    save_obj_as_pkl(obj=df, path=path)