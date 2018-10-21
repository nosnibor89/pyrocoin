# Lists
simple_list = [1,2,3, 4]
simple_list.append([5,6])
simple_list.extend([7,8])

print(simple_list)

del simple_list[-1]

print(simple_list)

# Dictionaries
my_dic = { 'name' : 'Choco', 'size': 'big'}

for k,v in my_dic.items():
    print(k + ' - ' + v)

del my_dic['name']

print(my_dic)

# Tuples
my_tuple = (1,2,3,'bad')

# del my_tuple[1] Can't
print(my_tuple.index(2))

# Sets
s = {'Isa', 'Rob', 'Toy'}

# del s['Isa'] Can't
s.remove('Toy')
print(s)

