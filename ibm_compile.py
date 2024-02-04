import numpy as np
from braket.circuits import Circuit
from braket.aws import AwsDevice

def ibm_compile(circuit: Circuit) -> Circuit:

    deveice = AwsDevice("arn:aws:braket:::device/quantum-simulator/amazon/sv1")
    output = Circuit()

    # Loop through the instructions (gates) in the circuit:
    for instruction in circuit.instructions:
        # Save the operator name and target
        op_name = instruction.operator.name
        target = instruction.target
        angle = None
        # If the operator has an attribute called 'angle', save that too
        if hasattr(instruction.operator, "angle"):
            angle = instruction.operator.angle

        # To make use of native gates, we'll define the operation for each 
        if op_name == "H":
            gate = output.h(target)
        elif op_name == "I":
            gate = output.i(target)
        elif op_name == "X":
            gate = output.x(target)
        elif op_name == "Y":
            gate = output.y(target)
        elif op_name == "Z":
            gate = output.z(target)
        elif op_name == "S":
            gate = output.s(target)
        elif op_name == "Si":
            gate = output.si(target)
        elif op_name == "T":
            gate = output.t(target)
        elif op_name == "Ti":
            gate = output.ti(target)
        elif op_name == "V":
            gate = output.v(target)
        elif op_name == "V":
            gate = output.vi(target)
        elif op_name == "Rx":
            gate = output.rx(target, -angle)
        elif op_name == "Ry":
            gate = output.ry(target, -angle)
        elif op_name == "Rz":
            gate = output.rz(target, -angle)
        elif op_name == "PhaseShift":
            gate = output.phaseshift(target, -angle)
        elif op_name == "CNot":
            gate = output.cnot(*target)
        elif op_name == "Swap":
            gate = output.swap(*target)
        elif op_name == "ISwap":
            gate = output.iswap(*target, -np.pi / 2)
        elif op_name == "PSwap":
            gate = output.pswap(*target, -angle)
        elif op_name == "XY":
            gate = output.xy(*target, -angle)
        elif op_name == "CPhaseShift":
            gate = output.cphaseshift(*target, -angle)
        elif op_name == "CPhaseShift00":
            gate = output.cphaseshift00(*target, -angle)
        elif op_name == "CPhaseShift01":
            gate = output.cphaseshift01(*target, -angle)
        elif op_name == "CPhaseShift10":
            gate = output.cphaseshift10(*target, -angle)
        elif op_name == "CY":
            gate = output.cy(*target)
        elif op_name == "CZ":
            gate = output.cz(*target)
        elif op_name == "XX":
            gate = output.xx(*target, -angle)
        elif op_name == "YY":
            gate = output.yy(*target, -angle)
        elif op_name == "ZZ":
            gate = output.zz(*target, -angle)
        elif op_name == "CCNot":
            gate = output.ccnot(*target)
        elif op_name == "CSwap":
            gate = output.cswap(*target)
        else:
            output_circ = gate.add(output)
    return output_circ