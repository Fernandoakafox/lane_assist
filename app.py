import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

def lineDashBoardColor(laneImage, infoLines):
    if infoLines == "left and right":
        cv2.line(laneImage, pt1=(100,80), pt2=(100,160), color=(0,255,0), thickness=10)
        cv2.line(laneImage, pt1=(120,80), pt2=(120,160), color=(0,255,0), thickness=10)
            
    elif infoLines == "left":
        #desenhar uma reta na imagem
        cv2.line(laneImage, pt1=(100,80), pt2=(100,160), color=(0,255,0), thickness=10)
        cv2.line(laneImage, pt1=(120,80), pt2=(120,160), color=(0,255,255), thickness=10)
    elif infoLines == "right":
        #desenhar uma reta na imagem
        cv2.line(laneImage, pt1=(100,80), pt2=(100,160), color=(0,255,255), thickness=10)
        cv2.line(laneImage, pt1=(120,80), pt2=(120,160), color=(0,255,0), thickness=10)
    else:
        cv2.line(laneImage, pt1=(100,80), pt2=(100,160), color=(0,255,255), thickness=10)
        cv2.line(laneImage, pt1=(120,80), pt2=(120,160), color=(0,255,255), thickness=10)

def verificaMudancaDeFaixa(infoLines, averagedLines):
    if infoLines == "left and right":
        faixaEsquerda, faixaDireita = averagedLines
        x1Esquerda,_,_,_ = faixaEsquerda
        x1Direita,_,_,_ = faixaDireita
        if x1Esquerda < 40 or x1Esquerda > 560:
            print(f"X1 esquerda: {x1Esquerda}")
            return True
    elif infoLines == "left":
        x1Esquerda,_,_,_ = averagedLines[0]
        if x1Esquerda < 40 or x1Esquerda > 560:
            print(f"X1 esquerda: {x1Esquerda}")
            return True
    elif infoLines == "right":
        x1Direita,_,_,_ = averagedLines[0]
        if x1Direita > 1920 or x1Direita < 1480:
            print(f"X1 esquerda: {x1Direita}")
            return True

    return False

def getVideoCartezianDimension(imagem):
    """Recebe um frame, no formato ndimensional array. Printa a imagem em um plano cartesiano"""
    plt.imshow(imagem)
    plt.show()

def makeCoordinates(image, lineParameters):
    slope, intercept = lineParameters
    #pegando a base da imagem
    y1 = image.shape[0]
    #pegando o "meio" da imagem
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1,y1,x2,y2])

def averageSlopeIntercept(image, lines):
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
        if slope < 0:
            leftFit.append((slope, intercept))
        else:
            rightFit.append((slope, intercept))


    leftLine = None
    rightLine = None

    #se existir coordenadas para a linha esquerda
    if leftFit:
        leftFitAverage = np.average(leftFit, axis = 0)
        leftLine = makeCoordinates(image, leftFitAverage)

    #se existir coordenadas para a linha direita
    if rightFit:
        rightFitAverage = np.average(rightFit, axis = 0)
        rightLine = makeCoordinates(image, rightFitAverage)
    
    #retorna as coordenadas das linhas, se elas existirem, do contrario, retorna coordenadas nulas.
    if leftLine is not None and rightLine is not None:
        return ("left and right",np.array([leftLine, rightLine]))
    elif leftLine is not None:
        return ("left", np.array([leftLine]))
    elif rightLine is not None:
        return ("right", np.array([rightLine]))
    else:
        return ("nothing",np.array([]))

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    lowThreshold = 50
    highThreshold = 150
    canny = cv2.Canny(blur, lowThreshold, highThreshold)
    return canny

def displayLines(image, lines):
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

def regionOfInterest(image):
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

        laneImage = np.copy(image)
        cannyImage = canny(laneImage)
        croppedImage = regionOfInterest(cannyImage)

        #detectando linhas
        lines = cv2.HoughLinesP(croppedImage, 2, np.pi/180, 100, np.array([]),minLineLength=40, 
        maxLineGap = 5) #maxLineGap representa o espaço entre linhas que posso considerar como se fosse linha.

        #se linhas foram identificadas
        if lines is not None:
            linhaIdentificada += 1

            infoLines, averagedLines = averageSlopeIntercept(laneImage, lines)
            if verificaMudancaDeFaixa(infoLines, averagedLines):
                # escrevendo texto na imagem
                cv2.putText(laneImage, "Mudanca de faixa", (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
                
            else:
                cv2.putText(laneImage, "Dentro das linhas", (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)

            # pinta linhas no dashboard (canto superior esquerdo)
            lineDashBoardColor(laneImage, infoLines)
            

            if averagedLines is not None and len(averagedLines) > 0:
                lineImage = displayLines(laneImage, averagedLines)
                #Vamos combinar a imagem que mostra as linhas com a imagem real. Para isso, somamos a imagem real com a imagem preta que possui linhas azuis, deste modo os pixels pretos, que valem zero, não irão modificar a imagem, porém, os pixels azuis, que valem 255, irão modificar a imagem.
                comboImage = cv2.addWeighted(laneImage, 1, lineImage, 1, 1)
            else:
                comboImage = laneImage

        #se linhas não foram identificadas
        else:
            cv2.putText(laneImage, "Indefinido", (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,165,255), 2)
            #pinta linhas no dashboard
            lineDashBoardColor(laneImage, infoLines)
            comboImage = laneImage
            linhaNaoIdentificada += 1
            

        cv2.imshow("Saida", comboImage)
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
