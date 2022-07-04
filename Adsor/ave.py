# coding = utf-8
import numpy as np

import ReadFile
import os

scale4f = 6.947e-11

file_path = "D:/document/00Study/01接触角摩擦力/计算/液滴/stage4/test/adsor/3/NH/ar.y.100.0.1890.profile"

path = os.path.split(file_path)[0]
file = os.path.split(file_path)[1]
strength = file.split('.')[3] + '.' + file.split('.')[4]
index = path.split('/')[-1]
if 'spring' in index:
    strength2 = file.split('.')[5]
    strength = strength + '.' + strength2
else:
    pass

save_path = path + '/chunktemp.0.31.%s.%s.txt' % (index, strength)

chunkFrequency, chunkNum, rowNum = 420, 140, 3
fileData = ReadFile.ReadData(file_path, chunkFrequency)

header4chunk = 3  # row number before each chunk# TimeStep Number-of-rows
Data = fileData.read2D(header4chunk)[0]
# Chunk Coord1 Coord2 Ncount temp density/number density/mass c2_03[1] c2_03[2] c2_03[3] c2_03[4] c2_03[5] c2_03[6]
# c_06 fx fy fz v_fa vx vy vz v_va
validNum = 10
validData = np.zeros((validNum, chunkNum, rowNum))  # 11 for early

target = 0  # 0 for intensive while 1 for extensive
index = [2, 3]  # [6]   # [7, 8, 9, 10, 11, 12]  # [6]  #    [18, 19, 20]  #  [3, 4, 5]  # [18, 19, 20]
indexCoord, indexNum = 1, 2

force, press = 0, 0  # whether calculate the force
vbin = 4 * 5 * 55.4372  # 21000
if force == 1:
    scale = scale4f
elif press == 1:
    scale = -1 / vbin
else:
    scale = 1
n = 0

# for t in range(chunkFrequency - validNum, chunkFrequency):
# 66, 77
for t in range(62, 72):

    properties = Data[t, :, index] * scale + (Data[t, :, indexNum] - 1) * Data[t, :, index] * target * scale
    if press == 1:
        pressure = np.average(properties[0:3], axis=0)
        validData[n, :, 1:(rowNum - 1)] = properties.T
        validData[n, :, rowNum - 1] = pressure.T
    else:
        validData[n, :, 1:] = properties.T
    validData[n, :, 0] = Data[t, :, indexCoord]
    n += 1

aveData = np.average(validData, axis=0)

# saveData = aveData[(aveData[:, 0] < 330) & (aveData[:, 0] > 20)]
np.savetxt(save_path, aveData)
