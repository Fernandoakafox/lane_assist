from enum import Enum ,auto


class Presets(Enum):
    HB20 = 1
    VW_SANTANA = 2

    
class CarAtributes():

    # O preset default do Santana
    def __init__(self, type = Presets.VW_SANTANA):
        
        self.name = type.name

        # janela de interrese do LaneAssist
        self.base_esquerda = (0, 0)
        self.base_direita = (0, 0)
        self.topo_direita = (0, 0)
        self.topo_esquerda = (0, 0)

        # Limites do TODO finalizar descrição
        self.limite_min_x1_esquerda = (0)
        self.limite_max_x1_esquerda = (0)
        self.limite_min_x1_direita = (0)
        self.limite_max_x1_direita = (0)

        self._initialize_atributes(type)


    # Essa função é responsável por iniciar os atributos
    # referentes a janela de interesse dos veículos utilizados nos vídeos
    # esses pontos são a delimitação da visão que a camera deve ter
    # isso é crucial para o correto funcionamento do LaneAssist
    def _initialize_atributes(self, type):
        
        match (type):
            case Presets.HB20:
                self.base_esquerda = (570,880)
                self.base_direita = (1350,880)
                self.topo_esquerda = (770,750)
                self.topo_direita = (1150,750)

                self.limite_min_x1_esquerda = (40)
                self.limite_max_x1_esquerda = (560)
                self.limite_min_x1_direita = (1480)
                self.limite_max_x1_direita = (1920)

            case Presets.VW_SANTANA:
                self.base_esquerda = (0,880)
                self.base_direita = (1920,880)
                self.topo_esquerda = (670,500)
                self.topo_direita = (1250,500)

                self.limite_min_x1_esquerda = (40)
                self.limite_max_x1_esquerda = (560)
                self.limite_min_x1_direita = (1480)
                self.limite_max_x1_direita = (1920)

            # TODO fazer os atributos dos indianCar


    def coordenadas(self):
        return self.value


# TODO remover o código abaixo quando não for mais necessário
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