import numpy as np
Z = [[1,2,6,7,15,16,28,29],[3,5,8,14,17,27,30,43],[4,9,13,18,26,31,42,44],[10,12,19,25,32,41,45,54],[11,20,24,33,40,46,53,55],[21,23,34,39,47,52,56,61],[22,35,38,48,51,57,60,62],[36,37,49,50,58,59,63,64]]
def inverse_zigzag(zigzag_array):
    """
    Inverse zigzag of an array into a matrix of size h x w.
    """
    # Create an empty matrix of size h x w
    matrix = np.zeros((8, 8), dtype=np.int16)

    for i in range(8):
        for j in range(8):
            matrix[i][j] = zigzag_array[Z[i][j]-1]
            # result[Z[i][j]] = matrix[i][j]

    return matrix
