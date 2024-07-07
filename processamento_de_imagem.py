import cv2
import numpy as np
from matplotlib import pyplot as plt

class PreProcessadorDeImagem:
    @staticmethod
    def aplicar_filtros(image):
            """Aplica filtros em uma imagem"""
            h,l,s = cv2.split(cv2.cvtColor(image,cv2.COLOR_BGR2HLS))
            cannyImage = cv2.Canny(l,100, 150)
            return cannyImage
    
    @staticmethod
    def cropp_image(frame, car_atributes):
        """Faz a cropagem da area de interece do frame, com base em pontos predeterminados"""
        verticeBaseEsquerda = car_atributes.base_esquerda
        verticeBaseDireita = car_atributes.base_direita
        verticeTopoEsquerda = car_atributes.topo_esquerda
        verticeTopoDireita = car_atributes.topo_direita
        #definição dos vertices do trapezio. É uma lista porque fillPoly só aceita listas de poligonos.
        vertices = np.array([
        [verticeBaseEsquerda , verticeBaseDireita , verticeTopoDireita ,verticeTopoEsquerda ]
         ])

        mask = np.zeros_like(frame) #criamos um array ndimensional de mesmas proporções que o array image, contendo somente pixels pretos

        cv2.fillPoly(mask, vertices, 255) # estamos aplicando o triangulo na mascara, de modo que o triangulo fique completamente branco.

        masked_frame = cv2.bitwise_and(frame, mask)

        return masked_frame
    
    @staticmethod
    def image_recizer(image):
        """Função para redimensionar uma imagem mantendo a proporção"""
        proporcao = 720 / image.shape[1]
        altura_desejada = int(image.shape[0] * proporcao)
        return cv2.resize(image, (720, altura_desejada))
    
    @staticmethod
    def getVideoCartezianDimension(imagem):
        """Recebe um frame, no formato ndimensional array. Printa a imagem em um plano cartesiano"""
        plt.imshow(imagem)
        plt.show()


