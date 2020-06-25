import numpy as np


# Index 13: STO2
def get_index_13(x, listener):
    # get R1 and R2
    r1 = listener.params[0]
    r2 = listener.params[1]
    # between 570nm and 590nm
    data1 = np.ma.amin(np.gradient(np.gradient(x[:, :, 14:18], axis=2), axis=2), axis=2)
    # between 740nm and 780nm
    data2 = np.ma.amin(np.gradient(np.gradient(x[:, :, 48:56], axis=2), axis=2), axis=2)
    temp1 = data1 / r1
    temp2 = data2 / r2
    index = temp1 / (temp1 + temp2)
    print(index)
    return index
