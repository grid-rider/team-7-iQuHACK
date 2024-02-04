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
import numpy as np

from typing import(
    List
)

from backend.PersonMap import Person, PersonMap
import copy
import random
class Matcher: 
    
    def __init__(self, survey_responses: List[dict]):
        self.survey_responses = survey_responses
    
    def find_matches(self) -> [Person]: 

        with open('./backend/data/connections.csv', "w", newline='') as csvfile:
            fieldnames = ['id', 'response', 'connections', 'result']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            

        
            _filtered_responses = copy.deepcopy(self.survey_responses)
            _probability_per_iteration = 0.6
            counter = 0

            while(counter != len(_filtered_responses)):
                _subset = []
                for x in range(len(_filtered_responses)): 
                    _random_num = np.random.rand()
                    if(_random_num > _probability_per_iteration and _filtered_responses[x] != None):
                        _subset.append(_filtered_responses[x])
                        _filtered_responses[x] = None
                        counter += 1
                       
                    #Breaking condition 
                    if(len(_subset) == 4):
                        break
                
                #Odd edge case
                if((len(_subset) % 2) != 0):
                    for x in range(len(_filtered_responses)): 
                        if( _filtered_responses[x] != None):
                            _subset.append(_filtered_responses[x])
                            _filtered_responses[x] = None
                            counter += 1
                            break
                       
                #2 remaining erdge case
                if((len(_filtered_responses) - counter) == 2):
                    if(_filtered_responses[x] != None):
                        _subset.append(_filtered_responses[x])
                        _filtered_responses[x] = None
                        counter += 1
                        break 
                        
                if((len(_filtered_responses) - counter) == 1):
                    return 
                                       
                _map = PersonMap(
                    survey_responses=_subset,
                    simalarity_threshold=0
                )
                
                if(len(_map.edges) > 10):
                    print("Warning")
                # Create a Quadratic Program
                qp = QuadraticProgram()

                # Add binary variables for existing edges
                for edge in _map.edges:
                    qp.binary_var(name=f"__id1__{edge[0]}//__id2__{edge[1]}")

                # Objective function - Minimize the total distance
                linear = {f"__id1__{edge[0]}//__id2__{edge[1]}": weight for edge, weight in _map.edges.items()}
                qp.minimize(linear=linear)

                # Constraints - Ensure each vertex is part of exactly one edge in the solution
                for vertex in _map.vertices:
                    involved_edges = [f"__id1__{edge[0]}//__id2__{edge[1]}" for edge in _map.edges if vertex in edge]
                    qp.linear_constraint(linear={edge: 1 for edge in involved_edges}, sense='==', rhs=1, name=f"match_constraint_{vertex}")

                # Convert to QUBO
                qubo_converter = QuadraticProgramToQubo()
                qubo = qubo_converter.convert(qp)

                # Initialize the optimizer
                optimizer = COBYLA()
                sampler =  Sampler()

                # Initialize QAOA using the new approach without Sampler, as the code snippet you provided does not fit the actual use of Sampler for QAOA
                qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=2)

                # Solve the QUBO problem using QAOA
                meo = MinimumEigenOptimizer(qaoa)
                result = meo.solve(qubo)

                qaoa_circuit = qaoa.ansatz
                # print(qaoa_circuit)

                print(f"Solution #{counter}: ", result)

                writer.writerow({'id': "", 'response': "", 'connections':"", 'result': result})

                counter += 1
        