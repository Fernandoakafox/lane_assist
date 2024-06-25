from estado import Estado

class Cronometro:
    TIME_LINE = []

    @staticmethod
    def tick(estado):
        Cronometro.TIME_LINE.append(estado)
