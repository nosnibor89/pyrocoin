# file = open('demo.html', mode='w')

# content = '''
# <html>
#     <head>Python</head>
#     <body>
#         <h1>Hi from Python!</h1>
#     </body>
# </html>
# '''

# file.write(content)


# file = open('demo.txt', mode='a')
# file.write("Some content\n")


# file = open('demo.txt')

# content = file.read()
# lines = file.readlines()

# file.close()

# print(content)
# print(lines)

# with open('demo.txt') as file:

#     print(file.readlines())

#     line = file.readline()
#     while line:
#         print(line)
#         line = file.readline()

with open('demo.txt', mode='w') as file:

    file.write('Test if closes')

input('Waiting')
print('Done')
