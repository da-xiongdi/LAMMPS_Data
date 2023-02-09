import numpy as np


class ReadData:
    def __init__(self, file):
        self.file = file
        with open(self.file, 'r') as f:
            self.fileData = f.readlines()
        self.header = self.fileData[0].strip('#').strip(' ').strip('\n').split(' ')

    def read2D(self):
        fileHeader = self.fileData[0:3]
        DataHeader = fileHeader[2].strip('#').strip(' ').strip('\n').split(' ')
        info4chunk = len(DataHeader)

        D2Data = self.fileData[3:]

        NumRow = int(D2Data[0].strip('\n').split(' ')[1])
        step = int(len(D2Data) / (1 + NumRow))
        validData = np.zeros((step, NumRow, info4chunk))

        n = 0
        m = 0
        for line in D2Data:
            num = [float(i) for i in line.strip(' ').strip('\n').split(' ')]
            if len(num) == info4chunk:
                # print(line)
                validData[n - 1, m] = num
                m += 1
            else:
                m = 0
                n += 1
        # print('data has been loaded!')
        return [validData, DataHeader]

    def read1D(self):
        fileHeader = self.fileData[0:2]
        DataHeader = fileHeader[1].strip('#').strip(' ').strip('\n').split(' ')
        D1Data = self.fileData[2:]
        validData = np.zeros((len(D1Data), len(DataHeader)))

        n = 0
        for line in D1Data:
            validData[n] = [float(i) for i in line.strip(' ').strip('\n').split(' ')]
            n += 1
        # print('data has been loaded!')
        return [validData, DataHeader]


class Readtri:

    @staticmethod
    def feikong(x):
        if x != ['']:
            return x

    def __init__(self, file):
        self.file = file

    def readlammpstrj(self):
        with open(self.file, 'r') as f:
            fileData = f.readlines()
        fileData = list(filter(self.feikong, fileData))
        ncount = int(fileData[3].strip(' ').strip('\n'))
        box, i = np.zeros((3, 2)), 0
        for d in [5, 6, 7]:
            box[i] = np.array(fileData[d].strip('/n').split(' ')).astype('float')
            i += 1
        header = fileData[8].strip('ITEM: ATOMS').strip(' ').strip('\n').split(' ')

        nstep = int(len(fileData) / (ncount + 9))
        nheader = len(header)

        validData = np.zeros((nstep, ncount, nheader))

        i, j = -1, 0
        for line in fileData:
            if line == 'ITEM: TIMESTEP\n':
                i += 1
                j = 1
            else:
                validData[i, j - 9] = np.array(line.strip('\n').split(' ')).astype('float') if j > 8 else 0
                j += 1

        print('data has been loaded!')
        return [box, header, validData]


class ReadIn:
    def __init__(self, file):
        self.file = file
        with open(self.file, 'r', encoding='UTF-8') as f:
            self.fileData = f.readlines()

    @property
    def cal_in(self):
        para = {}
        for line in self.fileData:
            [key, value] = line.strip('\n').split(' ', 1)
            para[key] = value
        return para
