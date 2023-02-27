import os.path

import numpy as np

import ReadFiles

file_path = "D:/document/00Study/01接触角摩擦力/计算/液滴/stage4/test/adsor/3/spring3NH/ar.y.100.0.1890.480.profile"
# '../drop.py/TW/stage3/lj/ar.square.100.0.2520.profile'
path = os.path.split(file_path)[0]
file = os.path.split(file_path)[1]
strength = file.split('.')[3] + '.' + file.split('.')[4]
index = path.split('/')[-1]
if 'spring' in index:
    strength2 = file.split('.')[5]
    strength = strength + '.' + strength2
else:
    pass
save_uni_path = path + '/uniform.%s.%s.txt' % (index, strength)

step = 420  # 983#2020  # 1620

data = ReadFiles.ReadChunk(file_path, step)
validdata = data.read2D()[0]
adsorbn = np.empty(step)
u = np.empty(step)

for i in range(step):
    temp_nozero = validdata[i, validdata[i, :, 3].nonzero(), 3]
    temp_ave = np.average(temp_nozero)
    u[i] = 1-np.sum(np.absolute(temp_ave-temp_nozero)/temp_ave)/(2*140)

np.savetxt(save_uni_path, u)
