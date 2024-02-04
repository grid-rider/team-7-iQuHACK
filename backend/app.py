# @Author: Armin Ulrich

from Matcher import Matcher
from parse import response_to_vector, parse_age_range
import csv 

form_submissions = []
with open('./data/9_19_responses.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        domain_group = "mit" if row["Email"].endswith("@mit.edu") else "external"
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


matchmaker = Matcher(form_submissions)
matchmaker.find_matches()

