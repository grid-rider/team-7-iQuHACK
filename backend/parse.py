import csv
from typing import List, Dict, Tuple
from similar import cosine_similarity, check_dealbreakers, normalized_similarity
import numpy as np

def parse_age_range(age_range: str) -> Tuple[int, int]:
    try:
        # Handle single number age ranges by using it as both lower and upper bounds
        if age_range.isdigit():
            age = int(age_range)
            return age, age
        elif "-" in age_range:
            start, end = age_range.split('-')
            return int(start), int(end)
        elif age_range.lower() in ["20 and older", "integer", "??"]:
            # For "20 and older", set a reasonable upper limit or handle as case-specific
            if age_range.lower() == "20 and older":
                return 20, 99  # Assuming 99 as an arbitrary upper limit
            # For ambiguous or invalid inputs, return a default range or flag as invalid
            else:
                print(f"Invalid age range: {age_range}")
                return 0, 0  # Invalid or ambiguous ranges are set to (0, 0)
    except ValueError:
        print(f"Invalid age range: {age_range}")
        return 0, 0

def check_mutual_age_preference(person_age: int, person_pref: Tuple[int, int], other_age: int, other_pref: Tuple[int, int]) -> bool:
    """Checks if both individuals' ages fall within each other's preferred age ranges."""
    return person_pref[0] <= other_age <= person_pref[1] and other_pref[0] <= person_age <= other_pref[1]

def group_by_email_domain(person: Dict) -> str:
    return "mit" if person["Email"].endswith("@mit.edu") else "external"

def load_participants(filename: str) -> Dict[str, List[Dict]]:
    participants = {"mit": [], "external": []}

    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            domain_group = "mit" if row["Email"].endswith("@mit.edu") else "external"
            responses = []
            for question in reader.fieldnames[7:]:  # Assuming questions start at the 8th column
                if question in row:  # Check if the question exists in the row
                    response = response_to_vector(row[question])
                    responses.append(response)
            participant = {
                "Nickname": row["nickname"],
                "Email": row["Email"],
                "Gender": row["Gender"],
                "Gender Preference": row["Gender Preference"],
                "Age": int(row["Age"]),
                "Age Preference Range": parse_age_range(row["Age Preference Range (Format example: 20-23)"]),
                "Responses": responses,
            }
            participants[domain_group].append(participant)

    return participants

def calculate_and_print_similarities(participants: Dict[str, List[Dict]]):
    for domain, members in participants.items():
        positive_similarity_count = 0
        non_positive_similarity_count = 0
        high_compatibility_count = 0
        
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                score = normalized_similarity(members[i], members[j])
                if score > 0:
                    positive_similarity_count += 1
                    if score > 0.9:
                        high_compatibility_count += 1
                else:
                    non_positive_similarity_count += 1
        
        print(f"\nDomain: {domain}")
        print(f"Total positive similarity pairs: {positive_similarity_count}")
        print(f"Total non-positive similarity pairs: {non_positive_similarity_count}")
        print(f"Total high compatibility pairs (similarity > 0.9): {high_compatibility_count}")

# def load_csv_and_group_by_age_preference_and_email(filename: str) -> Dict[str, Dict[str, List[Dict]]]:
#     groups = {"mit": {}, "external": {}}
#     participants = []  # Store all participants for mutual comparison

#     with open(filename, mode='r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         print(f"Reader fieldnames: {reader.fieldnames}")
#         for row in reader:
#             participants.append({
#                 "Nickname": row["nickname"],
#                 "Email": row["Email"],
#                 "Gender": row["Gender"],
#                 "Gender Preference": row["Gender Preference"],
#                 "Age": int(row["Age"]),
#                 "Age Preference Range": parse_age_range(row["Age Preference Range (Format example: 20-23)"]),
#                 "Responses": [response_to_vector(row[question]) for question in reader.fieldnames[7:]],
#             })

