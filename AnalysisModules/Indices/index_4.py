# Example index 4
import numpy as np

def get_index_4(x):

    abl = np.gradient(x, axis=2)
    nominator = np.max(abl[:,:,64:68], axis=2)*1000
    val710 = x[:,:,42]
    val900 = x[:,:,80]
    denominator = np.square(((val710 - val900)*100))
    
    
    index = nominator  / denominator
    return index