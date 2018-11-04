import random
import datetime

my_random_1 = random.uniform(0,1)

my_random_10 = random.uniform(0,10)

print(my_random_1)
print(my_random_10)

my_date = datetime.date(2018, 11, int(my_random_10))

print(my_date)