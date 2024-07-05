from lane_assist import LaneAssist
from line_drawer import LineDrawer
from processamento_de_imagem import PreProcessadorDeImagem
import cv2
import numpy as np

image_path = "./screenshots/base_image.png"
image = cv2.imread(image_path)
#aplicando filtros sobre o frame
frame_filtered = PreProcessadorDeImagem.aplicar_filtros(image)
#descobrindo linhas
lines = cv2.HoughLinesP(frame_filtered, 2, np.pi/180, 100, np.array([]),minLineLength=40, 
maxLineGap = 5) #maxLineGap representa o espaço entre linhas que posso considerar como se fosse linha.
#pintando linhas sobre a imagem original
combo_image = LineDrawer.draw_all_lines(lines, image)
cv2.imshow("combo_image",combo_image)
#fecha imagem quando clioca no x
cv2.waitKey(0)