#     for person in participants:
#         domain_group = group_by_email_domain(person)
#         for other in participants:
#             if person == other:
#                 continue  # Skip self-comparison
#             if check_mutual_age_preference(person["Age"], person["Age Preference Range"], other["Age"], other["Age Preference Range"]):
#                 group_key = f"{person['Age Preference Range'][0]}-{person['Age Preference Range'][1]}"
#                 groups[domain_group].setdefault(group_key, []).append(person)
#                 break  # Found a mutual match, no need to check further

#     # return groups
#     positive_similarity_count = 0  # Counter for positive similarity scores
#     non_positive_similarity_count = 0  # Counter for non-positive similarity scores
#     high_compatibility_count = 0  # Counter for similarity scores over 0.9

#     # Iterate through all pairs of participants
#     for i in range(len(participants)):
#         for j in range(i + 1, len(participants)):
#             person_a = participants[i]
#             person_b = participants[j]
#             # Convert the list of responses into numpy arrays for similarity calculation
#             person_a['Responses'] = np.array(person_a['Responses'])
#             person_b['Responses'] = np.array(person_b['Responses'])
#             # Calculate the similarity score
#             score = normalized_similarity(person_a, person_b)
#             if score > 0:
#                 positive_similarity_count += 1
#                 print(f"Positive similarity found between {person_a['Email']} and {person_b['Email']}: {score}")
#                 if score > 0.9:
#                     high_compatibility_count += 1
#             else:
#                 non_positive_similarity_count += 1

#     print(f"\nTotal positive similarity pairs: {positive_similarity_count}")
#     print(f"Total non-positive similarity pairs: {non_positive_similarity_count}")
#     print(f"Total high compatibility pairs (similarity > 0.9): {high_compatibility_count}")

def response_to_vector(response: str) -> int:
    agree_disagree_mapping = {
        "Strongly Agree": 5,
        "Agree": 4,
        "Neutral": 3,
        "Disagree": 2,
        "Strongly Disagree": 1,
    }
    
    # Check if the response is numeric (for the second-to-last question)
    if response.isdigit():
        return int(response)
    
    # Mapping for pickup lines to numeric values, if you wish to differentiate them
    pickup_line_mapping = {
        "Let's make a quantum system and superpose our states, so we can explore all the possibilities together.": 1,
        "You must be a quantum computer, because you've got my heart solving complex problems at the speed of light.": 2,
        "I'm no Schrödinger's cat, but you make me feel alive and dead at the same time with those looks.": 3,
        "Do you believe in quantum teleportation? Because I see us moving from here to a more intimate setting instantaneously.": 4,
        "In a world of classical paths, you're the quantum tunnel to my heart, breaking all barriers of probability.": 5,
    }
    
    normalized_response = response.strip()  # Remove leading/trailing whitespace

    # Attempt to match the normalized response with Agree/Disagree format
    if normalized_response in agree_disagree_mapping:
        return agree_disagree_mapping[normalized_response]
    
    # Handle pickup lines
    for line in pickup_line_mapping:
        if normalized_response[1:-1].lower() == line.lower():  # Case-insensitive comparison
            return pickup_line_mapping[line]
    
    # Default case for unexpected inputs
    return 0


if __name__ == "__main__":
    filename = "./data/9_19_responses.csv"
    # all_groups = load_csv_and_group_by_age_preference_and_email(filename)
    participants = load_participants(filename)
    calculate_and_print_similarities(participants)

    # # Iterate through each group to calculate pairwise similarity scores
    # for domain, age_groups in all_groups.items():
    #     print(f"\nDomain: {domain}")
    #     for age_range, members in age_groups.items():
    #         print(f"\nAge Range {age_range}: Calculating pairwise similarities among {len(members)} members.")
    #         for i in range(len(members)):
    #             for j in range(i + 1, len(members)):  # Ensure we don't compare a person with themselves or repeat pairings
    #                 person_a = members[i]
    #                 person_b = members[j]
    #                 # Calculate similarity score
    #                 score = normalized_similarity(person_a, person_b)
    #                 print(f"Similarity between {person_a['Email']} and {person_b['Email']}: {score}")
