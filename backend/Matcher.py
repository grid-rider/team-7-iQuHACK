# @Author: Armin Ulrich
# Description: 
# This class manages the matching of person 
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit.primitives import Sampler
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit_aer import Aer
from qiskit import transpile
import csv

from typing import(
    List
)

from backend.PersonMap import Person, PersonMap
import copy
import random
class Matcher: 
    
    def __init__(self, survey_responses: List[dict]):
        self.survey_responses = survey_responses
    
    def findmatches(self) -> [Person]: 

        with open('./backend/data/connections.csv', "w", newline='') as csvfile:
            fieldnames = ['id', 'response', 'connections']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writerow({'id': 'id','response': {'Baked':"backed"}, 'connections': ['Beans']})

        
            _filtered_responses = copy.deepcopy(self.survey_responses)
            _probability_per_iteration = 0.8
            counter = 0 

            while(len(_filtered_responses) > 1):
                _subset = []
                for x in range(len(_filtered_responses)): 
                    _random_num = random.randint(0,1)
                    if(_random_num > 0.8):
                        _subset.append(_filtered_responses[x])
                        del _filtered_responses[x]
            
                _map = PersonMap(
                    survey_responses=_subset,
                    simalarity_threshold=0.6
                )
                
                if(_map.edges > 10):
                    raise SystemError("Overflow") 
                # Create a Quadratic Program
                qp = QuadraticProgram()

                # Add binary variables for existing edges
                for edge in _map.edges:
                    qp.binary_var(name=f"c_{edge[0]}_{edge[1]}")

                # Objective function - Minimize the total distance
                linear = {f"c_{edge[0]}_{edge[1]}": weight for edge, weight in _map.edges.items()}
                qp.minimize(linear=linear)

                # Constraints - Ensure each vertex is part of exactly one edge in the solution
                for vertex in _map.vertices:
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

                # Generate the parameterized QAOA circuit

                # # Transpile the circuit for better visualization
                # transpiled_circuit = transpile(qaoa_circuit[0], backend)

                # # Print or draw the circuit
                # print(transpiled_circuit.draw())

                # Solve the QUBO problem using QAOA
                meo = MinimumEigenOptimizer(qaoa)
                result = meo.solve(qubo)

                qaoa_circuit = qaoa.ansatz
                # print(qaoa_circuit)

                print("Solution #{counter}: ", result)
                counter += 1
        