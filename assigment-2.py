# names = ['Robinson', 'Isamar', 'Joel', 'Ilse', 'Ramses']

# while len(names) > 0:
#     print('Printing the length of each name')
#     for name in names:
#         if len(name) > 5:
#             print('{name} - {length}'.format(name=name, length=len(name)))

#         if 'n' in name.lower():
#             print('{name} has letter n'.format(name=name))

#     names.pop()


class Dock:
    def talk(self):
        print('I\'m a duck')

class Dog:
    def talk(self):
        print('I\'m a dog')


def speak(animal):
    animal.talk()


speak(Dock())
speak(Dog())