def unlimited_arguments(*args, **keyword_args):
    print(args)
    print(keyword_args)



unlimited_arguments(1,2,3)

unlimited_arguments(*[1,2,3])

unlimited_arguments(1,2,3, name="max", age="34")

unlimited_arguments(3,**{'name':"max", 'age':"34", 'hobby': 'swim'})
