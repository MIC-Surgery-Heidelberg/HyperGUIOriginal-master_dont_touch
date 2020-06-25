import numpy as np


# Index 14: NIR
def get_index_14(x, listener):
    s1 = listener.params[2]
    s2 = listener.params[3]
    data1 = x[:, :, 65:85].mean(axis=2)  # between (825nm : 925nm)
    data2 = x[:, :, 31:47].mean(axis=2)  # between (655nm : 735nm)
    temp1 = data1/data2
    index = (temp1 - s1) / (s2 - s1)
    index = np.log(np.asarray(index) + 2.51) / np.log(1.3) - 3.8
    return index
