# Use Braket SDK Cost Tracking to estimate the cost to run this example
from braket.tracking import Tracker
t = Tracker().start()

from braket.aws import AwsDevice
from braket.circuits import Circuit, gates, noises, observables
from braket.devices import LocalSimulator
from braket.parametric import FreeParameter
import numpy as np
from scipy.stats import unitary_group
import math

def convert_instructions(instructions, n):
    # Find the maximum qubit index to determine the size of the output array
    max_qubit_index = n
    # Initialize the output array with empty lists for each qubit
    qubit_operations = [[] for _ in range(max_qubit_index)]
    # Iterate through instructions and append operations to the corresponding qubit
    for i in range(0, len(instructions)):
        inst = instructions[i]
        if(len(inst.target) > 1):
            qubit_operations[inst.target[0]].append({'operator': inst.operator.name, 'time' : i, 'first': True })
            qubit_operations[inst.target[1]].append({'operator': inst.operator.name, 'time' : i, 'first': False})
        else:
            qubit_operations[inst.target[0]].append({'operator': inst.operator.name, 'time': i})
                
        # Additional processing for control-target operations could be added here if necessary
    return qubit_operations

def gate_cancellation(instruct_arr):
    for gateLine in instruct_arr:
        print(gateLine)
        i = 1
        while(i < len(gateLine)):
            print(gateLine[i])
            a = gateLine[i]['operator']
            b = gateLine[i-1]['operator']
            if(a == b and (a == 'H' or a == 'X' or a == 'Y' or a == 'Z')):
                del gateLine[i]
                del gateLine[i-1]
            i += 1
            
           
