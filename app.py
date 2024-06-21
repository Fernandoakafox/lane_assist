import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

def get_video_cartezian_dimension(imagem):
    """Recebe um frame, no formato ndimensional array. Printa a imagem em um plano cartesiano"""
    plt.imshow(imagem)
    plt.show()

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    #pegando a base da imagem
    y1 = image.shape[0]
    #pegando o "meio" da imagem
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1,y1,x2,y2])

def average_slope_intercept(image, lines):
    # linha da esquerda
    left_fit = []
    # linha da direita
    right_fit = []
    for line in lines:
        x1,y1,x2,y2 = line.reshape(4)
        parameters = np.polyfit((x1,x2),(y1,y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        # se o coeficiente angular da reta/linha for negativo, então é uma linha da esquerda (lembre-se que neste plano carteziano o eixo y tem seu valor minimo no extremo e seu valor maximo proximo a onde o eixo x tem valor 0)
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    #calculando a media das linhas
    left_fit_average = np.average(left_fit, axis = 0)
    right_fit_average = np.average(right_fit, axis = 0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])


def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    low_threshold = 50
    high_threshold = 150
    canny = cv2.Canny(blur, low_threshold, high_threshold)
    return canny

def display_lines(image, lines):
    # uma imagem preta, pois é uma matriz de zeros, da mesma resolução que a imagem
    line_image = np.zeros_like(image)
    #verificamos se a matriz de linhas possui alguma linha
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line.reshape(4)
            #desenhando linhas sobre a imagem preta. As linhas utilizam 2 pontos para serem desenhadas
            cv2.line(line_image,(x1,y1),(x2,y2), (0,0,255), thickness=10)
    return line_image

def plotCannyGraphic(canny):
    """Sempre que quiser desenhar o tringulo, é necessario abrir a imagem com o matplotlib para ver as coordenadas dos pontos do triangulo na imagem."""
    plt.imshow(canny)
    plt.show()

def region_of_interest(image):
    alturaDaImagem = image.shape[0] #o parametro 0 do metodo shape, retorna o numero de linhas.
    verticeBaseEsquerdaTriangulo = (300,alturaDaImagem)
    verticeBaseDireitaTriangulo = (1700,alturaDaImagem)
    verticeTopoTriangulo = (1154,598)

    #definição dos vertices do triangulo. É uma lista porque fillPoly só aceita listas de poligonos.
    polygons = np.array([
        [(verticeBaseEsquerdaTriangulo) , (verticeBaseDireitaTriangulo) , (verticeTopoTriangulo)]
         ])

    mask = np.zeros_like(image) #criamos um array ndimensional de mesmas proporções que o array image, contendo somente pixels pretos

    cv2.fillPoly(mask, polygons, 255) # estamos aplicando o triangulo na mascara, de modo que o triangulo fique completamente branco.

    masked_image = cv2.bitwise_and(image, mask)

    return masked_image



videoPath = "./videos/test_countryroad.mp4"
capture = cv2.VideoCapture(videoPath)

# lê um frame do video. Retorna o True se a leitura foi bem sucedida e retorna também o frame
ret, image = capture.read()

while capture.isOpened():
    cv2.imshow("Original",image)
    lane_image = np.copy(image)
    canny_image = canny(lane_image)
    cropped_image = region_of_interest(canny_image)
    cv2.imshow("Cropped_image", cropped_image)
    #detectando linhas
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]),minLineLength=40, 
    maxLineGap = 5) #maxLineGap representa o espaço entre linhas que posso considerar como se fosse linha.
    averaged_lines = average_slope_intercept(lane_image, lines)
    #line_image = display_lines(lane_image, lines)
    line_image = display_lines(lane_image, averaged_lines)
    #Vamos combinar a imagem que mostra as linhas com a imagem real. Para isso, somamos a imagem real com a imagem preta que possui linhas azuis, deste modo os pixels pretos, que valem zero, não irão modificar a imagem, porém, os pixels azuis, que valem 255, irão modificar a imagem.
    combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
    cv2.imshow("Canny", canny_image)
    cv2.imshow("Saida", combo_image)
    
    ret,image = capture.read()

    #interrompe loop se a tecla esc for pressionada
    if cv2.waitKey(40) == 27:
        break


# Libera o vídeo e fecha as janelas
capture.release()
cv2.destroyAllWindows()