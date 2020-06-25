# Index 16: TWI
def get_index_16(x, listener):
    u1 = listener.params[6]
    u2 = listener.params[7]
    data1 = x[:, :, 76:80].mean(axis=2)  # between (880nm : 900nm)
    data2 = x[:, :, 91:96].mean(axis=2)  # between (955nm : 980nm)
    temp1 = data1/data2
    index = (temp1 - u1) / (u2 - u1)
    return index
