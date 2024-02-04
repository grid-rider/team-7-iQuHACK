from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.converters import QuadraticProgramToQubo
# from qiskit.utils import algorithm_globals
from qiskit.primitives import Sampler
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit_aer import Aer
from qiskit import transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Sampler, Options
import os

# Define the graph


edges = {
    ('A', 'B'): 0.04,
    ('A', 'C'): 0.03,
    ('B', 'E'): 0.06,
    ('C', 'D'): 0.1,
    ('F', 'D'): 0.4,
    ('A', "F"): 0.04,
}
vertices = ['A', 'B', 'C', 'D', 'E', "F"]

# edges = {
#     ('A', 'B'): 0.4, ('A', 'C'): 0.3, ('B', 'D'): 0.6, ('C', 'D'): 1.0,
#     ('G', 'J'): 0.3, ('A', 'E'): 0.5, ('B', 'F'): 0.6, ('C', 'G'): 0.7,
# }

# vertices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

# Create a Quadratic Program
qp = QuadraticProgram()

# Add binary variables for existing edges
for edge in edges:
    qp.binary_var(name=f"c_{edge[0]}_{edge[1]}")

# Objective function - Minimize the total distance
linear = {f"c_{edge[0]}_{edge[1]}": weight for edge, weight in edges.items()}
qp.minimize(linear=linear)

# Constraints - Ensure each vertex is part of exactly one edge in the solution
for vertex in vertices:
    involved_edges = [f"c_{edge[0]}_{edge[1]}" for edge in edges if vertex in edge]
    qp.linear_constraint(linear={edge: 1 for edge in involved_edges}, sense='==', rhs=1, name=f"match_constraint_{vertex}")

# Convert to QUBO
qubo_converter = QuadraticProgramToQubo()
qubo = qubo_converter.convert(qp)

# # Set the random seed for reproducible results
# algorithm_globals.random_seed = 10598

# Initialize the optimizer
optimizer = COBYLA()

# Initialize QAOA using the new approach without Sampler, as the code snippet you provided does not fit the actual use of Sampler for QAOA
key = os.getenv('secret_key')
service = QiskitRuntimeService(channel="ibm_quantum", token=key)
 

options = Options(optimization_level=1)
options.execution.shots = 1024  # Options can be set using auto-complete.

backend = service.get_backend('ibmq_qasm_simulator')
sampler = Sampler(backend=backend, options=options)

qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=2)

# Convert QUBO problem to Ising Hamiltonian (PauliSumOp)
op, offset = qubo.to_ising()

# Solve the QUBO problem using QAOA
meo = MinimumEigenOptimizer(qaoa)
result = meo.solve(qubo)
print("Solution: ", result)


# qaoa_circuit = qaoa.ansatz
# print(qaoa_circuit)


# import os
# from qiskit_ibm_runtime import QiskitRuntimeService, Options, Sampler
# from qiskit import QuantumCircuit

# key = os.getenv('secret_key')

# service = QiskitRuntimeService(channel="ibm_quantum",token=key)
# options = Options(optimization_level=1)
# options.execution.shots = 1024  # Options can be set using auto-complete.

# # 1. A quantum circuit for preparing the quantum state (|00> + |11>)/rt{2}
# bell = QuantumCircuit(2)
# bell.h(0)
# bell.cx(0, 1)

# # 2. Map the qubits to a classical register in ascending order
# bell.measure_all()

# # 3. Execute using the Sampler primitive
# backend = service.get_backend('ibmq_qasm_simulator')
# sampler = Sampler(backend=backend, options=options)
# job = sampler.run(circuits=bell)
# print(f"Job ID is {job.job_id()}")
# print(f"Job result is {job.result()}")