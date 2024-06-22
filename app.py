import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

def lineDashBoardColor(lane_image, info_lines):
    if info_lines == "left and right":
        cv2.line(lane_image, pt1=(100,80), pt2=(100,160), color=(0,255,0), thickness=10)
        cv2.line(lane_image, pt1=(120,80), pt2=(120,160), color=(0,255,0), thickness=10)
            
    elif info_lines == "left":
        #desenhar uma reta na imagem
        cv2.line(lane_image, pt1=(100,80), pt2=(100,160), color=(0,255,0), thickness=10)
        cv2.line(lane_image, pt1=(120,80), pt2=(120,160), color=(0,255,255), thickness=10)
    elif info_lines == "right":
        #desenhar uma reta na imagem
        cv2.line(lane_image, pt1=(100,80), pt2=(100,160), color=(0,255,255), thickness=10)
        cv2.line(lane_image, pt1=(120,80), pt2=(120,160), color=(0,255,0), thickness=10)
    else:
        cv2.line(lane_image, pt1=(100,80), pt2=(100,160), color=(0,255,255), thickness=10)
        cv2.line(lane_image, pt1=(120,80), pt2=(120,160), color=(0,255,255), thickness=10)

def verifica_mudanca_de_faixa(info_lines, averaged_lines):
    if info_lines == "left and right":
        faixaEsquerda, faixaDireita = averaged_lines
        x1Esquerda,_,_,_ = faixaEsquerda
        x1Direita,_,_,_ = faixaDireita
        if x1Esquerda > 0 and x1Esquerda < 30 or x1Esquerda > 470:
            return True
    elif info_lines == "left":
        x1Esquerda,_,_,_ = averaged_lines[0]
        if x1Esquerda > 0 and x1Esquerda < 100 or x1Esquerda > 470:
            return True
    elif info_lines == "right":
        x1Direita,_,_,_ = averaged_lines[0]
        if x1Direita > 1920 or x1Direita < 1480:
            return True

    return False

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
    """Retorna uma tupla, onde o primeiro elemento é uma string e o segundo elemento é um np array
    
    A string contem a informação do np array, avisando se o np array retornado contém as duas faixas, somente a da esquerda, somente a da direita ou nenhuma.

    """
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


    left_line = None
    right_line = None

    #se existir coordenadas para a linha esquerda
    if left_fit:
        left_fit_average = np.average(left_fit, axis = 0)
        left_line = make_coordinates(image, left_fit_average)

    #se existir coordenadas para a linha direita
    if right_fit:
        right_fit_average = np.average(right_fit, axis = 0)
        right_line = make_coordinates(image, right_fit_average)
    
    #retorna as coordenadas das linhas, se elas existirem, do contrario, retorna coordenadas nulas.
    if left_line is not None and right_line is not None:
        return ("left and right",np.array([left_line, right_line]))
    elif left_line is not None:
        return ("left", np.array([left_line]))
    elif right_line is not None:
        return ("right", np.array([right_line]))
    else:
        return ("nothing",np.array([]))

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
    if lines is not None and len(lines) > 0:
        for line in lines:
            # se a linha não é nula e possui as quatro coordenadas necessarias para traçar uma reta
            if line is not None and len(line) == 4:
                x1,y1,x2,y2 = line
                #desenhando linhas sobre a imagem preta. As linhas utilizam 2 pontos para serem desenhadas
                cv2.line(line_image,(x1,y1),(x2,y2), (0,0,255), thickness=10)
    return line_image

def plotCannyGraphic(canny):
    """Sempre que quiser desenhar o tringulo, é necessario abrir a imagem com o matplotlib para ver as coordenadas dos pontos do triangulo na imagem."""
    plt.imshow(canny)
    plt.show()

def region_of_interest(image):
    alturaDaImagem = image.shape[0] #o parametro 0 do metodo shape, retorna o numero de linhas.
    verticeBaseEsquerda = (0,alturaDaImagem) #antes era 178
    verticeBaseDireita = (1920,alturaDaImagem)
    verticeTopoEsquerda = (557,716)
    verticeTopoDireita = (1370,716)

    #definição dos vertices do trapezio. É uma lista porque fillPoly só aceita listas de poligonos.
    vertices = np.array([
        [verticeBaseEsquerda , verticeBaseDireita , verticeTopoDireita ,verticeTopoEsquerda ]
         ])

    mask = np.zeros_like(image) #criamos um array ndimensional de mesmas proporções que o array image, contendo somente pixels pretos

    cv2.fillPoly(mask, vertices, 255) # estamos aplicando o triangulo na mascara, de modo que o triangulo fique completamente branco.

    masked_image = cv2.bitwise_and(image, mask)

    return masked_image

def main():
    videoPath = "./videos/ultrapassagens.mp4"
    capture = cv2.VideoCapture(videoPath)
    linhaIdentificada = 0
    linhaNaoIdentificada = 0

    while True:
        startTime = time.time()
        # lê um frame do video. Retorna True se a leitura foi bem sucedida e retorna também o frame
        ret, image = capture.read()
        if ret is False:
            break

        lane_image = np.copy(image)
        canny_image = canny(lane_image)
        cropped_image = region_of_interest(canny_image)

        #detectando linhas
        lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]),minLineLength=40, 
        maxLineGap = 5) #maxLineGap representa o espaço entre linhas que posso considerar como se fosse linha.

        #se linhas foram identificadas
        if lines is not None:
            linhaIdentificada += 1

            info_lines, averaged_lines = average_slope_intercept(lane_image, lines)
            if verifica_mudanca_de_faixa(info_lines, averaged_lines):
                # escrevendo texto na imagem
                cv2.putText(lane_image, "Mudanca de faixa", (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
                print("mudanca de faixa-----------")
                
            else:
                cv2.putText(lane_image, "Dentro das linhas", (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)

            # pinta linhas no dashboard (canto superior esquerdo)
            lineDashBoardColor(lane_image, info_lines)
            

            if averaged_lines is not None and len(averaged_lines) > 0:
                line_image = display_lines(lane_image, averaged_lines)
                #Vamos combinar a imagem que mostra as linhas com a imagem real. Para isso, somamos a imagem real com a imagem preta que possui linhas azuis, deste modo os pixels pretos, que valem zero, não irão modificar a imagem, porém, os pixels azuis, que valem 255, irão modificar a imagem.
                combo_image = cv2.addWeighted(lane_image, 1, line_image, 1, 1)
            else:
                combo_image = lane_image

        #se linhas não foram identificadas
        else:
            cv2.putText(lane_image, "Indefinido", (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,165,255), 2)
            #pinta linhas no dashboard
            lineDashBoardColor(lane_image, info_lines)
            combo_image = lane_image
            linhaNaoIdentificada += 1
            

        cv2.imshow("Saida", combo_image)
        #interrompe loop se a tecla esc for pressionada
        if cv2.waitKey(40) == 27:
            break

        endTime = time.time()
        #print(endTime - startTime)

    # Libera o vídeo e fecha as janelas
    capture.release()
    cv2.destroyAllWindows()
    uptime = linhaIdentificada / (linhaNaoIdentificada + linhaIdentificada) * 100
    print("Uptime do lane assist: {:.2f}%".format(uptime))

if __name__ == "__main__":
    main()
