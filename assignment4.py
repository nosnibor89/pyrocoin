def operate(f, *numbers):
    for number in numbers:
        result = f'For {number} the result is: {f(number)}'
        print(result)


operate(lambda x: x + 2, 2, 3, 4)
print('New Operation')
operate(lambda x: x - 2, 2, 3, 4)
