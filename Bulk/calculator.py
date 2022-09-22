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
    esigma = edelta * kcal2J ** 2 * (1 / Na) ** 2
    cv = esigma / (kb * temp ** 2) / ncount * Na / 39.98
    # print(cv)
    cv_ave = np.average(cv)
    # print(cv_ave)
    return cv_ave


def vis_pacf(pacfs, ave):
    kB = 1.3806504e-23  # J/K
    atm2pa = 101325.0
    A2m = 1e-10
    fs2s = 1e-15
    V = 61887.25519
    dt = pacfs[0, 1, 1] - pacfs[0, 0, 1]
    shape = pacfs.shape
    trap = np.zeros(shape[0])
    for i in range(shape[0]):
        trap[i] = np.sum(pacfs[i, :, 3:]) - np.sum(pacfs[i, 0, 3:]) / 2 - np.sum(pacfs[i, -1, 3:]) / 2
    vis = trap * atm2pa ** 2 * dt * fs2s * V * A2m ** 3 / kB / 100/3

    if ave:
        vis_final = vis[-1]
    else:
        vis_final = np.average(vis)
    return vis_final
