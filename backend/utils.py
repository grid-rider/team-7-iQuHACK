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
    
import csv
def csv_clean(csv_file_src: str):
    finished = []
    with open(csv_file_src, newline='\n', mode="r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            sucess = [ element[:-4] for element in row[3].split(",") if element[-4:-2] == "=1"]
            
            sucess = [ (element.split("//")[0][8:],element.split("//")[1][7:]) for element in sucess]

            for element in sucess:
                finished.append(element)
    
    import json
    print(len(finished))
    print(json.dumps(finished))

            
            
# csv_clean("./backend/data/connections.csv")


from PersonMap import PersonMap
from parse import response_to_vector, parse_age_range

def generate_simalarity():
    
    final_result = []
    
    form_submissions = []
    with open('./backend/data/9_19_responses.csv', newline='', mode="r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            response_vector = []
            for question in reader.fieldnames[7:]:  # Assuming questions start at the 8th column
                if question in row:  # Check if the question exists in the row
                    response = response_to_vector(row[question])
                    response_vector.append(response)
            participant = {
                "Nickname": row["nickname"],
                "Email": row["Email"],
                "Gender": row["Gender"],
                "Gender Preference": row["Gender Preference"],
                "Age": int(row["Age"]),
                "Age Preference Range": parse_age_range(row["Age Preference Range (Format example: 20-23)"]),
                "Responses": response_vector,
            }
            form_submissions.append(participant)
    
    _map = PersonMap(form_submissions)
    people = _map.people

    _len_people = len(people)
    
    for i in range(_len_people): 
        _person1 = people[i]

        for j in range(i+1,_len_people):
            
            _person2 = people[j]
            
            simalarity = _map.normalized_similarity(_person1, _person2)
            
            if(simalarity > 0):
                final_result.append([_person1.survey_response["Email"],_person2.survey_response["Email"],simalarity])

    import json
    json_repr = json.dumps(final_result)
    with open("./backend/data/simalarity_map.json", "w") as outfile:
        outfile.write(json_repr)
    

# print(generate_simalarity())
            
