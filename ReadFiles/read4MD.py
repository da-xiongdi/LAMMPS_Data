import time

import numpy as np
import json


def count_step(path):
    """
    count the number of step in the dump file
    :param path: dump_file
    :return: number of step
    """
    with open(path, 'r') as file:
        buff_size = 1024 * 100
        buff = file.read(buff_size)
        count = 0
        while len(buff) > 0:
            count += buff.count('ITEM: TIMESTEP')
            buff = file.read(buff_size)
    return count


def count_atom(path):
    """
    count the number of atom in the dump file
    :param path: path of dump file
    :return: number of atom
    """
    with open(path) as f:
        for line in f:
            if "NUMBER OF ATOMS" in line:
                count = int(next(f).strip('\n'))
                break
        return count


def box(path):
    """
    read the information of box in the dump file
    :param path: dump file
    :return: boundary condition, box dimension
    """
    with open(path) as f:
        n = 0
        for line in f:
            if "BOX BOUNDS" in line:
                bc = line.strip('\n').split(' ')[3:]
                dime = np.zeros((len(bc), 2))
                while n < len(bc):
                    # print(next(f))
                    dime[n] = [float(k) for k in next(f).strip('\n').split(' ')]
                    n += 1
                break
    return bc, dime


def read_dump(path):
    """
    read the atom info in the dump file
    :param path: dump file
    :return: atom info such as position, velocity, force; ndarray
    """
    step_num = count_step(path)
    atom_num = count_atom(path)
    dump_data = np.empty((step_num, atom_num, 8))  # create a ndarray to store the atom info

    with open(path, "r") as f:
        m = 0
        for line in f:
            if "ITEM: ATOMS" in line:
                n = 0
                while n < atom_num:
                    dump_data[m, n] = [float(k) for k in next(f).strip('\n').split(' ')[:8]]
                    n += 1
                m += 1
    return dump_data


import pandas as pd
import numpy as np


def read_dump2(path):
    """
   read the atom info in the dump file
   :param path: dump file
   :return: atom info such as position, velocity, force; ndarray
   """
    # read the dump file using pandas
    df = pd.read_csv(path, skiprows=9, delim_whitespace=True, header=None)

    # get the number of steps and atoms
    num_steps = len(df[df[0] == 'ITEM: TIMESTEP'])
    num_atoms = df.iloc[0, 0]

    # convert the data frame to numpy array
    arr = df.values

    # remove the header rows and get only the atom info
    arr = arr[arr[:, 0] == 'ITEM: ATOMS'][1:]

    # convert the array to float
    arr = arr.astype(float)

    # reshape the array to 3D array
    arr = arr.reshape(num_steps, num_atoms, -1)

    return arr


with open("in.json", "r", encoding="UTF-8") as f:
    in_dict = json.load(f)
dump_file = in_dict["dump_path"]
#
# a = time.time()
# print(box(dump_file))
# b = time.time()
# print(b - a)
#
a = time.time()
c = read_dump2(dump_file)
print(c)
b = time.time()
print(b - a)
# print(c[-1][-1])
