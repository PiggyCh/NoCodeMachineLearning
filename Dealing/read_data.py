'''
@PiggyCh
@time 2023/8/3
@description: read data from files

This block is used to read data from files, which is the first step of data processing.
current support formats:
    1. csv
    2. txt
    3. json
    4. excel
'''

import os
import pandas as pd
import numpy as np 
from enum import Enum
# from Dealing.deal_args import deal_args
type_same = [
    [int, np.int64, np.int32, np.int16,float, np.float64, np.float32, np.float16],
    [str, np.str, np.str_],
    [bool, np.bool, np.bool_],
    [complex, np.complex, np.complex64, np.complex128],
    [list, np.ndarray],
    [dict],
    [tuple],
    [set],
]
def get_is_same_type(type1, type2):
    for i in range(len(type_same)):
        if type1 in type_same[i] and type2 in type_same[i]:
            return True
    return False
        

class data_dealer:
    def __init__(self) -> None:
        self.data = None

    def read_data_from_path(self, path: str):
        # get file type
        file_type = path.split('.')[-1].lower()
        # define a dictionary to map file types to read functions
        read_functions = {
            'csv': pd.read_csv,
            'txt': pd.read_table,
            'json': pd.read_json,
            'xlsx': pd.read_excel,
        }
        # check if file type is supported
        if file_type not in read_functions:
            raise ValueError('file type not supported')
        # read data using the appropriate function
        try:
            self.data = read_functions[file_type](path)
        except Exception as e:
            raise ValueError(f'Error reading file: {e}')
        return self.data
    
    def generate_data_report(self, data: pd.DataFrame = None, report_save_path: str = '.'):
        # check if data is a pandas dataframe
        if data is None:
            data = self.data
        if not isinstance(data, pd.DataFrame):
            raise ValueError('data should be a pandas dataframe')
        # generate report using pandas_profiling
        import pandas_profiling
        report = pandas_profiling.ProfileReport(data)
        # save report
        report.to_file(report_save_path)
        return report


    def process_col(self, col_name : str, deal_type, missing_method = 'mean', outlier_method = 'mean'):
        '''
        description: process a column of data
        params:
            -col_name: str
                the name of the column to be processed
            -deal_type: str
                the type of processing to be performed
                select in 
                [
                    0. '': no processing,
                    1. enum2onehot: enum (categorical type) type to one-hot encoding,
                    2. enum2int : enum type to int encoding,
                    3. float2int_round : float type to int type (rounding),
                    4. float2int_floor : float type to int type (floor),
                    5. float2int_ceil : float type to int type (ceil),
                    6. #TODO: add more
                ]
            -missing_wash: bool
                whether to process missing values
            -missing_method: str
                the method of processing missing values
                select in ['mean','median','mode','drop']
            -outlier_deal: bool
                whether to process outliers
            -outlier_method: str
                the method of processing outliers
                select in [ mean, median, mode, drop ]
        return:
            -data: pd.DataFrame
                the processed data
        '''
        # 1. check if col_name is in data and get the column
        if col_name not in self.data.columns:
            raise ValueError(f'column {col_name} not in data')
        select_data = self.data[col_name]
        select_data = self.data_wash(select_data, missing_method)
        select_data = self.deal_outlier(select_data, outlier_method)
        # 2. data wash

    def data_wash(self, data, row, col_name, use_method):
        method_dict = {
            'mean': np.mean,
            'median': np.median,
            'mode': np.bincount,
            'drop': None,
        }
        sigma = np.std(data)
        mean = np.mean(data)
        select_col_data = data[col_name]
        if use_method == 'drop':
            # drop row
            data = data.drop(row)
        elif use_method == 'clip':
            data[col_name] = data[col_name].clip(mean - 3 * sigma, mean + 3 * sigma)
        else:
            data[col_name][row] = method_dict[use_method](select_col_data)
        return data
    
    def check_outlier(self):
        # 1. check nan
        if self.data == None:
            raise ValueError('data not loaded')
        # 2. check if data is a pandas dataframe
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError('data should be a pandas dataframe')
        # 3. check col  
        total_error = {}
        for col in self.data.columns:
            # 3.1 check nan, over 3 sigma, type diff
            nan_index = []
            total_type_diff = []
            over_3sigma = []
            sigma = np.std(self.data[col])
            mean = np.mean(self.data[col])
            range_val = [mean - 3 * sigma, mean + 3 * sigma]
            main_type = type(self.data[col][0])
            for i in range(len(self.data[col])):
                if self.data[col][i] == 'nan':
                    nan_index.append(i)
                if self.data[col][i] < range_val[0] or self.data[col][i] > range_val[1]:
                    over_3sigma.append(i)
                if not get_is_same_type(main_type, type(self.data[col][i])):
                    total_type_diff.append(i)    
            total_error[col] = {
                'nan_index': nan_index,
                'over_3sigma': over_3sigma,
                'total_type_diff': total_type_diff
            }
        return total_error
