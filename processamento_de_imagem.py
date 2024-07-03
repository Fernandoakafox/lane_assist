import cv2
import numpy as np
from enums.pointsForRegionOfInterest import PointsVWSantana

class PreProcessadorDeImagem:
    @staticmethod
    def aplicar_filtros(image):
            """Aplica filtros em uma imagem"""
            h,l,s = cv2.split(cv2.cvtColor(image,cv2.COLOR_BGR2HLS))
            cannyImage = cv2.Canny(l,100, 150)
            return cannyImage
    
    @staticmethod
    def cropp_image(frame):
        """Faz a cropagem da area de interece do frame, com base em pontos predeterminados"""
        verticeBaseEsquerda = PointsVWSantana.BASE_ESQUERDA.coordenadas()
        verticeBaseDireita = PointsVWSantana.BASE_DIREITA.coordenadas()
        verticeTopoEsquerda = PointsVWSantana.TOPO_ESQUERDA.coordenadas()
        verticeTopoDireita = PointsVWSantana.TOPO_DIREITA.coordenadas()
        #definição dos vertices do trapezio. É uma lista porque fillPoly só aceita listas de poligonos.
        vertices = np.array([
        [verticeBaseEsquerda , verticeBaseDireita , verticeTopoDireita ,verticeTopoEsquerda ]
         ])

        mask = np.zeros_like(frame) #criamos um array ndimensional de mesmas proporções que o array image, contendo somente pixels pretos

        cv2.fillPoly(mask, vertices, 255) # estamos aplicando o triangulo na mascara, de modo que o triangulo fique completamente branco.

        masked_frame = cv2.bitwise_and(frame, mask)

        return masked_frame

