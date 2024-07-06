from enum import Enum

class PointsHB20(Enum):
    BASE_ESQUERDA = (570,880)
    BASE_DIREITA = (1350,880)
    TOPO_ESQUERDA = (770,750)
    TOPO_DIREITA = (1150,750)

    def coordenadas(self):
        return self.value

class PointsVWSantana(Enum):
    BASE_ESQUERDA = (0,880)
    BASE_DIREITA = (1920,880)
    TOPO_ESQUERDA = (670,500)
    TOPO_DIREITA = (1250,500)
    LIMITE_MIN_X1_LEFT = (40)
    LIMITE_MAX_X1_LEFT = (560)
    LIMITE_MIN_X1_RIGHT = (1480)
    LIMITE_MAX_X1_RIGHT = (1920)

    def coordenadas(self):
        return self.value