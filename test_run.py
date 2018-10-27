def simple_fun():
    ret = 3
    print(ret)
    return ret


class Animal:
    def __init__(self, barksound):
        self.legs = []
        self.barksound = barksound

    def bark(self):
        print(self.barksound)


class leg:
    def __init__(self, length):
        self.length = length


def make_animal():
    return Animal('woof')


def arg_input(animal):
    animal.bark()
    animal.legs.append(leg(1))

if __name__ == "__main__":
    ret = complex_fun()
    print(ret)