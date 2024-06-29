from enum import Enum

class PointsHB20(Enum):
    BASE_ESQUERDA = (570,880)
    BASE_DIREITA = (1350,880)
    TOPO_ESQUERDA = (770,750)
    TOPO_DIREITA = (1150,750)

    def coordenadas(self):
        return self.value