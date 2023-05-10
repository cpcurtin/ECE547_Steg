G = []
import numpy as np
def generateMessageBank(m):
    res = bytes(m, 'utf-8')
    print(res)
    result = []
    for c in m:
        
        #numpy matrix multiplication
        result.append([c]*G)
        print(result)
    return result
if __name__ == '__main__':
    generateMessageBank("HI")