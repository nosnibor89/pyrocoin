# def decorator_message(func):
#     def wrapper(message):
#         print(message)
#         func()
#         print('Done')

#     return wrapper


def message(message):
    def decorator_message(func):
        def wrapper():
            print(message)
            func()
            print('Done')

        return wrapper

    return decorator_message


@message('Rob')
def hello():
    print('Helloooo')


hello()
