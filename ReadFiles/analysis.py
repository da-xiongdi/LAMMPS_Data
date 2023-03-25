import numpy as np
from read4MD import *


def spatial_bin(atom_data, bin_dim, bin_size, boundary, bin_origin=None):
    box_dim = boundary  # boundary in x, y, z
    box_size = boundary[:, 1] - boundary[:, 0]

    temp_x = np.arange(box_dim[0, 0], box_dim[0, 1], bin_size[0])
    # bin_bound_x = np.vstack((temp, temp + bin_size[0]))
    # bin_bound_x[bin_bound_x > box_dim[0, 1]] = box_dim[0, 1]
    temp_y = np.arange(box_dim[1, 0], box_dim[1, 1], bin_size[1])
    # bin_bound_y = np.vstack((temp, temp + bin_size[1]))
    # # bin_bound_y = np.where(bin_bound_y > bin_dim[1, 1], bin_dim[1, 1], bin_bound_y)
    # bin_bound_y[bin_bound_y > box_dim[1, 1]] = box_dim[1, 1]

    atom_xyz = atom_data[:, 2:5]

    x_idx = np.digitize(atom_xyz[:, 0], temp_x) - 1
    y_idx = np.digitize(atom_xyz[:, 1], temp_y) - 1
    grid_counts, _, _ = np.histogram2d(x_idx, y_idx, bins=[len(temp_x)-1, len(temp_y)-1])
    print(grid_counts)
    # print(atom_xyz[:, 0])
    # bin_x_atom_num = np.zeros(bin_bound_x.shape[1])
    # bin_atom_num = np.zeros((bin_bound_x.shape[1], bin_bound_y.shape[1]))
    # for i in range(bin_bound_x.shape[1]):
    #     for j in range(bin_bound_y.shape[1]):
    #         bin_x_in = np.logical_and(bin_bound_x[1, i] > atom_xyz[:, 0], atom_xyz[:, 0] > bin_bound_x[0, i])
    #         bin_y_in = np.logical_and(bin_bound_y[1, j] > atom_xyz[:, 1], atom_xyz[:, 1] > bin_bound_y[0, j])
    #         bin_atom_num[i, j] = np.sum(np.logical_and(bin_x_in, bin_y_in))
    #
    # print(bin_bound_y[1, 100], bin_bound_x[1,100])
    # print(bin_atom_num[100,100])

    # bin_num = np.ceil(box_size[bin_dim] / bin_size)
    # atom_binned = np.zeros((bin_num[0], bin_num[1]))
    #
    # atom_data[0,1]<

    # for i in range(bin_num[0]):
    #     for j in range(bin_num[1]):

    # for dim in bin_dim:
    #     bin_num[i] = bin_size / 1
    #     i = 0


# a = [0, 1]
# b = np.arange(0,6).reshape((3,2))
# print(b)
# print(b[a])
with open("in.json", "r", encoding="UTF-8") as f:
    in_dict = json.load(f)
dump_file = in_dict["dump_path"]

a = time.time()
box_dime = box(dump_file)

data = read_dump(dump_file)
b = time.time()
print(b - a)
spatial_bin(data[0], [0, 1], np.array([4, 4]), boundary=box_dime[1])

c = time.time()
print(c - b)

# a = np.arange(12)
# print(np.sum(np.logical_and(a < 5, a > 2)))
# print(a[a < 3])
