from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.converters import QuadraticProgramToQubo
# from qiskit.utils import algorithm_globals
from qiskit.primitives import Sampler
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit_aer import Aer
from qiskit import transpile

# Define the graph
edges = {
    ('A', 'B'): 4,
    ('A', 'C'): 3,
    ('B', 'D'): 6,
    ('C', 'D'): 10
}
vertices = ['A', 'B', 'C', 'D']

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

# Assuming `qubo` is your QuadraticProgram object from before
# First, convert the QUBO into a PauliSumOp for QAOA
qubo_converter = QuadraticProgramToQubo()
qubo_problem = qubo_converter.convert(qubo)

# Initialize the optimizer
optimizer = COBYLA()
backend = Aer.get_backend('aer_simulator_statevector')
sampler =  Sampler()

# Initialize QAOA using the new approach without Sampler, as the code snippet you provided does not fit the actual use of Sampler for QAOA
qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=2)

# Convert QUBO problem to Ising Hamiltonian (PauliSumOp)
op, offset = qubo.to_ising()

# # Generate the parameterized QAOA circuit
# qaoa_circuit = qaoa.construct_circuit(qaoa.ansatz.parameters, op)

# # Transpile the circuit for better visualization
# transpiled_circuit = transpile(qaoa_circuit[0], backend)

# # Print or draw the circuit
# print(transpiled_circuit.draw())

# Solve the QUBO problem using QAOA
meo = MinimumEigenOptimizer(qaoa)
result = meo.solve(qubo)

print("Solution: ", result)