import numpy as np


class Cl:
    def __init__(self, ChunkData, rho, ylo):
        self.ChunkData = ChunkData
        self.rho = rho
        self.ylo = ylo

    def contour(self):
        dropCoord = np.zeros(self.ChunkData.shape[0]).tolist()
        n = 0
        for i in self.ChunkData:
            m = 0
            for j in i:
                if j[2] >= self.ylo and self.rho * 0.9 <= j[6] <= self.rho * 1.1:
                    if m == 0:
                        dropCoord[n] = [[float(j[1]), float(j[2])]] # [int(j[0])] # [float(j[1]), float(j[2])]
                    else:
                        dropCoord[n].append([float(j[1]), float(j[2])])
                        # dropCoord[n].append(float(j[2]))
                    m += 1
            n += 1
        return dropCoord

    def drop(self):
        ClCoord = np.zeros((self.ChunkData.shape[0], 2))
        n = 0
        for i in self.ChunkData:
            xmin, xmax = 1000, -100
            ymax = 0
            for j in i:
                # print(i)
                if j[2] == self.ylo and j[6] >= self.rho:  # ylo = 20
                    xmin = j[1] if xmin >= j[1] else xmin
                    xmax = j[1] if xmax <= j[1] else xmax

                if j[6] >= self.rho:
                    ymax = j[2] if ymax <= j[2] else ymax
            r = xmax - xmin if xmax >= xmin else 0
            ClCoord[n] = [r, ymax]
            n += 1
        return ClCoord

    def meniscus(self):
        ClCoord = np.zeros((self.ChunkData.shape[0], 3))
        n = 0
        for i in self.ChunkData:
            xup, xdown, xmid = 0, 0, 0
            for j in i:
                if j[2] == 20 and j[6] >= self.rho:
                    xup = j[1] if xup <= j[1] else xup
                elif j[2] == 88 and j[6] >= self.rho:
                    xdown = j[1] if xdown <= j[1] else xdown
                elif 52 < j[2] <= 56 and j[6] >= self.rho:
                    xmid = j[1] if xmid <= j[1] else xmid
            # r = xdown - xup if xdown >= xup else 0
            ClCoord[n] = [xup, xdown, xmid]
            n += 1
        return ClCoord
