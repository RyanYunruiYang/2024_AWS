from braket.aws import AwsDevice
from braket.circuits import Circuit, gates, noises, observables
from braket.devices import LocalSimulator
from braket.parametric import FreeParameter
import numpy as np
from scipy.stats import unitary_group
import math


def convert_instructions(instructions, n):
    """
    converts the braket base instructions file into a form that is easier to work with
    """
    
    max_qubit_index = n
    qubit_operations = [[] for _ in range(max_qubit_index)]
    
    for i in range(0, len(instructions)):
        inst = instructions[i]
        if(len(inst.target) > 1):
            qubit_operations[inst.target[0]].append({'operator': inst.operator.name, 'time' : i, 'first': True })
            qubit_operations[inst.target[1]].append({'operator': inst.operator.name, 'time' : i, 'first': False})
        else:
            qubit_operations[inst.target[0]].append({'operator': inst.operator.name, 'time': i})
                
    return qubit_operations

def gate_cancellation(instruct_arr):
    """
    Goes through truncated form of circuit and removes operators which square to the identity.
    """
    for gateLine in instruct_arr:
        i = 1
        while(i < len(gateLine)):
            print(gateLine[i])
            a = gateLine[i]['operator']
            b = gateLine[i-1]['operator']
            if(a == b and (a == 'H' or a == 'X' or a == 'Y' or a == 'Z')):
                del gateLine[i]
                del gateLine[i-1]
            i += 1
            

def get_gate_cancelled_circuit(circuit,n):
    """
    Takes in the circuit and then removes any duplicate graphs.
    * Put in the parameter of number of total qubits along with the circuit
    """
    
    instructs = convert_instructions(circuit.instructions,n)
    gate_cancellation(instructs)
    
    new_circuit = Circuit()
    
    for i in range(0, n):
        circuit.i(i)
    
    print(circuit.instructions)
    
    for i in range(len(circuit.instructions)):
        row = circuit.instructions[i]

        op_name = row.operator.name
        
        target = row.target
        
        if(len(instructs[target[0]]) == 0 or instructs[target[0]][0]['time'] != i):
            continue

        if op_name == "H":
            new_circuit.h(target)
        elif op_name == "I":
            new_circuit.i(target)
        elif op_name == "X":
            new_circuit.x(target)
        elif op_name == "Y":
            new_circuit.y(target)
        elif op_name == "Z":
            new_circuit.z(target)
        elif op_name == "S":
            new_circuit.s(target)
        elif op_name == "Si":
            new_circuit.si(target)
        elif op_name == "T":
            new_circuit.t(target)
        elif op_name == "Ti":
            new_circuit.ti(target)
        elif op_name == "V":
            new_circuit.v(target)
        elif op_name == "V":
            new_circuit.vi(target)
        elif op_name == "Rx":
            new_circuit.rx(target, -row.operator.anglegle)
        elif op_name == "Ry":
            new_circuit.ry(target, -row.operator.angle)
        elif op_name == "Rz":
            new_circuit.rz(target, -row.operator.angle)
        elif op_name == "PhaseShift":
            new_circuit.phaseshift(target, -row.operator.angle)
        elif op_name == "CNot":
            new_circuit.cnot(*target)
        elif op_name == "Swap":
            new_circuit.swap(*target)
        elif op_name == "ISwap":
            new_circuit.iswap(*target, -np.pi / 2)
        elif op_name == "PSwap":
            new_circuit.pswap(*target, -row.operator.angle)
        elif op_name == "XY":
            new_circuit.xy(*target, -row.operator.angle)
        elif op_name == "CPhaseShift":
            new_circuit.cphaseshift(*target, -row.operator.angle)
        elif op_name == "CPhaseShift00":
            new_circuit.cphaseshift00(*target, -row.operator.angle)
        elif op_name == "CPhaseShift01":
            new_circuit.cphaseshift01(*target, -row.operator.angle)
        elif op_name == "CPhaseShift10":
            new_circuit.cphaseshift10(*target, -row.operator.angle)
        elif op_name == "CY":
            new_circuit.cy(*target)
        elif op_name == "CZ":
            new_circuit.cz(*target)
        elif op_name == "XX":
            new_circuit.xx(*target, -row.operator.angle)
        elif op_name == "YY":
            new_circuit.yy(*target, -row.operator.angle)
        elif op_name == "ZZ":
            new_circuit.zz(*target, -row.operator.angle)
        elif op_name == "CCNot":
            new_circuit.ccnot(*target)
        elif op_name == "CSwap":
            new_circuit.cswap(*target)
            
        del instructs[target[0]][0]           
    return new_circuit
        
