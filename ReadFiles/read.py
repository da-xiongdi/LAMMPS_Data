# encoding:-utf
import numpy as np
import json
import time

with open("in.json", "r", encoding="UTF-8") as f:
    in_dict = json.load(f)
dump_file = in_dict["dump_path"]


def read_dump(path):
    # read the dump file
    with open(path, "r") as file:
        in_dump = file.readlines()

    # count the steps and atoms, read the boundary condition and dimension
    boundary = dict()
    for i in range(len(in_dump)):
        if in_dump[i + 1][:len("ITEM: TIMESTEP")] == "ITEM: TIMESTEP":
            count_onestep = i + 1
            break
        elif in_dump[i + 1][:len("ITEM: NUMBER OF ATOMS")] == "ITEM: NUMBER OF ATOMS":
            count_atom = int(in_dump[i + 2].strip('/n'))  # atom number
        elif in_dump[i + 1][:len("ITEM: BOX BOUNDS")] == "ITEM: BOX BOUNDS":
            boundary["condition"] = in_dump[i + 1].strip('\n').split(' ')[3:]  # boundary condition
            boundary["x"] = [float(j) for j in in_dump[i + 2].strip('\n').split(' ')]
            boundary["y"] = [float(j) for j in in_dump[i + 3].strip('\n').split(' ')]
            if len(boundary["condition"]) == 3:
                boundary["z"] = [float(j) for j in in_dump[i + 4].strip('\n').split(' ')]

    count_step = int(len(in_dump) / count_onestep)  # step number

    # write the atom info to dump_data, id type x y z vx vy vz
    dump_data = np.empty((count_step, count_atom, 8))
    # m = 0
    # for i in range(len(in_dump)):
    #     n = 0
    #     if "ITEM: ATOMS id type" in in_dump[i]:
    #         temp = in_dump[i + 1:i + 1 + count_atom]
    #         for j in range(count_atom):
    #             dump_data[m, n] = [float(k) for k in temp[j].strip('\n').split(' ')[:8]]
    #             n += 1
    #         m += 1
    m = 0
    it = iter(in_dump)
    for line in it:
        n = 0
        if "ITEM: ATOMS id type" in line:
            while n < count_atom:
                dump_data[m, n] = [float(k) for k in next(it).strip('\n').split(' ')[:8]]
                n += 1
            m += 1
    del in_dump
    print(dump_data[123, 1455])
    return dump_data


# a = time.time()
# read_dump(dump_file)
# b = time.time()
# print(b - a)


def read_dump2(path):
    # read the dump file
    f = open(path, "r")
    buff = f.read(1024 * 500)
    # print(type(buff))
    print(buff.find("\n", 0))

    return
    dimension, num_dim = [], 10
    j = 0
    atom_info = []
    for line in f:
        if j == 0 and "ITEM: TIMESTEP" in line:
            next(f)
        elif j == 0 and "ITEM: NUMBER OF ATOMS" in line:
            atom_num = int(next(f).strip('\n'))
        elif j == 0 and "ITEM: BOX BOUNDS" in line:
            bc = line.strip("ITEM: BOX BOUNDS").strip('\n').split(" ")
            for m in range(len(bc)): dimension.append([float(k) for k in next(f).strip('\n').split(' ')])
        elif "ITEM: ATOMS" in line:
            i = 0
            while i < atom_num:
                atom_info.append([])
                atom_info[j].append([float(k) for k in next(f).strip('\n').split(' ')[:8]])
                i += 1
            j += 1
    f.close()

    print(atom_info[123][1455])
    # return atom_info


def read_dump3(path):
    file = open(path)
    buff_size = 1024 * 1000
    buff = file.read(buff_size)
    length = 0
    index = []
    while len(buff) > 0:
        start = 0
        pos = buff.find('ITEM: TIMESTEP', start)
        while pos >= 0:
            length += (pos-start+1)
            index.append(pos)
            start = pos + 1
            pos = buff.find('ITEM: TIMESTEP', start)
        buff = file.read(buff_size)
    return index


a = time.time()
print(len(read_dump3(dump_file)))
b = time.time()
print(b - a)

# print(0x0A)
