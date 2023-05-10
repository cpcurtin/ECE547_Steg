G = []
import numpy as np
import bitarray
G = np.matrix('1 0 0 0 1 0 1; 0 1 0 0 1 1 0; 0 0 1 0 1 1 1; 0 0 0 1 0 1 1',dtype=int)
H = np.matrix('1 0 1; 1 1 0 ; 1 1 1; 0 1 1; 1 0 0 ; 0 1 0; 0 0 1',dtype=int).transpose()

def generateMessageBank(m):
    ba = bitarray.bitarray()
    ba.frombytes(m.encode('utf-8'))
    l = ba.tolist()
    # Convert Back
    # bitarray.bitarray(l)
    # bitarray.bitarray(l).tobytes().decode('utf-8')
    while(len(l)%4 != 0):
        l.append(False) # append zeros till a multiple of 4
    n = int(len(l)/4)
    
    result = []
    for i in range(n):    
        c = np.matrix(l[4*i:4*(i+1)],dtype=int)
        #temp = c*G%2
        result.append(c*G%2)
        # print(H)
        # print(temp)
        # print(H*temp.transpose()%2)
    return result, n
def verify(l):
    lMatrix = np.matrix(l,dtype=int).transpose()
    s = H*lMatrix%2
    return (s[0,0] == 0) & (s[1,0] == 0) & (s[2,0] == 0)

if __name__ == '__main__':
    a,b=generateMessageBank("BYE")
    l = [0, 0, 0, 1, 1, 0, 1]
    verify(l)
