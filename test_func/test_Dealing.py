import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Dealing.read_data import data_dealer

def test_gene_report():
    import pandas as pd
    save_fake_data_path = 'data_buffer/train.csv'
    save_path = 'test_func/test_report.html'
    data_dealer().generate_data_report(data_dealer().read_data_from_path(save_fake_data_path), save_path)


if __name__ == '__main__':
    test_gene_report()
