from vehicle import Vehicle

class Car(Vehicle):
    def brag(self):
        print('look my car')


car = Car()
car2 = Car(250)

# Car.max_speed = 1000

# car.drive()

# car.accelerate(200)
# car2.drive()

# print(car.max_speed)
# print(car2.max_speed)

# print(car)
# print(car.__dict__)

# car.__warnings.append("Baddd")

car.add_warning('Good')
car.add_warning('Good 2')

print(car)
print(car.get_warnings())
