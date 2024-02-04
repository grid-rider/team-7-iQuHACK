# @Author: Armin Ulrich

from Matcher import Matcher
import csv 

responses = {}
with open('./backend/data/responses.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['nickname'], row['Email'])
# Matcher()

