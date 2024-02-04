from braket.aws import AwsDevice
from braket.circuits import Circuit, gates, noises, observables
from braket.devices import LocalSimulator
from braket.parametric import FreeParameter
import numpy as np
from scipy.stats import unitary_group
import math

import sys 
sys.path.append('../')
from circuits.qft import qft
from simulating_noise import noise_model


def reorder_overall(circuit, num_qubits, fidelities):
    # Read through circuit instructions and look for instances of CNOT, and use them to 
    # generate the demand matrix
    demand = [[0 for i in range(0, num_qubits)] for j in range(0, num_qubits)]
    for row in circuit.instructions:
        if "CPhaseShift" in str(row.operator):
            print(row)
            demand[row.target[0]][row.target[1]] += 1

    print(demand)

    if True: 
        v_f = fidelities
        vertex_map = GreedyV(demand, v_f)
    
    print(vertex_map)

    return reshape(circuit, vertex_map)

def reshape(circuit, vertex_map):
    new_circuit = Circuit()
    for row in circuit.instructions:
        print(row)
        print(row.target[0])

        op_name = row.operator
        try: 
            target = vertex_map[row.target[0]], vertex_map[row.target[1]]
        except:
            target = vertex_map[row.target[0]]

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

        # if "CPhaseShift" in str(row.operator):
        #     print("hi")
        #     new_circuit.cnot(vertex_map[row.target[0]], vertex_map[row.target[1]])
        # else:
        #     new_circuit += row

    print("New Circuit")
    for row in new_circuit.instructions:
        print(row)

    return new_circuit


def GreedyV(demand, vertex_fid):
    assert len(vertex_fid) >= len(demand)

    # Demand and Fidelities are both graphs

    # Sort the vertices by demand
    vertex_demands = [[i, sum(demand[i])] for i in range(0, len(demand))]
    vertex_demands.sort(key = lambda x: -x[1])

    # Sort the vertices by fidelity
    vertex_fidelities = [[i, vertex_fid[i]] for i in range(0, len(vertex_fid))]
    vertex_fidelities.sort(key = lambda x: -x[1])

    # Map the ith largest demand to the ith largest fidelity
    vertex_map = {}
    for i in range(0, len(demand)):
        vertex_map[vertex_demands[i][0]] = vertex_fidelities[i][0]
    
    return vertex_map 



def main():
    # CNOT_usage = [
    #     [0, 1, 1, 1],
    #     [0, 0, 0, 0],
    #     [0, 0, 1, 1],
    #     [0, 0, 0, 0],
    # ]
    # remap = GreedyV(CNOT_usage, vertex_fidelity)   
    # print(remap)

    vertex_fidelity = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    circuit3 = qft(3, [1, 0, 1])

    print("Original Circuit")
    print(circuit3.instructions)

    sorted_circuit = reorder_overall(circuit3, 3, vertex_fidelity)

    print("New Circuit")
    print(circuit3.instructions)


    # print(reshape(circuit3, remap).instructions)
    # device = LocalSimulator('braket_dm')
    # nm = noise_model()
    # nm.apply(circuit3)

    # result = device.run(circuit3, shots=10000).result()
    # measurement = result.measurement_counts

    # print(measurement)

if __name__ == "__main__":
    main()