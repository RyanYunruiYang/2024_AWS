# Will 
# - Generate test circuits
# - Call the circuits which learn noise
# - Feed the information about noise and the intended circuit to the compiler
# - Run the compiled circuits on the noisy simulator

from circuits.qft import qft
from braket.devices import LocalSimulator

from simulating_noise import noise_model
from fidelity_measurement import fidelity_estimate
from ibm_compile import compile

if __name__ == "__main__": 
    test_circuit = qft(3)
    test_circuit_no_noise = qft(3)
    nm = noise_model()

    fidelities = fidelity_estimate(nm)
    compiled_circuit = compile(test_circuit, fidelities)

    # apply the noise model to the circuit
    test_circuit = nm.apply(test_circuit)
    compiled_circuit = nm.apply(compiled_circuit)

    # Run the circuits 
    device = LocalSimulator('braket_dm')
    test_result = device.run(test_circuit, shots=1000).result()
    no_noise_result = device.run(test_circuit_no_noise, shots=1000).result()
    compiled_result = device.run(compiled_circuit, shots=1000).result()
    
    