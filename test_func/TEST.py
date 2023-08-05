import numpy as np 
def deal_outlier(data, use_method):
    '''
    '''
    method_dict = {
        'mean': np.mean,
        'median': np.median,
        'mode': np.bincount,
        'drop': None,
    }
    if use_method == 'drop':
        data = data.dropna()
    else:
        sigma = np.std(data)
        mean = np.mean(data)
        outlier_index = np.where(np.abs(data - mean) > 3 * sigma)
        data[outlier_index] = method_dict[use_method](data)
    return data

total_data = np.random.uniform(0, 100, 1000)
#add outlier
random_index = np.random.randint(0, 100, 2)
total_data[random_index] += 1000
print(random_index)
print(total_data[random_index])
print(total_data[random_index].shape)
print(total_data.shape)
modified_data = deal_outlier(total_data, 'mean')
print(modified_data[random_index])
print(modified_data[random_index].shape)
print(modified_data.shape)