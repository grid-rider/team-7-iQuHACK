# @Author: Armin Ulrich

from Matcher import Matcher
import csv 

responses = []
with open('./backend/data/9_19_responses.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        responses.append(row)

matchmaker = Matcher(responses)
matchmaker.findmatches()

