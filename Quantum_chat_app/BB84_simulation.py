from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import random

n =8 

# Alice generates random bits
alice_bits = [random.randint(0,1) for _ in range(n)]
print("Alice bits:", alice_bits)

# Create quantum circuit
qc = QuantumCircuit(n, n)

# Encode bits
for i in range(n):
    if alice_bits[i] == 1:
        qc.x(i)

# Measure qubits
qc.measure(range(n), range(n))

# Run simulator
simulator = AerSimulator()
job = simulator.run(qc, shots=1)
result = job.result()
counts = result.get_counts()

print("Measured result:", counts)

secret_key = list(counts.keys())[0]
print("Generated Quantum Key:", secret_key)