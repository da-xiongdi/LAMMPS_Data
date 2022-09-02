import numpy as np


def diff_msd(time, distance):
    return (np.polyfit(time, distance, deg=1)[0] / 6) * 1e6


def vis_gk(vis_value, ave=False):
    return np.average(vis_value) if ave else vis_value[-1]


def capacity(etotal, etotal2, temp, ncount):
    kb = 1.38e-23
    Na = 6.023e23
    kcal2J = 4184
    edelta = etotal2 - etotal ** 2
    esigma = edelta*kcal2J**2*(1/Na)**2
    cv = esigma/(kb*temp**2)/ncount*Na/39.98
    # print(cv)
    cv_ave = np.average(cv)
    # print(cv_ave)
    return cv_ave
