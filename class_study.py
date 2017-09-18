import random as r


class Fish(object):
    def __init__(self):
        self.x = r.randint(0, 10)
        self.y = r.randint(0, 10)

    def move(self):
        self.x -= 1
        print "My location is at :", self.x, self.y


class GoldFish(Fish):
    pass


class Crap(Fish):
    pass


class Salmon(Fish):
    pass


class Shark(Fish):
    def __init__(self):
        super(Shark, self).__init__()
        self.hungry = True

    def eat(self):
        if self.hungry == True:
            print "I'm hungry, i want eat something ..."
            self.hungry = False
        else:
            print "haha, i'm full ..."


shark = Shark()
shark.eat()
shark.move()
