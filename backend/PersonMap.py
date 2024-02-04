from typing import (
    List
)
import uuid
from utils import people_simalarity

class Person: 

    def __init__(self, survey_response: map, edges: li):
        self.id = uuid.uuid4()
        self.survey_response = survey_response
        self.edges = edges

class PersonMap:
    
    def __init__(self, survey_responses: List[map], simalarity_threshold = 0.6):
        """
        Init of person map 

        Args:
            people (List[perosn]): The people connections contained on the map

        Raises:
            TypeError: If people are of invalid type
        """
        
        if(isinstance(survey_responses, List[map])): 
            raise TypeError("Invalid Argument types")
        
        self.simalarity_threshold = simalarity_threshold 
        
        self.people = self._get_people(survey_responses)
        self.edges = [person.id for person in self.people]
        self.vertices = self._get_vertices(self.people)
        
    def _get_people(self, survey_responses: List[map]) -> List[Person]: 
        
        def _get_vertices(self, people: List[Person]) -> map: 
            _len_people = len(people)
            for i in range(_len_people): 
                for j in range(i, _len_people):
                    simalarity = people_simalarity(person, comparison_person)
                    
                    #Threshold
                    if(simalarity > self.simalarity_threshold): 
                        person
                    
    
    def is_empty(self): 
        return (len(self.edges) == 0)
        

        
     
    



