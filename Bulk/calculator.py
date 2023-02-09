import numpy as np

kB = 1.3806504e-23  # J/K
Na = 6.023e23
kcal2J = 4184
atm2pa = 101325.0
A2m = 1e-10
fs2s = 1e-15


def diff_msd(data, para):
    dimension = list(int(x) for x in para['dimension'].split())
    time, distance = data[:, 0], data[:, 1:]
    dime_dis = distance.shape[1]
    valid_dis = distance * dimension
    diff = 0
    for i in range(dime_dis):
        diff += np.polyfit(time, valid_dis[:, i], deg=1)[0] / 2 * 1e6
    diff = diff / sum(dimension)
    return diff


def vis_gk(data, para):
    ave = int(para['ave'])
    return np.average(data[:, -1]) if ave == 1 else data[-1, -1]


def fluc(data, para):
    e, e2 = data[:, 1], data[:, 2]
    temp, ncount = float(para['temp']), int(para['ncount'])

    edelta = e2 - e ** 2
    esigma = edelta * kcal2J ** 2 * (1 / Na) ** 2
    cv = esigma / (kB * temp ** 2) / ncount * Na / 39.98
    cv_ave = np.average(cv)
    return cv_ave


def vis_pacf(data, para):
    pacfs = data[1:]
    ave, V = int(para['ave']), float(para['Volume'])

    dt = pacfs[0, 1, 1] - pacfs[0, 0, 1]
    shape = pacfs.shape
    trap = np.zeros(shape[0])

    for i in range(shape[0]):
        trap[i] = np.sum(pacfs[i, :, 3:]) - np.sum(pacfs[i, 0, 3:]) / 2 - np.sum(pacfs[i, -1, 3:]) / 2
    vis = trap * atm2pa ** 2 * dt * fs2s * V * A2m ** 3 / kB / 100 / 3
    vis_final = vis[-1] if ave == 0 else np.average(vis)

    return vis_final


def test():
    print('test')
