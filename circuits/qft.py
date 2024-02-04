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

def qft(n, arr):
    circuit = Circuit()
    
    for i in len(arr):
        if(arr[i] == 1):
            circuit.x(i)
    
    for i in range(0, n):
        circuit.h(i)
        for j in range(1, n - i):
            circuit.cphaseshift(i+j,i,(2 * np.pi / math.pow(2,j)))

    return circuit

qft = qft(4)

print(qft)
