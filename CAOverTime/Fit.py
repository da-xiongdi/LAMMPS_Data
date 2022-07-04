import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit


class Fit:
    def __init__(self, input):
        self.input = input

    @staticmethod
    def circle(x, x0, y0, r):
        z = (x[0] - x0) ** 2 + (x[1] - y0) ** 2 - r ** 2
        return z

    def circleFit(self):
        circle_fit, fitcov = curve_fit(self.circle, self.input[0:2], self.input[2], bounds=([0, -100, 0], [350, 0, np.inf]))
        return circle_fit

    @staticmethod
    def poly(x, a, b, c, d):
        y = a * x**3 + b*x**2 + c * x + d
        return y

    def polyfit(self):
        circle_fit, fitcov = curve_fit(self.poly, self.input[0], self.input[1])
        return circle_fit

    @staticmethod
    def fitshown(x, circle_fit):
        x0, y0, r = circle_fit.tolist()
        dx = x - x0
        dy2 = r ** 2 - dx ** 2

        dy2new = np.zeros(len(dy2))
        n = 0
        for i in dy2:
            if i >= 0:
                dy2new[n] = i
            else:
                dy2new[n] = 0
            n += 1
        y = y0 + np.sqrt(dy2new)
        return y


# circle_fit, fitcov = curve_fit(circle, [x, y], z)
#
# # print(fitcov)
#
# y_f = fitshown(x, circle_fit)
# y_ave = np.average(y)
# ssr = np.sum((y_f - y_ave) ** 2)
# sst = np.sum((y - y_ave) ** 2)
# # print(y_f)
# r2 = ssr / sst
# print("Mean R :", r2)

# x_ran = np.random.randint(100, 250, size=100)
# y_fit = fitshown(x_ran, circle_fit)
#
# plt.scatter(x_ran, y_fit, marker='*')
# plt.scatter(x, y_f, marker='+')
# plt.scatter(x, y)
# plt.show()
