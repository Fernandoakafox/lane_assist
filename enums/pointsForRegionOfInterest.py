from enum import Enum

class PointsHB20(Enum):
    BASE_ESQUERDA = (570,880)
    BASE_DIREITA = (1350,880)
    TOPO_ESQUERDA = (770,750)
    TOPO_DIREITA = (1150,750)

    def coordenadas(self):
        return self.value

class PointsVWSantana(Enum):
    BASE_ESQUERDA = (150,880)
    BASE_DIREITA = (1800,880)
    TOPO_ESQUERDA = (670,600)
    TOPO_DIREITA = (1250,600)

    def coordenadas(self):
        return self.value