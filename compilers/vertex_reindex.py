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



def reshape(circuit, vertex_map):
    new_circuit = Circuit()
    for row in circuit.instructions:
        if row.operator == "cnot":
            new_circuit.cnot(vertex_map[row.target], vertex_map[row.control])
        else:
            new_circuit.add_instruction(row)
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
        vertex_map[vertex_fidelities[i][0]] = vertex_demands[i][0]
    
    return vertex_map 



def main():
    CNOT_usage = [
        [0, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 0],
    ]
    vertex_fidelity = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    remap = GreedyV(CNOT_usage, vertex_fidelity)   
    print(remap)


    circuit3 = qft(3)
    device = LocalSimulator('braket_dm')
    nm = noise_model()
    nm.apply(circuit3)

    result = device.run(circuit3, shots=10000).result()
    measurement = result.measurement_counts

    print(measurement)

if __name__ == "__main__":
    main()