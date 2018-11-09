
import pickle

finish = False
data = []


def save_data(text):
    data.append(text)


def save_to_file():
    with open('personal_data.p', mode='wb') as file:
        file.write(pickle.dumps(data))


def read_file():
    with open('personal_data.p', mode='rb') as file:
        global data
        data = pickle.loads(file.read())


read_file()

print('Type any text you want to store.')
print('Press down "Q" and enter if you want to quit')
print('Press down "P" and enter if you want to print the content')
print('Press down "S" and enter if you want to save the content')


while not finish:
    option = input()

    if option.lower() == "q":
        finish = True
    elif option.lower() == "s":
        save_to_file()
    elif option.lower() == "p":
        print(data)
    else:
        save_data(option)
