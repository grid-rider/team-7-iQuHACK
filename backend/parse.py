# import csv
# from typing import List, Dict, Tuple

# def parse_age_range(age_range: str) -> Tuple[int, int]:
#     """Parses the age preference range from a string format to a tuple of integers."""
#     try:
#         start, end = age_range.split('-')
#         return int(start), int(end)
#     except ValueError:
#         print(f"Invalid age range: {age_range}")
#         return (0, 0)

# def check_age_match(person_age: int, target_range: str) -> bool:
#     """Checks if a person's age falls within a given age range string."""
#     start, end = parse_age_range(target_range)
#     return start <= person_age <= end

# def group_by_email_domain(person: Dict) -> str:
#     """Determines the group key based on email domain."""
#     if person["Email"].endswith("@mit.edu"):
#         return "mit"
#     else:
#         return "external"

# def load_csv_and_group_by_age_preference_and_email(filename: str) -> Dict[str, Dict[str, List[Dict]]]:
#     """Loads CSV data and groups people by age preferences and email domains."""
#     groups = {"mit": {}, "external": {}}
#     with open(filename, mode='r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             person = {
#                 "Nickname": row["nickname"],
#                 "Email": row["Email"],
#                 "Gender": row["Gender"],
#                 "Gender Preference": row["Gender Preference"],
#                 "Age": int(row["Age"]),
#                 "Age Preference Range": row["Age Preference Range (Format example: 20-23)"],
#                 "Responses": [response_to_vector(row[question]) for question in reader.fieldnames[7:-2]],  # Adjusted for indexing
#             }
#             email_domain_group = group_by_email_domain(person)
#             # Iterate through existing groups within the domain to find a match
#             matched = False
#             for group_key, members in groups[email_domain_group].items():
#                 if check_age_match(person["Age"], group_key) or any(check_age_match(member["Age"], person["Age Preference Range"]) for member in members):
#                     members.append(person)
#                     matched = True
#                     break
#             # If no existing group is a match, create a new one
#             if not matched:
#                 group_key = person["Age Preference Range"]
#                 groups[email_domain_group].setdefault(group_key, []).append(person)
#     return groups

# def response_to_vector(response: str) -> int:
#     """Converts survey responses to a numeric vector."""
#     mapping = {
#         "Strongly Agree": 5,
#         "Agree": 4,
#         "Neutral": 3,
#         "Disagree": 2,
#         "Strongly Disagree": 1,
#     }
#     return mapping.get(response, 0)

# # Example usage
# if __name__ == "__main__":
#     filename = "./data/9_19_responses.csv"
#     all_groups = load_csv_and_group_by_age_preference_and_email(filename)
#     for domain, groups in all_groups.items():
#         print(f"\nDomain: {domain}")
#         for age_range, members in groups.items():
#             member_emails = [member["Email"] for member in members]
#             print(f"Age Range {age_range} has {len(members)} members: {', '.join(member_emails)}")


import csv
from typing import List, Dict, Tuple

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
        for row in reader:
            participants.append({
                "Nickname": row["nickname"],
                "Email": row["Email"],
                "Gender": row["Gender"],
                "Gender Preference": row["Gender Preference"],
                "Age": int(row["Age"]),
                "Age Preference Range": parse_age_range(row["Age Preference Range (Format example: 20-23)"]),
                "Responses": [response_to_vector(row[question]) for question in reader.fieldnames[7:-2]],  # Adjusted for indexing
            })

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
    for domain, age_groups in all_groups.items():
        print(f"\nDomain: {domain}")
        for age_range, members in age_groups.items():
            print(f"Age Range {age_range} has {len(members)} members. Emails: {[member['Email'] for member in members]}")
