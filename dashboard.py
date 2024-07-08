import cv2
from cores_bgr import CoresBGR

class Dashboard: 

    @staticmethod 
    def show(mensagem,frame):
        cor = CoresBGR.BRANCO
        match(mensagem):
            case "Mudanca de faixa":
                cor = CoresBGR.VERMELHO
            case "Dentro das faixas":
                cor = CoresBGR.VERDE
            case "Indefinido":
                cor = CoresBGR.LARANJA
            case _:
                cor = CoresBGR.BRANCO
  
        cv2.putText(frame, mensagem, (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, cor, 2)

    @staticmethod
    def lineDashBoardColor(frame, info_lines):
        match(info_lines):
            case "left and right":
                right_color = left_color = CoresBGR.VERDE
            case "left":
                left_color = CoresBGR.VERDE
                right_color = CoresBGR.CINZA
            case "right":
                left_color = CoresBGR.CINZA
                right_color = CoresBGR.VERDE
            case _:
                right_color = left_color = CoresBGR.CINZA
            
        #desenhar uma reta na imagem
        cv2.line(frame, pt1=(100,80), pt2=(100,160), color=left_color, thickness=10)
        cv2.line(frame, pt1=(120,80), pt2=(120,160), color=right_color, thickness=10)
