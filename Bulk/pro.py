import numpy as np
from ReadFile import ReadIn, ReadData
import os

kB = 1.3806504e-23  # J/K
Na = 6.023e23
kcal2J = 4184
atm2pa = 101325.0
A2m = 1e-10
fs2s = 1e-15


class Calculator:
    def __init__(self, input_path):
        self.input_path = input_path
        self.para = ReadIn(input_path).cal_in

    def diff_msd(self, data):
        dimension = list(int(x) for x in self.para['dimension'].split())
        time, distance = data[:, 0], data[:, 1:4]
        dime_dis = distance.shape[1]
        valid_dis = distance * dimension
        diff = 0
        for i in range(dime_dis):
            diff += np.polyfit(time, valid_dis[:, i], deg=1)[0] / 2 * 1e6
        diff = diff / sum(dimension)
        return diff

    def vis_gk(self, data):
        ave = int(self.para['ave'])
        return np.average(data[:, -1]) if ave == 1 else data[-1, -1]

    def fluc(self, data):
        dime = data.shape[1]
        order = int((dime - 1) / 3)
        deviation = np.zeros((order - 1, 3))
        for j in np.arange(1, order):
            for i in np.arange(1, 4):
                e, e2 = data[:, i], data[:, i + 3*j]
                temp, para = float(self.para['temp']), int(self.para['ncount'])

                edelta = e2 - e ** (j+1)
                esigma = edelta * kcal2J ** (j+1) * (1 / Na) ** (j+1)
                cv = esigma / (kB * temp ** (j+1)) / para * Na / 39.98
                deviation[j-1, i-1] = np.average(cv)
        return deviation.reshape(deviation.shape[0]*deviation.shape[1])

    def vis_pacf(self, data):
        pacfs = data[1:]
        ave, V = int(self.para['ave']), float(self.para['Volume'])

        dt = pacfs[0, 1, 1] - pacfs[0, 0, 1]
        shape = pacfs.shape
        trap = np.zeros(shape[0])

        for i in range(shape[0]):
            trap[i] = np.sum(pacfs[i, :, 3:]) - np.sum(pacfs[i, 0, 3:]) / 2 - np.sum(pacfs[i, -1, 3:]) / 2
        vis = trap * atm2pa ** 2 * dt * fs2s * V * A2m ** 3 / kB / 100 / 3
        vis_final = vis[-1] if ave == 0 else np.average(vis)

        return vis_final


class Walker(Calculator):
    def __init__(self, input_path):
        super().__init__(input_path)
        self.modul = self.para['module']

    @property
    def file_collector(self):
        dir_path = self.para['dir_path']
        suf = self.para['suffix'].split()

        file_paths = []
        for file in os.listdir(dir_path):
            suffix = '.' + file.split('.')[-1]
            if suffix in suf:
                file_path = os.path.join(dir_path, file)
                file_name = file.rstrip(suffix)
                keywords = file_name.split('-')

                if self.modul in keywords:
                    try:
                        file_paths.append(file_path) if self.para['sl'] in keywords else None
                    except KeyError:
                        file_paths.append(file_path)
        return file_paths

    def cal_walker(self):
        file_paths = self.file_collector

        traj_num = len(file_paths)  # number of output files from the collector
        values = np.zeros((traj_num, 7))
        i = 0
        damp_num, tdamp = 0, 0  # damp_num, number of traj with different tdamp
        for input_file in file_paths:
            path, file = os.path.split(input_file)
            suffix = '.' + file.split('.')[-1]
            file = file.rstrip(suffix)

            keywords = file.split('-')
            data = ReadData(input_file)
            input_data, header = data.read1D() if 'Time-averaged' in data.header else data.read2D()

            for func in Calculator.__dict__.keys():
                if self.modul in func:
                    values[i, 1:] = getattr(self, func)(input_data)
                else:
                    pass
            values[i, 0] = keywords[-1]
            damp_num += 1 if keywords[-1] != tdamp else 0
            tdamp = keywords[-1]

            i += 1
        save_path = path + '/%s-%s-single.txt' % (self.modul, keywords[-2])
        np.savetxt(save_path, values[values[:, 0].argsort()])

        value_sum = np.zeros((damp_num, 3))
        value_sum[:, 2] = 1

        i, tdamp = 0, 0
        for value in values:
            if value[0] != tdamp:
                value_sum[i, 1] = value[1]
            else:
                i -= 1
                value_sum[i, 1] += value[1]
                value_sum[i, 2] += 1
            value_sum[i, 0] = value[0]
            i += 1
            tdamp = value[0]

        value_sum[:, 1] = value_sum[:, 1] / value_sum[:, 2]
        value_sum = value_sum[value_sum[:, 0].argsort()]
        save_path = path + '/%s-%s-ave.txt' % (self.modul, keywords[-2])
        np.savetxt(save_path, value_sum)
