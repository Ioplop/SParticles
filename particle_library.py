import json

with open('particles.json', 'r') as file:
    data = json.load(file)

print(data)