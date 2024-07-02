from processamento_de_imagem import PreProcessadorDeImagem
import cv2
import numpy as np

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
            if lines:
                pass
                

    def debug_mode():
        pass

    def teste():
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
