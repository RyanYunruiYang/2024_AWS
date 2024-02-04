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

def repeat_h():
    circuit= Circuit()
    
    circuit.h(0)
    circuit.h(0)
    circuit.h(0)
    circuit.x(1)
    circuit.h(1)
    circuit.x(1)
    circuit.y(2)
    circuit.y(2)
    circuit.z(3)
    
    return circuit