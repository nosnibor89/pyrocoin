class Vehicle:
    max_speed = 300

    def __init__(self, starting_speed=100):
        self.top_speed = starting_speed
        self.__warnings = []

    # def __str__(self):
    #     return str(f'I\'m a car with top speed of {self.top_speed}')

    def __repr__(self):
        return str(f'I\'m a car with top speed of {self.top_speed} and {len(self.__warnings)} warnings')

    def add_warning(self, text):
        if len(text) > 0:
            self.__warnings.append(text)

    def get_warnings(self):
            return self.__warnings

    def drive(self):
        print(f'I am driving at {self.top_speed}')

    def accelerate(self, speed):
        if speed < self.max_speed:
            self.top_speed=speed
            print(f'I acelerating to {self.top_speed}')
