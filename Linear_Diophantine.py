import numpy as np
from itertools import combinations, permutations, product
import math


def Cmax(C):
    X = list(product([0,1], repeat=3))
    solutions = list()
    for x in X:
        solutions.append(abs(C[0]*x[0] + C[1]*x[1] + C[2]*x[2] + C[3]))
    return np.max(solutions)

def KC(C):
    if C[0] == 0:
        return 0
    bits = np.unpackbits(np.array(C, dtype=np.uint8))
    while bits[0] == 0:
        bits = bits[1:]
    return len(bits)

def bi(C, i):
    if C[0] == 0:
        return 0
    bits = np.unpackbits(np.array(C, dtype=np.uint8))
    if (i > len(bits)):
        return 0
    return bits[7-i]

def create_finite_automaton(bits):
    def normal_state(i):
        return {(0, i):{'000':(0,i+1),
                        '101':(0,i+1),
                        '011':(0,i+1),
                        '110':(1,i+1)}}
    def carry_state(i):
        return {(1, i):{'001':(0,i+1),
                        '100':(1,i+1),
                        '010':(1,i+1),
                        '111':(1,i+1)}}
    automaton = dict()
    for i in range(bits):
        automaton.update(normal_state(i))
        automaton.update(carry_state(i))

    return automaton



if __name__ == "__main__":
    '''
    cmax = Cmax([3, 0, -4, -17])
    print(cmax)
    kc = get_KC([34])
    print(kc)
    '''

    bits = 8

    M1 = create_finite_automaton(bits)
    for i in M1.items():
        print(i)

    x, y, z = 13, 4, 17
    print(np.unpackbits(np.array([x], dtype=np.uint8)))
    print(np.unpackbits(np.array([y], dtype=np.uint8)))
    print(np.unpackbits(np.array([z], dtype=np.uint8)))

    state = (0,0)
    for i in range(bits):
        print('State:', i+1)
        key = str(bi([x], i)) + str(bi([y], i)) + str(bi([z], i)) 
        state = M1[state][key]
    print(state)
