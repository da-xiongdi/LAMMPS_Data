# coding = utf-8
import numpy as np

import ReadFile

inputPath = '../chunk_data/drop/testMop/ar.square.100.0.126.profile'
outputPath = '../chunk_data/drop/testMop/stress1.txt'

chunkFrequency = 506
Data = ReadFile.ReadChunk(inputPath, chunkFrequency)

Data2D = Data.to2D(1)
np.savetxt(outputPath, Data2D[0])
# validData = np.zeros((100, 791, 4))
#
# n = 0
# for t in range(406, chunkFrequency):
#     validData[n] = Data[t, :, 1:]
#     n += 1
# # print(validData.shape)
#
# aveData = np.average(validData, axis=0)
# np.savetxt(outputPath, aveData)