# coding = utf-8
import numpy as np

import ReadFiles
import os

scale4f = 6.947e-11


def ave_time_space(input_file, tin, tfi, index):
    path = os.path.split(input_file)[0]
    file = os.path.split(input_file)[1]
    suffix = '.' + file.split('.')[-1]
    file = file.strip(suffix)

    strength = file.split('-')[3]
    strategy = path.split('/')[-1]

    fileData = ReadFiles.ReadData(input_file)

    header4chunk = 3  # row number before each chunk# TimeStep Number-of-rows
    temp = fileData.read2D()
    header4Data, Data = temp[1], temp[0]
    chunkNum, rowNum = Data[0].shape[0], 5
    for i in range(len(header4Data)):
        if '/' in header4Data[i]:
            header4Data[i] = header4Data[i].replace('/', '-')
            # print(header4Data[i])
        else:
            pass
    # print(header4Data)
    save_path = path + '/%s.%s.%s.%s.%s.txt' % (header4Data[index[0]], strategy, strength, tin/1e6, tfi/1e6)

    validNum = int((tfi-tin)/5000) + 1
    validData = np.zeros((validNum, chunkNum, rowNum))  # 11 for early

    target = 1  # 0 for intensive while 1 for extensive
    indexCoord = 0 if 'square' in file.split('-') else 1
    indexNum = 3

    force, press = 0, 1  # whether calculate the force
    vbin = 4 * 5 * 55.4372  # 21000
    if force == 1:
        scale = scale4f
    elif press == 1:
        scale = -1 / vbin
    else:
        scale = 1
    n = 0

    for t in range(int(tin/5000)-1, int(tfi/5000)):

        properties = Data[t, :, index] * scale + (Data[t, :, indexNum] - 1) * Data[t, :, index] * target * scale
        if press == 1:
            pressure = np.average(properties[0:3], axis=0)
            validData[n, :, 1:(rowNum - 1)] = properties.T
            validData[n, :, rowNum - 1] = pressure.T
        else:
            # print(validData[n, :, 1:].shape)
            validData[n, :, 1:] = properties.T
        validData[n, :, 0] = Data[t, :, indexCoord]
        n += 1

    aveData = np.average(validData, axis=0)
    np.savetxt(save_path, aveData)
