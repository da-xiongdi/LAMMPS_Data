import os
from ReadFile import ReadData
import numpy as np
import calculator


def file_walker(path):
    diff_path = []
    vis_path = []
    fluc_path = []
    for file in os.listdir(path):
        suffix = '.' + file.split('.')[-1]
        if suffix == '.dat':
            file_path = os.path.join(path, file)
            file_name = file.strip(suffix)
            keywords = file_name.split('-')

            if keywords[0] == 'D':
                diff_path.append(file_path)
            elif keywords[0] == 'v':
                vis_path.append(file_path)
            elif keywords[0] == 'fluc':
                fluc_path.append(file_path)
    return [diff_path, vis_path, fluc_path]


def calculate_walker(input_files, equili=0):
    traj_num = len(input_files)
    values = np.zeros((traj_num, 3))
    i = 0
    damp_num, tdamp = 0, 0
    for input_file in input_files:
        path = os.path.split(input_file)[0]
        file = os.path.split(input_file)[1]
        suffix = '.' + file.split('.')[-1]
        file = file.strip(suffix)

        keywords = file.split('-')
        data = ReadData(input_file)
        input_data, header = data.read1D()

        values[i, 0:2] = keywords[3:5]
        if 'D' in keywords:
            equili_data = input_data[equili:]
            values[i, 2] = calculator.diff_msd(equili_data[:, 0], equili_data[:, 4])
            # print(values[i, 2], input_file)
        elif 'v' in keywords:
            values[i, 2] = calculator.vis_gk(input_data[:, 4], ave=False)
            # print(values[i, 2], input_file)
            # if values[i, 2] < 0:
            #     print(input_file)
        elif 'fluc' in keywords:
            values[i, 2] = calculator.capacity(input_data[:, 1], input_data[:, 4], temp=100, ncount=354)
            # print(values[i, 2], input_file)

        damp_num += 1 if keywords[3] != tdamp else 0
        tdamp = keywords[3]

        i += 1
    value_sum = np.zeros((damp_num, 3))
    value_sum[:, 2] = 1

    i, tdamp = 0, 0
    for value in values:
        if value[0] != tdamp:
            value_sum[i, 1] = value[2]
        else:
            i -= 1
            value_sum[i, 1] += value[2]
            value_sum[i, 2] += 1
        value_sum[i, 0] = value[0]
        i += 1
        tdamp = value[0]

    value_sum[:, 1] = value_sum[:, 1] / value_sum[:, 2]
    value_sum = value_sum[value_sum[:, 0].argsort()]
    save_path = path + '/%s.txt' % keywords[0]
    np.savetxt(save_path, value_sum)
