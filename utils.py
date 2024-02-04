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