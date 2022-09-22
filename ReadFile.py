import numpy as np


class ReadChunk:
    def __init__(self, file, step):
        self.file = file
        self.step = step

    def read2D(self, info4chunk=3):
        with open(self.file, 'r') as f:
            fileData = f.readlines()
        fileHeader = fileData[0:3]
        DataHeader = fileHeader[2].strip('#').strip(' ').strip('\n').split(' ')
        D2Data = fileData[3:]

        NumRow = int(D2Data[0].strip('\n').split(' ')[1])
        validData = np.zeros((self.step, NumRow, len(DataHeader)))

        n = 0
        m = 0
        for line in D2Data:
            num = [float(i) for i in line.strip(' ').strip('\n').split(' ')]
            if len(num) != info4chunk:
                validData[n - 1, m] = num
                m += 1
            else:
                m = 0
                n += 1
        print('data has been loaded!')
        return [validData, DataHeader]

    def read3DChunk(self):
        with open(self.file, 'r') as f:
            fileData = f.readlines()
        fileHeader = fileData[0:3]
        DataHeader = fileHeader[2].strip('#').strip(' ').strip('\n').split(' ')
        chunkData = fileData[3:]

        # step = 1
        # for line in chunkData:
        #     num = [float(i) for i in line.strip(' ').strip('\n').split(' ')]
        #     if num[2] % self.ntotal == 0:
        #         step += 1
        NumChunk = int(chunkData[0].strip('\n').split(' ')[1])
        validData = np.zeros((self.step, NumChunk, len(DataHeader)))

        n = 0
        m = 0
        for line in chunkData:
            num = [float(i) for i in line.strip(' ').strip('\n').split(' ')]
            if num[1] != NumChunk:
                validData[n - 1, m] = num
                m += 1
            else:
                m = 0
                n += 1
        print('data has been loaded!')
        return [validData, DataHeader]

    def dataByChunk(self):
        validData = self.read3DChunk()[0]
        DataHeader = self.read3DChunk()[1]
        dataByPt = np.zeros((validData.shape[1], validData.shape[0], validData.shape[2] - 3))
        m = 0
        for i in validData:
            n = 0
            for j in i:
                dataByPt[n, m] = j[3:]
                n += 1
            m += 1
        return dataByPt

    def to2D(self, dimension):
        data = self.read3DChunk()
        row = len(data[1])
        validData = data[0]

        ylo, yhi = np.min(validData[0, :, 2]), np.max(validData[0, :, 2])
        xlo, xhi = np.min(validData[0, :, 1]), np.max(validData[0, :, 1])

        ycount = len(validData[0, :, 1][np.where(validData[0, :, 1] == xlo)])
        xcount = len(validData[0, :, 2][np.where(validData[0, :, 2] == ylo)])
        xstep, ystep = (xhi - xlo) / (xcount - 1), (yhi - ylo) / (ycount - 1)
        pInfo = [[xlo, xhi, xcount, xstep], [ylo, yhi, ycount, ystep]]
        dInfo = pInfo[dimension]
        print(dInfo)
        print(pInfo[dimension - 1])

        temp = np.zeros((self.step, ycount, row - 2))

        t = 0
        for i in validData:
            for j in i:
                for dvalue in np.arange(dInfo[0], dInfo[1] + dInfo[3], dInfo[3]):
                    index = int((dvalue - dInfo[0]) / dInfo[3])
                    if j[dimension + 1] == dvalue:
                        temp[t, index] += np.hstack((j[dimension + 1], j[3:]))
            t += 1
        valid2D = temp / xcount
        return valid2D


class ReadData:
    def __init__(self, file, step=1000):
        self.file = file
        self.step = step

    def read2D(self):
        with open(self.file, 'r') as f:
            fileData = f.readlines()
        fileHeader = fileData[0:3]
        # timeHeader = fileHeader[1].strip('#').strip(' ').strip('\n').split(' ')
        # info4chunk = len(timeHeader)
        DataHeader = fileHeader[2].strip('#').strip(' ').strip('\n').split(' ')
        info4chunk = len(DataHeader)

        D2Data = fileData[3:]

        NumRow = int(D2Data[0].strip('\n').split(' ')[1])
        step = int(len(D2Data) / (3 + NumRow)) + 1
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
        with open(self.file, 'r') as f:
            fileData = f.readlines()
        fileHeader = fileData[0:2]
        DataHeader = fileHeader[1].strip('#').strip(' ').strip('\n').split(' ')
        D1Data = fileData[2:]
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
