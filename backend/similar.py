import numpy as np
from numpy.linalg import norm
from typing import Dict, Tuple
from PersonMap import Person

def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Calculate the cosine similarity between two vectors."""
    return np.dot(vec_a, vec_b) / (norm(vec_a) * norm(vec_b))

def check_dealbreakers(person_a: Dict, person_b: Dict) -> bool:
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

def normalized_similarity(person_a: Person, person_b: Person) -> float:
    """Calculate a normalized similarity score between two people, taking into account dealbreakers."""
    # If there are dealbreakers, return a negative score
    person_a_response = person_a.survey_response
    person_b_response = person_b.survey_response

    if not check_dealbreakers(person_a.survey_response, person_b.survey_response):
        return 10.0
    
    # Convert response lists to numpy arrays for cosine similarity calculation
    vec_a = np.array(person_a_response["Responses"])
    vec_b = np.array(person_b_response["Responses"])
    print(f"vec_a: {vec_a}")
    print(f"vec_b: {vec_b}")
    
    # Calculate and return the cosine similarity
    return 1-cosine_similarity(vec_a, vec_b)

# Example usage
person_a = {
    "Gender": "Female",
    "Gender Preference": "Male",
    "Age": 25,
    "Age Preference Range": (24, 30),
    "Responses": [5, 4, 3, 2, 1]  # Simplified vectorized responses for demonstration
}

person_b = {
    "Gender": "Male",
    "Gender Preference": "Female",
    "Age": 27,
    "Age Preference Range": (22, 28),
    "Responses": [1, 2, 3, 4, 5]  # Simplified vectorized responses for demonstration
}

# Calculate normalized similarity
# similarity_score = normalized_similarity(person_a, person_b)
# print(f"Normalized similarity score: {similarity_score}")