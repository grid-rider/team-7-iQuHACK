# @Author: Armin Ulrich

from typing import (
    List
)
import numpy as np
from numpy.linalg import norm
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
        self.vertices = [person.survey_response["Email"] for person in self.people] # e.g. ["256aae76-f3f3-4d55-a212-b16eb73e4e13", "264693ac-47e8-4f95-a4ad-7198b4c42026",...]
        self.edges = self._get_edges(self.people) 

            
        
    def _get_edges(self, people: List[Person]) -> dict: 
        """
        Get dictionairy of edges

        Args:
            people (List[Person]):  List of Person Classes

        Returns:
            dict: Dictionary of edges, e.g. {("256aae76-f3f3-4d55-a212-b16eb73e4e13","256aae76-f3f3-4d55-a212-b16eb73e4e13"):5,...}
        """
        # def people_simalarity(person1: Person, person2: Person) -> float: 
        #     """
        #     Vector simalarity computes simalarity of 2 N dimensional vectors

        #     Args:
        #         vector1 (): _description_
        #         vector2 (_type_): _description_

        #     Returns:
        #         float: _description_
        #     """
        #     import random
            
        #     if(not isinstance(person1, Person) and not isinstance(person2, Person)):
        #         raise TypeError("Invalid argument type")
            
        #     return np.random.rand()
        
        _vertices = {}
        _len_people = len(people)
        
        for i in range(_len_people): 
            for j in range(i+1, _len_people):
                
                _person1 = people[i]
                _person2 = people[j]
                
                simalarity = self.normalized_similarity(_person1, _person2)
                
                #Threshold
                # if(simalarity > self.simalarity_threshold): 

                _vertices[(_person1.survey_response["Email"], _person2.survey_response["Email"])] = simalarity
                    
        return _vertices
                        
    def get_person(self, id: str) -> Person:
        if(self.is_empty()):
            raise IndexError("Map is empty")
        
        for person in self.people:
            if(person.id == id):
                return person     
        
        raise IndexError("Id Not Found")
    
    
    def normalized_similarity(self, person_a: Person, person_b: Person) -> float:
        """Calculate a normalized similarity score between two people, taking into account dealbreakers."""

        def check_dealbreakers(person_a: dict, person_b: dict) -> bool:
            """Check for dealbreakers in gender preference and age range."""
            # Gender preference dealbreaker
            if person_a["Gender Preference"] != person_b["Gender"] or person_b["Gender Preference"] != person_a["Gender"]:
                return False
            
            # Age range dealbreaker
            person_a_pref_start, person_a_pref_end = person_a["Age Preference Range"]
            person_b_pref_start, person_b_pref_end = person_b["Age Preference Range"]
            if not (person_a_pref_start <= person_b["Age"] <= person_a_pref_end and
                    person_b_pref_start <= person_a["Age"] <= person_b_pref_end):
                return False
            
            return True

        def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
            """Calculate the cosine similarity between two vectors."""
            return np.dot(vec_a, vec_b) / (norm(vec_a) * norm(vec_b))

        # If there are dealbreakers, return a negative score
        person_a_response = person_a.survey_response
        person_b_response = person_b.survey_response

        if not check_dealbreakers(person_a_response, person_b_response):
            return -1.0
        
        # Convert response lists to numpy arrays for cosine similarity calculation
        vec_a = np.array(person_a_response["Responses"])
        vec_b = np.array(person_b_response["Responses"])
        print(f"vec_a: {vec_a}")
        print(f"vec_b: {vec_b}")
        
        # Calculate and return the cosine similarity
        return cosine_similarity(vec_a, vec_b)

    def is_empty(self): 
        return (len(self.edges) == 0)
        

        
     
    



