import numpy as np


# Example index 3
def get_index_3(x):
    index = np.gradient(x[:, :, 0:10] + x[:, :, 10:20], axis=2)
    index = index[:, :, :3]
    index = np.moveaxis(index, [0, 1, 2], [2, 1, 0])
    return index
