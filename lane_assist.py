from processamento_de_imagem import PreProcessadorDeImagem
import cv2
import numpy as np
from relatorio.cronometro import *
from estado import Estado
from dashboard import Dashboard
from line_drawer import LineDrawer
from time import time
from relatorio.relatorio import Relatorio
from relatorio.exporter import CSVExporter
import math

class LaneAssist:
    #construtor para arquivos vídeos (da para fazer uma sobrecarga para webcam)
    def __init__(self, videoPath, car_atributes):
        self.capture = cv2.VideoCapture(videoPath) #objeto para ler os frames do vídeo
        self.car_atributes = car_atributes
        
    def sentinel_mode(self):
        """Este método é responsavel por aplicar filtros, detectar linhas, gerar notificações e gerar um relatorio sobre a permanencia do veículo entre faixas."""
        if not self.capture.isOpened():
            print("Erro ao abrir o arquivo de vídeo")
            return

        while(True):
            start_time = time()
            # lê um frame do video. Retorna True se a leitura foi bem sucedida e retorna também o frame
            ret, frame = self.capture.read()
            if ret is False:
                break

            lines = self.line_detection(frame)
            if lines is not None:
                infoLines, averagedLines = self.average_slope_intercept(frame, lines)

                if infoLines != "nothing":
                    if self.verifica_mudanca_deFaixa(infoLines, averagedLines):  
                        Cronometro.tick(Estado.FORA)
                    else:
                        Cronometro.tick(Estado.NA_FAIXA)
                else:
                    Cronometro.tick(Estado.DESCONHECIDO)

            end_time = time()
            print(end_time - start_time)

    def graphical_mode(self):
        """Este método é responsavel por aplicar filtros, detectar linhas e printar a imagem contendo um dashboard e as linhas identificadas na entrada de vídeo do objeto. Utilize este método para fins de debug."""
        if not self.capture.isOpened():
            print("Erro ao abrir o arquivo de vídeo")
            return

        while(True):
            start_time = time()
            # lê um frame do video. Retorna True se a leitura foi bem sucedida e retorna também o frame
            ret, frame = self.capture.read()
            if ret is False:
                break

            lines = self.line_detection(frame)
            if lines is not None:
                infoLines, averaged_lines = self.average_slope_intercept(frame, lines)

                ret = self.verifica_mudanca_deFaixa(infoLines, averaged_lines)
                #se não houver faixas
                if infoLines == "nothing":
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
            
                #desenhando, no dashboard, o estado da identificação de linhas
                Dashboard.lineDashBoardColor(frame, infoLines)
                #desenhando linhas sobre a imagem originalf
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
            end_time = time()
            print(end_time - start_time)
        relatorio = Relatorio(Cronometro.TIME_LINE, 15)
        export = CSVExporter(relatorio)
        export.export()
        self.capture.release()
        cv2.destroyAllWindows()
     
    def debug_mode(
        self,
        base_image_output=False,
        cropped_base_image_output=False,
        base_image_filtered_output=False,
        cropped_filtered_image_output=False,
        combo_image_all_lines_output=False,
        combo_image_output=False,
    ):
        """Este método é responsavel por aplicar filtros, detectar linhas e printar imagens de todas as transformações feitas na entrada de vídeo do objeto. Utilize este método para fins de debug."""

        if not self.capture.isOpened():
            print("Erro ao abrir o arquivo de vídeo")
            return
        
        isFirstLoop = 0
        while(True):
            start_time = time()
            # lê um frame do video. Retorna True se a leitura foi bem sucedida e retorna também o frame
            ret, frame = self.capture.read()
            if ret is False:
                print("Não foi possível ler o frame do vídeo ou fim do vídeo")
                break

            copy_frame = np.copy(frame)
            #cropando a area de interesse sobre o frame original
            cropped_base_image = PreProcessadorDeImagem.cropp_image(copy_frame, self.car_atributes)
            #aplicando filtros sobre o frame
            frame_filtered = PreProcessadorDeImagem.aplicar_filtros(copy_frame)
            #cropando a area de interesse sobre frame filtrado
            cropped_frame = PreProcessadorDeImagem.cropp_image(frame_filtered, self.car_atributes)
            #detectando linhas
            lines = cv2.HoughLinesP(cropped_frame, 2, np.pi/180, 100, np.array([]),minLineLength=40, 
            maxLineGap = 5) #maxLineGap representa o espaço entre linhas que posso considerar como se fosse linha.

            if lines is not None:
                infoLines, averaged_lines = self.average_slope_intercept(copy_frame, lines, self.car_atributes)

                #VER ESSA LINHA ABAIXO
                #if self.faixas_dentro_do_intervalo(infoLines,averaged_lines) == True:

                ret = self.verifica_mudanca_deFaixa(infoLines, averaged_lines)
                #se não houver faixas
                if infoLines == "nothing":
                    Cronometro.tick(Estado.DESCONHECIDO)
                    Dashboard.show("Indefinido",copy_frame)
                #se houver faixas e estiver mudando de faixa
                elif ret:
                    Cronometro.tick(Estado.FORA)
                    Dashboard.show("Mudanca de faixa",copy_frame)
                #se não houver faixas e estiver mudando de faixa    
                elif not ret:
                    Cronometro.tick(Estado.NA_FAIXA)
                    Dashboard.show("Dentro das faixas",copy_frame)
            
                #desenhando, no dashboard, o estado da identificação de linhas
                Dashboard.lineDashBoardColor(copy_frame, infoLines)
                #desenhando linhas sobre a imagem original
                combo_image = LineDrawer.draw_lines(averaged_lines, copy_frame)
                all_lines = LineDrawer.draw_all_lines(lines, copy_frame)
        
            #se as linhas não foram identificadas
            else:
                cv2.putText(copy_frame, "Indefinido", (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,165,255), 2)
                #pinta linhas no dashboard
                Dashboard.lineDashBoardColor(copy_frame, "")
                combo_image = copy_frame
                all_lines = copy_frame
            
            lista_de_imagens = []

            try:
                if base_image_output == True:
                    lista_de_imagens.append(frame)
                if base_image_filtered_output == True:
                    lista_de_imagens.append(frame_filtered)
                if cropped_filtered_image_output == True:
                    lista_de_imagens.append(cropped_frame)
                if combo_image_output == True:
                    lista_de_imagens.append(combo_image)
                if cropped_base_image_output == True:
                    lista_de_imagens.append(cropped_base_image)
                if combo_image_all_lines_output == True:
                    lista_de_imagens.append(all_lines)
            except:
                print("Erro ou adicionar as imagens para a lista")

            #mostra as imagens
            self.show_multiple_images(lista_de_imagens,isFirstLoop)
            isFirstLoop = 1
            #interrompe loop se a tecla esc for pressionada
            if cv2.waitKey(40) == 27:
                break

            end_time = time()
            #print(end_time - start_time)
           
        self.capture.release()
        cv2.destroyAllWindows()


