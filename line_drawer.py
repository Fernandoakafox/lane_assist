import numpy as np
import cv2
import math


class LineDrawer:
    @staticmethod
    def draw_lines(averaged_lines, frame):
        if averaged_lines is not None and len(averaged_lines) > 0:
            lineImage = LineDrawer._display_lines(frame, averaged_lines)
            #Vamos combinar a imagem que mostra as linhas com a imagem real. Para isso, somamos a imagem real com a imagem preta que possui linhas azuis, deste modo os pixels pretos, que valem zero, não irão modificar a imagem, porém, os pixels azuis, que valem 255, irão modificar a imagem.
            return cv2.addWeighted(frame, 1, lineImage, 1, 1)    
        else:
            return frame
    
    @staticmethod 
    def draw_all_lines(lines, frame):
        if lines is not None and len(lines) > 0:
            lineImage = LineDrawer._display_all_lines(frame, lines)
            #Vamos combinar a imagem que mostra as linhas com a imagem real. Para isso, somamos a imagem real com a imagem preta que possui linhas azuis, deste modo os pixels pretos, que valem zero, não irão modificar a imagem, porém, os pixels azuis, que valem 255, irão modificar a imagem.
            return cv2.addWeighted(frame, 1, lineImage, 1, 1)    
        else:
            return frame

    @staticmethod
    def _display_lines(frame, lines):
        # uma imagem preta, pois é uma matriz de zeros, da mesma resolução que a imagem
        line_image = np.zeros_like(frame)
        #verificamos se a matriz de linhas possui alguma linha
        if lines is not None and len(lines) > 0:
            for line in lines:
                # se a linha não é nula e possui as quatro coordenadas necessarias para traçar uma reta
                if line is not None and len(line[0]) == 4:
                    x1,y1,x2,y2 = line[0]
                    parameters = np.polyfit((x1,x2),(y1,y2), 1)
                    slope = parameters[0]
                    #o coeficiente angular não deve pertencer ao intervalo ]-0.5,0.5[
                    if slope < -0.5 or slope > 0.5:
                        try:
                            #desenhando linhas sobre a imagem preta. As linhas utilizam 2 pontos para serem desenhadas
                            cv2.line(line_image,(x1,y1),(x2,y2), (0,0,255), thickness=10)
                        except:
                            print("Erro display_lines")
        return line_image

    @staticmethod
    def _display_all_lines(frame, lines):
        # uma imagem preta, pois é uma matriz de zeros, da mesma resolução que a imagem
        line_image = np.zeros_like(frame)
        #verificamos se a matriz de linhas possui alguma linha
        if lines is not None and len(lines) > 0:
            for line in lines:
                # se a linha não é nula e possui as quatro coordenadas necessarias para traçar uma reta
                if line is not None and len(line[0]) == 4:
                    x1,y1,x2,y2 = line[0]
                    catetos = pow((x2 - x1), 2) + pow((y2 - y1),2)
                    hipotenusa = math.sqrt(catetos)
                    #se as retas forem maiores que 100 pixels
                    if abs(hipotenusa) > 100:
                        parameters = np.polyfit((x1,x2),(y1,y2), 1)
                        slope = parameters[0]
                        #o coeficiente angular não deve pertencer ao intervalo ]-0.5,0.5[
                        if slope < -0.5 or slope > 0.5:
                            try:
                                #desenhando linhas sobre a imagem preta. As linhas utilizam 2 pontos para serem desenhadas
                                cv2.line(line_image,(x1,y1),(x2,y2), (0,0,255), thickness=10)
                            except:
                                print("Erro display_lines")
        return line_image
    
    