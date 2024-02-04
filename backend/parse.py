import csv
from typing import List, Dict, Tuple
from similar import cosine_similarity, check_dealbreakers, normalized_similarity
import numpy as np

def parse_age_range(age_range: str) -> Tuple[int, int]:
    try:
        start, end = age_range.split('-')
        return int(start), int(end)
    except ValueError:
        print(f"Invalid age range: {age_range}")
        return (0, 0)

def check_mutual_age_preference(person_age: int, person_pref: Tuple[int, int], other_age: int, other_pref: Tuple[int, int]) -> bool:
    """Checks if both individuals' ages fall within each other's preferred age ranges."""
    return person_pref[0] <= other_age <= person_pref[1] and other_pref[0] <= person_age <= other_pref[1]

def group_by_email_domain(person: Dict) -> str:
    return "mit" if person["Email"].endswith("@mit.edu") else "external"

def load_csv_and_group_by_age_preference_and_email(filename: str) -> Dict[str, Dict[str, List[Dict]]]:
    groups = {"mit": {}, "external": {}}
    participants = []  # Store all participants for mutual comparison

    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        print(f"Reader fieldnames: {reader.fieldnames}")
        for row in reader:
            participants.append({
                "Nickname": row["nickname"],
                "Email": row["Email"],
                "Gender": row["Gender"],
                "Gender Preference": row["Gender Preference"],
                "Age": int(row["Age"]),
                "Age Preference Range": parse_age_range(row["Age Preference Range (Format example: 20-23)"]),
                "Responses": [response_to_vector(row[question]) for question in reader.fieldnames[7:]],  # Adjusted for indexing
            })
    
    print(participants)

    for person in participants:
        domain_group = group_by_email_domain(person)
        for other in participants:
            if person == other:
                continue  # Skip self-comparison
            if check_mutual_age_preference(person["Age"], person["Age Preference Range"], other["Age"], other["Age Preference Range"]):
                group_key = f"{person['Age Preference Range'][0]}-{person['Age Preference Range'][1]}"
                groups[domain_group].setdefault(group_key, []).append(person)
                break  # Found a mutual match, no need to check further

    return groups

def response_to_vector(response: str) -> int:
    mapping = {
        "Strongly Agree": 5,
        "Agree": 4,
        "Neutral": 3,
        "Disagree": 2,
        "Strongly Disagree": 1,
    }
    return mapping.get(response, 0)

if __name__ == "__main__":
    filename = "./data/9_19_responses.csv"
    all_groups = load_csv_and_group_by_age_preference_and_email(filename)

    # Iterate through each group to calculate pairwise similarity scores
    for domain, age_groups in all_groups.items():
        print(f"\nDomain: {domain}")
        for age_range, members in age_groups.items():
            print(f"\nAge Range {age_range}: Calculating pairwise similarities among {len(members)} members.")
            for i in range(len(members)):
                for j in range(i + 1, len(members)):  # Ensure we don't compare a person with themselves or repeat pairings
                    person_a = members[i]
                    person_b = members[j]
                    # Calculate similarity score
                    score = normalized_similarity(person_a, person_b)
                    print(f"Similarity between {person_a['Email']} and {person_b['Email']}: {score}")