#------------------------------manipulação da imagem-------------------------------
    #TODO botar essa função na classe ProcesadorDeImagem (modificar o move window para ele se adaptar ao numero de janelas e ao tamanho do monitor do usuario, o tamanho das telas também pode ser proporcional ao numero de telas e ao monitor do usuario)
    @staticmethod
    def show_multiple_images(lista_de_imagens,isFirstLoop):
        """Recebe uma lista de imagens, printa as imagens na tela."""
        for i,image in enumerate(lista_de_imagens):
            cv2.imshow(f"image {i}", PreProcessadorDeImagem.image_recizer(image))
        if isFirstLoop == 0:
            cv2.moveWindow('image 0', 50, 50)  # Posição (50, 50)
            cv2.moveWindow('image 1', 800, 50)  # Posição (400, 50)
            cv2.moveWindow('image 2', 50, 700)  # Posição (50, 50)
            cv2.moveWindow('image 3', 800, 700)  # Posição (400, 50)
            cv2.moveWindow('image 4', 800, 700)  # Posição (400, 50)

#----------------m------------------------------------------------------------------

    def verifica_mudanca_deFaixa(self, infoLines, averagedLines):
        """Verifica se o veículo esta mudando de faixas"""
        atributes = self.car_atributes

        min_esquerda = atributes.limite_min_x1_esquerda
        max_esquerda = atributes.limite_max_x1_esquerda

        min_direita = atributes.limite_min_x1_direita
        max_direita = atributes.limite_max_x1_direita
        
        if infoLines == "left and right":
            faixaEsquerda, faixaDireita = averagedLines[0][0], averagedLines[1][0]
            x1Esquerda,_,_,_ = faixaEsquerda
            x1Direita,_,_,_ = faixaDireita
            if (x1Esquerda < min_esquerda or x1Esquerda > max_esquerda) and (x1Direita < min_direita or x1Direita > max_direita):
                #print(f"X1 esquerda: {x1Esquerda} , X1 direita: {x1Direita}") #Debug
                return True
        elif infoLines == "left":
            x1Esquerda,_,_,_ = averagedLines[0][0]
            if x1Esquerda < min_esquerda or x1Esquerda > max_esquerda:
                #print(f"X1 esquerda: {x1Esquerda}") #Debug
                return True
        elif infoLines == "right":
            x1Direita,_,_,_ = averagedLines[0][0]
            if x1Direita < min_direita or x1Direita > max_direita:
                #print(f"X1 esquerda: {x1Direita}") #Debug
                return True
        return False

    def make_coordinates(self, image, lineParameters):
        """Recebe uma image, coeficiente linear e angular referente a uma reta, retorna as coordenadas de dois pontos para que seja desenhada uma reta com estes pontos. O tamanho desta reta leva em consideração as dimensoes da imagem recebida.
        
        Argumentos:
        - image (ndimensional array): A imagem original.
        - lineParameters (list): lista contendo coeficiente angular e coeficiente linear
        
        Retorno:
        - np.array: contendo coordenadas 

        """
        slope, intercept = lineParameters
        #definindo a coordenada y do ponto inicial da reta, com base na coordenada da base da imagem
        y1 = image.shape[0]
        #definindo a coordenada y do ponto final da reta
        y2 = int(y1*(3/5))
        x1 = int((y1 - intercept)/slope)
        x2 = int((y2 - intercept)/slope)
        return np.array([x1,y1,x2,y2])

    def average_slope_intercept(self, image, lines, car_atributes):
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
            catetos = pow((x2 - x1), 2) + pow((y2 - y1),2)
            hipotenusa = math.sqrt(catetos)

            #se as retas forem maiores que 70 pixels
            if abs(hipotenusa) > 100:
                # se o coeficiente angular da reta/linha for negativo, então é uma linha da esquerda (lembre-se que neste plano carteziano o eixo y tem seu valor minimo no extremo e seu valor maximo proximo a onde o eixo x tem valor 0)
                if slope < -0.5:
                    #print("--------------------------")
                    #print(f"x1: {x1}, y1: {y1} x2: {x2} y2: {y2}")
                    #print("slope {:.2f}".format(slope))
                    leftFit.append((slope, intercept))
                elif slope > 0.5:
                    #print("--------------------------")
                    #print(f"x1: {x1}, y1: {y1} x2: {x2} y2: {y2}")
                    #print("slope {:.2f}".format(slope))
                    rightFit.append((slope, intercept))


        leftLine = None
        rightLine = None

        #se existir coordenadas para a linha esquerda
        if leftFit:
            leftFitAverage = np.average(leftFit, axis = 0)
            leftLine = self.make_coordinates(image, leftFitAverage)

        #se existir coordenadas para a linha direita
        if rightFit:
            rightFitAverage = np.average(rightFit, axis = 0)
            rightLine = self.make_coordinates(image, rightFitAverage)        
              
        #retorna as coordenadas das linhas, se elas existirem, do contrario, retorna coordenadas nulas.
        if leftLine is not None and rightLine is not None:
            #calculando um ponto medio na reta da direita
            x1,_,x2,_ = rightLine
            medium_point_right_line = ((x2 - x1) /2)
            #calculando um ponto medio na reta da esquerda
            x1,_,x2,_ = leftLine
            medium_point_left_line = ((x2 - x1) /2)
            
            #se as retas tiverem um espaçamento minimo de pixels entre elas
            if abs(medium_point_right_line - medium_point_left_line) > car_atributes.limite_min_entre_faixas:
                print(medium_point_right_line - medium_point_left_line)                
                return ("left and right",np.array([[leftLine], [rightLine]]))
            else:
                return ("nothing",None)
        elif leftLine is not None:
            return ("left", np.array([[leftLine]]))
        elif rightLine is not None:
            return ("right", np.array([[rightLine]]))
        else:
            return ("nothing",None)

    def line_detection(self, frame):
        """Recebe um frame e retorna uma lista contendo as coordenadas das linhas deste frame"""
        #aplicando filtros sobre o frame
        frame_filtered = PreProcessadorDeImagem.aplicar_filtros(frame)
        #cropando a area de interesse do frame
        cropped_frame = PreProcessadorDeImagem.cropp_image(frame_filtered, self.car_atributes)
        #detectando linhas
        lines = cv2.HoughLinesP(cropped_frame, 2, np.pi/180, 100, np.array([]),minLineLength=40, 
        maxLineGap = 5) #maxLineGap representa o espaço entre linhas que posso considerar como se fosse linha.
        return lines     

