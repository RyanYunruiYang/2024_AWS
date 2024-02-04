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
            gate = Circuit().h(target)
        elif op_name == "I":
            gate = Circuit().i(target)
        elif op_name == "X":
            gate = Circuit().x(target)
        elif op_name == "Y":
            gate = Circuit().y(target)
        elif op_name == "Z":
            gate = Circuit().z(target)
        elif op_name == "S":
            gate = Circuit().si(target)
        elif op_name == "Si":
            gate = Circuit().s(target)
        elif op_name == "T":
            gate = Circuit().ti(target)
        elif op_name == "Ti":
            gate = Circuit().t(target)
        elif op_name == "V":
            gate = Circuit().vi(target)
        elif op_name == "Vi":
            gate = Circuit().v(target)
        elif op_name == "Rx":
            gate = Circuit().rx(target, -angle)
        elif op_name == "Ry":
            gate = Circuit().ry(target, -angle)
        elif op_name == "Rz":
            gate = Circuit().rz(target, -angle)
        elif op_name == "PhaseShift":
            gate = Circuit().phaseshift(target, -angle)
        elif op_name == "CNot":
            gate = Circuit().cnot(*target)
        elif op_name == "Swap":
            gate = Circuit().swap(*target)
        elif op_name == "ISwap":
            gate = Circuit().pswap(*target, -np.pi / 2)
        elif op_name == "PSwap":
            gate = Circuit().pswap(*target, -angle)
        elif op_name == "XY":
            gate = Circuit().xy(*target, -angle)
        elif op_name == "CPhaseShift":
            gate = Circuit().cphaseshift(*target, -angle)
        elif op_name == "CPhaseShift00":
            gate = Circuit().cphaseshift00(*target, -angle)
        elif op_name == "CPhaseShift01":
            gate = Circuit().cphaseshift01(*target, -angle)
        elif op_name == "CPhaseShift10":
            gate = Circuit().cphaseshift10(*target, -angle)
        elif op_name == "CY":
            gate = Circuit().cy(*target)
        elif op_name == "CZ":
            gate = Circuit().cz(*target)
        elif op_name == "XX":
            gate = Circuit().xx(*target, -angle)
        elif op_name == "YY":
            gate = Circuit().yy(*target, -angle)
        elif op_name == "ZZ":
            gate = Circuit().zz(*target, -angle)
        elif op_name == "CCNot":
            gate = Circuit().ccnot(*target)
        elif op_name == "CSwap":
            gate = Circuit().cswap(*target)
        else:
            output_circ = gate.add(output)
    return output_circ