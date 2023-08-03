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


    def process_col(self, col_name : str , deal_type = '', missing_wash = True, missing_method = 'mean', outlier_deal = True, outlier_method = 'mean'):
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
                select in
                [
                    1. 'mean': fill with mean,
                    2. 'median': fill with median,
                    3. 'mode': fill with mode,
                    4. 'drop': drop the row,
                    5. #TODO: add more
                ]
            -outlier_deal: bool
                whether to process outliers
            -outlier_method: str
                the method of processing outliers
                select in
                [
                    1. 'mean': fill with mean,
                    2. 'median': fill with median,
                    3. 'mode': fill with mode,
                    4. 'drop': drop the row,
                    5. #TODO: add more
                ]
        return:
            -data: pd.DataFrame
                the processed data
        '''
        pass
