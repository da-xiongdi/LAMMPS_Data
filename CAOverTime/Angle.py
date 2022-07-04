import numpy as np


class CLAngle:
    def __init__(self, fitpara, y):
        self.fitpara = fitpara
        self.y = y

    @property
    def circleAngle(self):
        # print(self.x0, self.y0, self.r)
        x = self.fitpara[0] - (self.fitpara[2] ** 2 - (self.y - self.fitpara[1]) ** 2) ** 0.5
        dr = np.array([x - self.fitpara[0], self.y - self.fitpara[1]])
        theta = np.arccos(abs(dr[1]) / np.sum(dr ** 2) ** 0.5) / np.pi * 180
        if dr[1] >= 0:
            theta = theta
        else:
            theta = 180 - theta
        return theta

    @property
    def polyAngle(self):
        # print(self.x0, self.y0, self.r)
        fitpara = self.fitpara
        fitpara[len(fitpara) - 1] = fitpara[len(fitpara) - 1] - self.y
        x = np.roots(fitpara)
        xcl = 300
        for i in x:
            if 20 < i < 300:
                if i < xcl:
                    xcl = i
        tanTheta = 3 * fitpara[0] * xcl ** 2 + 2 * fitpara[1] * xcl + fitpara[2]
        theta = np.arctan(tanTheta) / np.pi * 180
        return theta
