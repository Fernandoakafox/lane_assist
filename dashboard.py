import cv2

class Dashboard:  
    def show(mensagem,frame):
        cor = (0,0,0)
        match(mensagem):
            case "Mudanca de faixa":
                cor = (0,0,255)   #vermelho
            case "Dentro das faixas":
                cor = (0,255,0)   #verde
            case "Indefinido":
                cor = (0,165,255) #laranja
            case _:
                cor = (0,0,0)

            
        cv2.putText(frame, mensagem, (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, cor, 2)

    #TODO modularizar/encurtar/endireitar
    def lineDashBoardColor(frame, infoLines):
        if infoLines == "left and right":
            cv2.line(frame, pt1=(100,80), pt2=(100,160), color=(0,255,0), thickness=10)
            cv2.line(frame, pt1=(120,80), pt2=(120,160), color=(0,255,0), thickness=10)
                
        elif infoLines == "left":
            #desenhar uma reta na imagem
            cv2.line(frame, pt1=(100,80), pt2=(100,160), color=(0,255,0), thickness=10)
            cv2.line(frame, pt1=(120,80), pt2=(120,160), color=(128,128,128), thickness=10)
        elif infoLines == "right":
            #desenhar uma reta na imagem
            cv2.line(frame, pt1=(100,80), pt2=(100,160), color=(128,128,128), thickness=10)
            cv2.line(frame, pt1=(120,80), pt2=(120,160), color=(0,255,0), thickness=10)
        else:
            cv2.line(frame, pt1=(100,80), pt2=(100,160), color=(128,128,128), thickness=10)
            cv2.line(frame, pt1=(120,80), pt2=(120,160), color=(128,128,128), thickness=10)