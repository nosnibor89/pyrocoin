import copy

persons = [
    {'name': 'Rob', 'age': 12, 'hobbies': ['gym', 'videogames', 'books']},
    {'name': 'Sam', 'age': 34, 'hobbies': ['sleep', 'eat']},
    {'name': 'Ron', 'age': 24, 'hobbies': ['soccer', 'baseball']},
]

print(persons)

names = [person['name'] for person in persons]

print(names)

all_older_than_twenty = all([person['age'] > 20 for person in persons])

print(all_older_than_twenty)

persons_copy = copy.deepcopy(persons)

persons_copy[0]['name'] = 'Jhon'

print(persons)
print(persons_copy)

rob, sam, ron = persons

print("Rob: ", rob)
print("Ron: ", ron)
print("Sam: ", sam)
