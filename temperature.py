import traceback


class Temperature:
    def __init__(self, temperature=0):
        self._temperature = temperature

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if value < -273:
            traceback.print_exc("Temperature below 273 is not possible")
        self._temperature = value


main = Temperature()
print(main.temperature)
main.temperature = 37
print(main.temperature)

print(main.__dict__)
# main.temperature = -370
# print(main.temperature)
