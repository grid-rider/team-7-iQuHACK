from typing import (
    List
)
import uuid

class Person: 

    def __init__(self, vector, edges = []):
        self.id = uuid()
        self.vector = vector
        self.edges = edges

class PersonMap:
    
    def __init__(self, people: List[Person]):
        """
        Init of person map 

        Args:
            people (List[perosn]): The people connections contained on the map

        Raises:
            TypeError: If people are of invalid type
        """
        
        if( isinstance(people, List[Person])): 
            raise TypeError("Invalid Argument types")
        
        self.edges = []
        self.vertices = self._get_vertices(people)
        
    def _get_vertices(self, people: List[Person]) -> map: 
        pass
    
    def is_empty(self): 
        return (len(self.edges) == 0)
        

        
     
    



