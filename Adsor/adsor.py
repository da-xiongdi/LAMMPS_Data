import os.path
import sys

import numpy as np
import ReadFile

Na = 6.022e23  # /mol
kB = 1.38e-23  # J/K


def surface(input_file, layers, frequency, equli=0):
    path = os.path.split(input_file)[0]
    file = os.path.split(input_file)[1]
    suffix = '.' + file.split('.')[-1]
    file = file.strip(suffix)

    order = file.split('-')[2] if len(file.split('-')) == 5 else 1

    if '-' in file.split('/')[-1]:
        strength = file.split('-')[-1]
    else:
        strength = file.split('.')[3] + '.' + file.split('.')[4]
    index = path.split('/')[-1]
    if 'spring' in index or 'spring-void' in index:
        strength1 = file.split('-')[4]
        strength2 = file.split('-')[3]
        strength = strength1 + '-' + strength2
    else:
        pass

    data = ReadFile.ReadChunk(input_file, frequency)
    input_data, header = data.read2D()
    n_index = header.index('Ncount') if 'Ncount' in header else 0
    temp_index = header.index('temp') if 'temp' in header else 0
    ke_index = header.index('c_kear') if 'c_kear' in header else 0
    if n_index * temp_index == 0:
        print('wrong format for temp and ncount!')
        sys.exit(0)
    valid_data = input_data[:, layers[0]:(layers[1] + 1), :]
    ylo, yhi = input_data[0, layers[0], 1], input_data[0, layers[1], 1]
    thick = (yhi - ylo) / (layers[1] - layers[0])

    save_n_path = path + '/nad.%d-%d.%s.%s.%s.txt' % (ylo - thick / 2, yhi + thick / 2, index, order, strength)  # 15-17
    save_T_path = path + '/Tad.%d-%d.%s.%s.%s.txt' % (ylo - thick / 2, yhi + thick / 2, index, order, strength)

    adsorbn = np.empty(frequency - equli)
    temp = np.empty(frequency - equli)
    for i in range(equli, frequency, 1):
        j = i - equli
        adsorbn[j] = np.sum(valid_data[i, :, n_index])  # 0:6
        if adsorbn[j] == 0:
            temp[j] = 0
        elif adsorbn[j] != 0 and ke_index == 0:
            temp[j] = np.dot(valid_data[i, :, n_index], valid_data[i, :, temp_index]) / \
                      adsorbn[j]
        elif adsorbn[j] != 0 and ke_index != 0:
            temp[j] = np.dot(valid_data[i, :, n_index], valid_data[i, :, ke_index]) / \
                      Na * 4.184 * 1000 / kB / adsorbn[j] / 1.5

    np.savetxt(save_n_path, adsorbn)
    np.savetxt(save_T_path, temp)


def single(input_file, cutoff, baseline):
    cri_line = cutoff + baseline
    path, file = os.path.split(input_file)
    suffix = '.' + file.split('.')[-1]
    file = file.strip(suffix)

    order = file.split('.')[4] + '.' + file.split('.')[5]

    if '-' in file.split('/')[-1]:
        strength = file.split('-')[4]
    else:
        strength = file.split('.')[2] + '.' + file.split('.')[3]
    index = path.split('/')[-1]
    if 'spring' in index:
        strength2 = file.split('.')[5]
        strength = strength + '.' + strength2
    else:
        pass

    data = ReadFile.ReadData(input_file)
    input_data, header = data.read1D()

    a = 1
    cri_t = []
    for line in input_data:
        if a * (line[1] - cri_line) < 0:
            cri_t.append(int(line[0]))
            a = -1 * a
    cri_info = input_data[cri_t, :]
    collisions = int(len(cri_info) / 2)
    row = [0, 5, 6, 7, 8, 9]
    d_info = np.empty((collisions, 6))
    arrest_time = 0
    for i in range(collisions):
        d_info[i] = cri_info[i + 1, row] - cri_info[i, row]
        arrest_time = cri_t[i + 1] - cri_t[i] + arrest_time
    arrest_time = arrest_time if len(cri_info) % 2 == 0 else arrest_time + input_data[-1, 0] - cri_t[-1]

    save_cri_path = path + '/critical.%s.%s.%s.txt' % (index, order, strength)
    save_d_path = path + '/diff.%s.%s.%s.txt' % (index, order, strength)
    np.savetxt(save_cri_path, cri_info)
    np.savetxt(save_d_path, d_info)
    return arrest_time
