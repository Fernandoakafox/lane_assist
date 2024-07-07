from enum import Enum

class Presets(Enum):
    HB20 = 1
    VW_SANTANA = 2
    INDIAN_CAR = 3
    
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

            case Presets.INDIAN_CAR:
                self.base_esquerda = (250,1080)
                self.base_direita = (1920,1080)
                self.topo_esquerda = (750,500)
                self.topo_direita = (1000,500)

                self.limite_min_x1_esquerda = (40)
                self.limite_max_x1_esquerda = (560)
                self.limite_min_x1_direita = (1480)
                self.limite_max_x1_direita = (1920)
