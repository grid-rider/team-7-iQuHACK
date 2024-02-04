# @Author: Armin Ulrich

from typing import (
    List
)
import numpy as np
import uuid

    

class Person: 

    def __init__(self, survey_response: dict):
        """
        Person wrapper classes. Contains survey response and new ID

        Args:
            survey_response (dict): Survey response dictionairy
        """
        self.id = str(uuid.uuid4())
        self.survey_response = survey_response
        
        

class PersonMap:
    
    def __init__(self, survey_responses: List[dict], simalarity_threshold = 0.6):
        """
        Init of person map 

        Args:
            survey_responses (List[map]): The survey responses
            
        Attributes:
            simalarity_threshold (float): Thrershold of acceptable simalarity (between 0 and 1)
            people (List[Person]): Person class list of survey responses
            vertices (list): Vertices of graph (i.e. people), represented as ID
            edges (dict): Dictionairy of vertices e.g. {("A","B"):5} equivalent to edge between A and B with weight 5

        Raises:
            TypeError: If the survey responses are of invalid type
        """
        
        if(not isinstance(survey_responses, list)): 
            raise TypeError("Invalid Argument types")
        
        self.simalarity_threshold = simalarity_threshold 
        
        self.people = [Person(response) for response in survey_responses]
        self.vertices = [person.id for person in self.people] # e.g. ["256aae76-f3f3-4d55-a212-b16eb73e4e13", "264693ac-47e8-4f95-a4ad-7198b4c42026",...]
        self.edges = self._get_edges(self.people) 

            
        
    def _get_edges(self, people: List[Person]) -> dict: 
        """
        Get dictionairy of edges

        Args:
            people (List[Person]):  List of Person Classes

        Returns:
            dict: Dictionary of edges, e.g. {("256aae76-f3f3-4d55-a212-b16eb73e4e13","256aae76-f3f3-4d55-a212-b16eb73e4e13"):5,...}
        """
        def people_simalarity(person1: Person, person2: Person) -> float: 
            """
            Vector simalarity computes simalarity of 2 N dimensional vectors

            Args:
                vector1 (): _description_
                vector2 (_type_): _description_

            Returns:
                float: _description_
            """
            import random
            
            if(not isinstance(person1, Person) and not isinstance(person2, Person)):
                raise TypeError("Invalid argument type")
            
            return np.random.rand()
        
        _vertices = {}
        _len_people = len(people)
        
        for i in range(_len_people): 
            for j in range(i+1, _len_people):
                
                _person1 = people[i]
                _person2 = people[j]
                
                simalarity = people_simalarity(_person1, _person2)
                
                #Threshold
                if(simalarity > self.simalarity_threshold): 
                    _vertices[(_person1.id, _person2.id)] = simalarity
                    
        return _vertices
                        
    def get_person(self, id: str) -> Person:
        if(self.is_empty()):
            raise IndexError("Map is empty")
        
        for person in self.people:
            if(person.id == id):
                return person     
        
        raise IndexError("Id Not Found")
    
    def is_empty(self): 
        return (len(self.edges) == 0)
        

        
     
    



