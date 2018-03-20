import json
from pprint import pprint

data = json.load(open('point_default.json'))

default_points = {}
for from_to in data['poe']:
    default_points[from_to] = [item[2] for item in data['poe'][from_to]['point_cap']]

for city in data['sub_cities']:
    default_points[city] = [item[2] for item in data['sub_cities'][city]['point_cap']]

for city in data['cities']:
    default_points[city] = [item[2] for item in data['cities'][city]['point_cap']]

print(default_points)
for city in default_points:
    pprint(city)
    assert len(default_points[city]) == 96
# print(data['sub_cities']['juarez'])
# print(data['cities']['tucson'])
