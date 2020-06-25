# Index 15: THI
def get_index_15(x, listener):
    t1 = listener.params[4]
    t2 = listener.params[5]
    data1 = x[:, :, 6:18].mean(axis=2)  # between (530nm : 590nm)
    data2 = x[:, :, 57:65].mean(axis=2)  # between (785nm : 825nm)
    temp1 = data1/data2
    index = (temp1 - t1) / (t2 - t1)
    return index
