from processamento_de_imagem import PreProcessadorDeImagem
import cv2
import numpy as np
from relatorio.cronometro import *
from estado import Estado
from dashboard import Dashboard
from line_drawer import LineDrawer

class LaneAssist:
    #construtor para arquivos vídeos (da para fazer uma sobrecarga para webcam)
    def __init__(self,videoPath):
        self.capture = cv2.VideoCapture(videoPath)                    #objeto para ler os frames do vídeo
        self.heigh = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)) #altura do video
        self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))  #largura do video

    def sentinel_mode(self):
        """Gera notificações caso o veículo esteja fora das faixas"""
        while(True):
            # lê um frame do video. Retorna True se a leitura foi bem sucedida e retorna também o frame
            ret, frame = self.capture.read()
            if ret is False:
                break

            lines = self.line_detection(frame)
            if lines is not None:
                infoLines, averagedLines = self.averageSlopeIntercept(frame, lines)

                if infoLines is not "nothing":
                    if self.verificaMudancaDeFaixa(infoLines, averagedLines):  
                        Cronometro.tick(Estado.FORA)
                    else:
                        Cronometro.tick(Estado.NA_FAIXA)
                else:
                    Cronometro.tick(Estado.DESCONHECIDO)

    def graphical_mode(self):
        while(True):
            # lê um frame do video. Retorna True se a leitura foi bem sucedida e retorna também o frame
            ret, frame = self.capture.read()
            if ret is False:
                break

            lines = self.line_detection(frame)
            if lines is not None:
                infoLines, averaged_lines = self.averageSlopeIntercept(frame, lines)

                ret = self.verificaMudancaDeFaixa(infoLines, averaged_lines)
                #se não houver faixas
                if infoLines is "nothing":
                    Cronometro.tick(Estado.DESCONHECIDO)
                    Dashboard.show("Indefinido",frame)
                #se houver faixas e estiver mudando de faixa
                elif ret:
                    Cronometro.tick(Estado.FORA)
                    Dashboard.show("Mudanca de faixa",frame)
                #se não houver faixas e estiver mudando de faixa    
                elif not ret:
                    Cronometro.tick(Estado.NA_FAIXA)
                    Dashboard.show("Dentro das faixas",frame)
            
                #desenhando estado da identificação de linhas, no dashboard
                Dashboard.lineDashBoardColor(frame, infoLines)
                #desenhando linhas sobre a imagem original
                combo_image = LineDrawer.draw_lines(averaged_lines, frame)
        
                #se linhas não foram identificadas

            else:
                cv2.putText(frame, "Indefinido", (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,165,255), 2)
                #pinta linhas no dashboard
                Dashboard.lineDashBoardColor(frame, "")
                combo_image = frame
            
            cv2.imshow("Imagem final", combo_image)

            #interrompe loop se a tecla esc for pressionada
            if cv2.waitKey(40) == 27:
                break

                # Libera o vídeo e fecha as janelas
        self.capture.release()
        cv2.destroyAllWindows()
     
    @staticmethod
    def verificaMudancaDeFaixa(infoLines, averagedLines):
        if infoLines == "left and right":
            faixaEsquerda, faixaDireita = averagedLines
            x1Esquerda,_,_,_ = faixaEsquerda
            x1Direita,_,_,_ = faixaDireita
            if (x1Esquerda < 40 or x1Esquerda > 560) and (x1Direita < 1480 or x1Direita > 1920):
                #print(f"X1 esquerda: {x1Esquerda} , X1 direita: {x1Direita}") #Debug
                return True
        elif infoLines == "left":
            x1Esquerda,_,_,_ = averagedLines[0]
            if x1Esquerda < 40 or x1Esquerda > 560:
                #print(f"X1 esquerda: {x1Esquerda}") #Debug
                return True
        elif infoLines == "right":
            x1Direita,_,_,_ = averagedLines[0]
            if x1Direita < 1480 or x1Direita > 1920:
                #print(f"X1 esquerda: {x1Direita}") #Debug
                return True
        return False

    def makeCoordinates(self, image, lineParameters):
        """Cria uma reta com base em parametros recebidos.
        
        Argumentos:
        - image (ndimensional array): A imagem original.
        - lineParameters (list): lista contendo coeficiente angular e coeficiente linear
        
        """
        slope, intercept = lineParameters
        #definindo a coordenada y do ponto inicial da reta, com base na coordenada da base da imagem
        y1 = image.shape[0]
        #definindo a coordenada y do ponto final da reta
        y2 = int(y1*(4/5))
        x1 = int((y1 - intercept)/slope)
        x2 = int((y2 - intercept)/slope)
        return np.array([x1,y1,x2,y2])

    def averageSlopeIntercept(self, image, lines):
        """Retorna uma tupla, onde o primeiro elemento é uma string e o segundo elemento é um np array
        
        A string contem a informação do np array, avisando se o np array retornado contém as duas faixas, somente a da esquerda, somente a da direita ou nenhuma.

        """
        # linha da esquerda
        leftFit = []
        # linha da direita
        rightFit = []
        for line in lines:
            x1,y1,x2,y2 = line.reshape(4)
            parameters = np.polyfit((x1,x2),(y1,y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            # se o coeficiente angular da reta/linha for negativo, então é uma linha da esquerda (lembre-se que neste plano carteziano o eixo y tem seu valor minimo no extremo e seu valor maximo proximo a onde o eixo x tem valor 0)

            if slope < -0.5:
                #print("--------------------------")
                #print(f"x1: {x1}, y1: {y1} x2: {x2} y2: {y2}")
                #print("{:.2f}".format(slope))
                leftFit.append((slope, intercept))
            elif slope > 0.5:
                #print("--------------------------")
                #print(f"x1: {x1}, y1: {y1} x2: {x2} y2: {y2}")
                #print("{:.2f}".format(slope))
                rightFit.append((slope, intercept))


        leftLine = None
        rightLine = None

        #se existir coordenadas para a linha esquerda
        if leftFit:
            leftFitAverage = np.average(leftFit, axis = 0)
            leftLine = self.makeCoordinates(image, leftFitAverage)

        #se existir coordenadas para a linha direita
        if rightFit:
            rightFitAverage = np.average(rightFit, axis = 0)
            rightLine = self.makeCoordinates(image, rightFitAverage)
        
        #retorna as coordenadas das linhas, se elas existirem, do contrario, retorna coordenadas nulas.
        if leftLine is not None and rightLine is not None:
            return ("left and right",np.array([leftLine, rightLine]))
        elif leftLine is not None:
            return ("left", np.array([leftLine]))
        elif rightLine is not None:
            return ("right", np.array([rightLine]))
        else:
            return ("nothing",np.array([]))
                

    def debug_mode():
        pass

 

    @staticmethod
    def line_detection(frame):
        """Detecta linhas em um frame"""
        #aplicando filtros sobre o frame
        frame_filtered = PreProcessadorDeImagem.aplicar_filtros(frame)
        #cropando a area de interesse do frame
        cropped_frame = PreProcessadorDeImagem.cropp_image(frame_filtered)
        #detectando linhas
        lines = cv2.HoughLinesP(cropped_frame, 2, np.pi/180, 100, np.array([]),minLineLength=40, 
        maxLineGap = 5) #maxLineGap representa o espaço entre linhas que posso considerar como se fosse linha.

        return lines


    def line_drawer():
        pass

    def dashboard():
        pass
