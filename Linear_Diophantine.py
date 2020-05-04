# Colin Greeley #

import numpy as np
from itertools import combinations, permutations, product
import math

# returns the max value of a polynomial equation
def Cmax(C):                                            
    X = list(product([0,1], repeat=4))
    solutions = list()
    for x in X:
        solutions.append(abs(C[0]*x[0] + C[1]*x[1] + C[2]*x[2] + x[3]))
    return np.max(solutions)

# returns the length of a binary value
def KC(C):
    if C[0] == 0:
        return 0
    bits = np.unpackbits(np.array(C, dtype=np.uint8))
    while bits[0] == 0:
        bits = bits[1:]
    return len(bits)

# converts an int to binary and returns specified index value
def bi(C, i):
    if C[0] == 0:
        return 0
    bits = np.unpackbits(np.array(C, dtype=np.uint8))
    if (i > len(bits)):
        return 0
    return bits[7-i]

# helper function for making the states of the automaton, 
# impliments Zhe Dang's equation for (carry, i) -> (carry', i') on reading input symbol (a1, a2, a3)
def get_states(C, state):
    carry, i = state
    X = list(product([0,1], repeat=len(C)-1))
    solutions = dict()
    for a in X:
        R = 0
        for j in range(len(C)-1):
            R += C[j]*a[j]
        R += bi([C[-1]], i) + carry
        if R % 2 == 0:
            key = ''.join([str(u) for u in a])
            carry = int(R/2)
            solutions.update({key:(carry, i+1)})
    return solutions

# creates an automaton composed of states and edge values, made with a dictionary
def create_finite_automaton(constants, automaton, state, bits):
    if state[1] >= bits:
        return automaton
    state_values = get_states(constants, state)
    automaton.update({state:state_values})
    for state in state_values.values():
        create_finite_automaton(constants, automaton, state, bits)
    return automaton

# finds a path from the initial state to the accepting state of a given automaton,
# if there is no solution, [] is returned
def solution_search(automaton, C, bits):
    X = list(product([0,1], repeat=len(C)-1))
    keys = list()
    for x in X:
        x = [str(i) for i in x]
        keys.append(''.join(x))
    key_index = [0 for _ in range(bits)]
    state = (0,0)
    states = [state]
    while state != (0,bits):
        while keys[key_index[state[1]]] not in automaton[state]:
            key_index[state[1]] += 1
            while key_index[state[1]] >= bits-1:                # change states
                if states == []:
                    return [keys[i] for i in key_index]
                state = states.pop(-1)
                key_index = [0 if i >= state[1] else key_index[i] for i in range(bits)]
                if states == []:
                    return [keys[i] for i in key_index]
                state = states.pop(-1)
                key_index[state[1]] += 1
        state = automaton[state][keys[key_index[state[1]]]]
        states.append(state)
        while state[1] == bits and state[0] != 0:               # change states
            if states == []:
                return [keys[i] for i in key_index]
            state = states.pop(-1)
            key_index = [0 if i >= state[1] else key_index[i] for i in range(bits)]
            if states == []:
                return [keys[i] for i in key_index]
            state = states.pop(-1)
            key_index[state[1]] += 1
        if (state[1] < bits):
            if key_index[state[1]] >= bits-1:                   # change states
                if states == []:
                    return [keys[i] for i in key_index]
                state = states.pop(-1)
                key_index = [0 if i >= state[1] else key_index[i] for i in range(bits)]
                if states == []:
                    return [keys[i] for i in key_index]
                state = states.pop(-1)
                key_index[state[1]] += 1
    return [keys[i] for i in key_index]

# checks if an input word is accepted by a given automaton
def run_input_on_automaton(FA, inputs, bits):
    print('Input word:')
    for i in inputs:
        print(np.unpackbits(np.array([i], dtype=np.uint8)))
    state = (0, 0)
    for i in range(bits):
        print('State{}: '.format(i), state)
        key = ''.join([str(bi([u], i)) for u in inputs])
        if key not in FA[state]:
            print('The input word is not accepted by this automaton')
            return
        state = FA[state][key]
    print('Final state:', state)
    print('The input word is accepted by this automaton')

# print out all states and edges of a given automaton
def print_states(automaton):
    for i in automaton.items():
        print(i)

# converts path to accepting state to integer values for the polynomial equation solution
def convert(path):
    def str_to_list(X):
        return int(''.join(str(x) for x in X), 2) 
    path = np.array([list(i) for i in path]).T
    path = np.array([np.flip(i) for i in path])
    return [str_to_list(i) for i in path]

# test 1
def T1(bits):
    print('\nT1:')
    c1 = (3,-2,1,5)
    c2 = (6,-4,2,9)
    M1, M2 = dict(), dict()
    M1 = create_finite_automaton(c1, M1, (0,0), bits)
    M2 = create_finite_automaton(c2, M2, (0,0), bits)
    #print_states(M1)
    #print()
    #print_states(M2)
    path_to_accepting_state_M1 = solution_search(M1, c1, bits)
    path_to_accepting_state_M2 = solution_search(M2, c2, bits)
    M1_outputs = convert(path_to_accepting_state_M1)
    M2_outputs = convert(path_to_accepting_state_M2)
    print('M1 outputs:', M1_outputs)
    print('M2 outputs:', M2_outputs)
    run_input_on_automaton(M1, M1_outputs, bits)
    run_input_on_automaton(M2, M2_outputs, bits)

# test 2
def T2(bits):
    print('\nT2:')
    c1 = (3,-2,-1,3)
    c2 = (6,-4,1,3)
    M1, M2 = dict(), dict()
    M1 = create_finite_automaton(c1, M1, (0,0), bits)
    M2 = create_finite_automaton(c2, M2, (0,0), bits)
    #print_states(M1)
    #print()
    #print_states(M2)
    path_to_accepting_state_M1 = solution_search(M1, c1, bits)
    path_to_accepting_state_M2 = solution_search(M2, c2, bits)
    M1_outputs = convert(path_to_accepting_state_M1)
    M2_outputs = convert(path_to_accepting_state_M2)
    print('M1 outputs:', M1_outputs)
    print('M2 outputs:', M2_outputs)
    run_input_on_automaton(M1, M1_outputs, bits)
    run_input_on_automaton(M2, M2_outputs, bits)


if __name__ == "__main__":

    bits = 8
    T1(bits)
    T2(bits)