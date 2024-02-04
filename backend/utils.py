from typing import (
    List
)
from PersonMap import Person
import random

def people_simalarity(person1: Person, person2: Person) -> float: 
    """
    Vector simalarity computes similarity of 2 N dimensional vectors

        Args:
            vector1 (): _description_
            vector2 (_type_): _description_

        Returns:
            float: _description_
        """
        
        if(not isinstance(person1, Person) and not isinstance(person2, Person)):
            raise TypeError("Invalid argument type")
        
        return random.randint(0,1)
        