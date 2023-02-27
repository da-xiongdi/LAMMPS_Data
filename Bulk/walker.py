import os
from ReadFiles import ReadData
import numpy as np
import calculator


# collect the output file from lammps classified by the calculated properties such as vis, diff
def file_collector(dir_path, cal, suf):
    file_paths = []
    for file in os.listdir(dir_path):
        suffix = '.' + file.split('.')[-1]
        if suffix in suf:
            file_path = os.path.join(dir_path, file)
            file_name = file.strip(suffix)
            keywords = file_name.split('-')
            file_paths.append(file_path) if cal in keywords else None
    # print(file_paths)
    return file_paths


def cal_walker(file_paths, modul, input_para):
    traj_num = len(file_paths)  # number of output files from the collector
    values = np.zeros((traj_num, 2))
    i = 0
    damp_num, tdamp = 0, 0  # damp_num, number of traj with different tdamp
    for input_file in file_paths:
        path = os.path.split(input_file)[0]
        file = os.path.split(input_file)[1]
        suffix = '.' + file.split('.')[-1]
        file = file.strip(suffix)

        keywords = file.split('-')
        data = ReadData(input_file)
        input_data, header = data.read1D() if 'Time-averaged' in data.header else data.read2D()
        values[i, 0] = keywords[-1]  # values[i, 0:2] = keywords[3:5]

        for func in dir(calculator):
            values[i, 1] = getattr(calculator, func)(input_data, input_para) if modul in func else None

        damp_num += 1 if keywords[-1] != tdamp else 0
        tdamp = keywords[-1]

        i += 1
    save_path = path + '/%s-single.txt' % modul
    np.savetxt(save_path, values[values[:, 0].argsort()])

    value_sum = np.zeros((damp_num, 3))
    value_sum[:, 2] = 1

    i, tdamp = 0, 0
    for value in values:
        if value[0] != tdamp:
            value_sum[i, 1] = value[1]
        else:
            i -= 1
            value_sum[i, 1] += value[1]
            value_sum[i, 2] += 1
        value_sum[i, 0] = value[0]
        i += 1
        tdamp = value[0]

    value_sum[:, 1] = value_sum[:, 1] / value_sum[:, 2]
    value_sum = value_sum[value_sum[:, 0].argsort()]
    save_path = path + '/%s-ave.txt' % modul
    np.savetxt(save_path, value_sum)


def file_walker(path):
    diff_path = []
    vis_path = []
    fluc_path = []
    pacf_path = []
    for file in os.listdir(path):
        suffix = '.' + file.split('.')[-1]
        if suffix == '.dat' or suffix == '.profile':
            file_path = os.path.join(path, file)
            file_name = file.strip(suffix)
            keywords = file_name.split('-')

            if keywords[0] == 'D':
                diff_path.append(file_path)
            elif keywords[0] == 'v':
                vis_path.append(file_path)
            elif keywords[0] == 'fluc':
                fluc_path.append(file_path)
            elif keywords[1] == 'SS':
                # print('yes')
                pacf_path.append(file_path)
    return [diff_path, vis_path, fluc_path, pacf_path]


def calculate_walker(input_files, equili=0):
    traj_num = len(input_files)
    values = np.zeros((traj_num, 2))  # tdamp value
    i = 0
    damp_num, tdamp = 0, 0  # damp_num, number of traj with different tdamp
    for input_file in input_files:
        path = os.path.split(input_file)[0]
        file = os.path.split(input_file)[1]
        suffix = '.' + file.split('.')[-1]
        file = file.strip(suffix)

        keywords = file.split('-')
        data = ReadData(input_file)
        if 'SS' not in keywords:
            input_data, header = data.read1D()

        values[i, 0] = keywords[-1]  # values[i, 0:2] = keywords[3:5]
        if 'D' in keywords:
            equili_data = input_data[equili:]
            values[i, 1] = calculator.diff_msd(equili_data[:, 0], equili_data[:, -1])
        elif 'v' in keywords:
            values[i, 1] = calculator.vis_gk(input_data[:, 4], ave=False)
        elif 'fluc' in keywords:
            values[i, 1] = calculator.capacity(input_data[:, 1], para=354)
        elif 'SS' in keywords:
            # print('yes')
            input_data = data.read2D()[0]
            values[i, 1] = calculator.vis_pacf(input_data, ave=True)

        damp_num += 1 if keywords[-1] != tdamp else 0
        tdamp = keywords[-1]

        i += 1
    save_path = path + '/%s-single.txt' % keywords[0]
    np.savetxt(save_path, values[values[:, 0].argsort()])

    value_sum = np.zeros((damp_num, 3))
    value_sum[:, 2] = 1

    i, tdamp = 0, 0
    for value in values:
        if value[0] != tdamp:
            value_sum[i, 1] = value[1]
        else:
            i -= 1
            value_sum[i, 1] += value[1]
            value_sum[i, 2] += 1
        value_sum[i, 0] = value[0]
        i += 1
        tdamp = value[0]

    value_sum[:, 1] = value_sum[:, 1] / value_sum[:, 2]
    value_sum = value_sum[value_sum[:, 0].argsort()]
    save_path = path + '/%s-ave.txt' % keywords[0]
    np.savetxt(save_path, value_sum)
