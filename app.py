import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

#--------------------------Manipulação da imagem-------------------------------#

# Função para redimensionar uma imagem mantendo a proporção
def redimensionarImagem(img, largura_desejada):
    proporcao = largura_desejada / img.shape[1]
    altura_desejada = int(img.shape[0] * proporcao)
    return cv2.resize(img, (largura_desejada, altura_desejada))

def getVideoCartezianDimension(imagem):
    """Recebe um frame, no formato ndimensional array. Printa a imagem em um plano cartesiano"""
    plt.imshow(imagem)
    plt.show()

def cannySatura(image):
    rgb2hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
    rgb2hls[:, :, 2] = 255
    hls2rgb = cv2.cvtColor(rgb2hls, cv2.COLOR_HLS2RGB)
    gray = cv2.cvtColor(hls2rgb, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0) #reduzir ruido
    minThreshold = 50 #todo brilho abaixo do minThreshold será desconsiderado como borda
    maxThreshold = 150 #todo brilho acima do maxThreshold será concerteza considerado como borda
    #o que acontece entre os valores minThreshold e maxThreshold é mais complicado 
    canny = cv2.Canny(blur, minThreshold, maxThreshold)
    kernel = np.zeros((3,3), np.uint8)
    erode = cv2.erode(canny, kernel, iterations=1)
    return erode

def canny(image):
    h,l,s = cv2.split(cv2.cvtColor(image,cv2.COLOR_BGR2HLS))
    cannyImage = cv2.Canny(l,100, 150)
    return cannyImage

def plotCannyGraphic(canny):
    """Sempre que quiser desenhar o tringulo, é necessario abrir a imagem com o matplotlib para ver as coordenadas dos pontos do triangulo na imagem."""
    plt.imshow(canny)
    plt.show()

def regionOfInterest(image):
    alturaDaImagem = image.shape[0] #o parametro 0 do metodo shape, retorna o numero de linhas.
    verticeBaseEsquerda = (570,alturaDaImagem-200) #antes era 178
    verticeBaseDireita = (1350,alturaDaImagem-200)
    verticeTopoEsquerda = (770,750)
    verticeTopoDireita = (1150,750)

    #definição dos vertices do trapezio. É uma lista porque fillPoly só aceita listas de poligonos.
    vertices = np.array([
        [verticeBaseEsquerda , verticeBaseDireita , verticeTopoDireita ,verticeTopoEsquerda ]
         ])

    mask = np.zeros_like(image) #criamos um array ndimensional de mesmas proporções que o array image, contendo somente pixels pretos

    cv2.fillPoly(mask, vertices, 255) # estamos aplicando o triangulo na mascara, de modo que o triangulo fique completamente branco.

    masked_image = cv2.bitwise_and(image, mask)

    return masked_image

#--------------------------------------Line--------------------------------------#

def displayLines(image, lines):
    # uma imagem preta, pois é uma matriz de zeros, da mesma resolução que a imagem
    line_image = np.zeros_like(image)
    #verificamos se a matriz de linhas possui alguma linha
    if lines is not None and len(lines) > 0:
        for line in lines:
            # se a linha não é nula e possui as quatro coordenadas necessarias para traçar uma reta
            if line is not None and len(line) == 4:
                x1,y1,x2,y2 = line
                try:
                    #desenhando linhas sobre a imagem preta. As linhas utilizam 2 pontos para serem desenhadas
                    cv2.line(line_image,(x1,y1),(x2,y2), (0,0,255), thickness=10)
                except:
                    print("Gabriel")
    return line_image

def displayAllLines(image, lines):
    # uma imagem preta, pois é uma matriz de zeros, da mesma resolução que a imagem
    line_image = np.zeros_like(image)
    #verificamos se a matriz de linhas possui alguma linha
    if lines is not None and len(lines) > 0:
        for line in lines:
            allLines = line[0]
            # se a linha não é nula e possui as quatro coordenadas necessarias para traçar uma reta
            if line is not None and len(allLines) == 4:
                x1,y1,x2,y2 = allLines
                parameters = np.polyfit((x1,x2),(y1,y2), 1)
                slope = parameters[0]
                if abs(slope) > 0.4: #ignora linhas com coeficiente angular no intervalo ]0.5, -0.5[
                    try:
                        #desenhando linhas sobre a imagem preta. As linhas utilizam 2 pontos para serem desenhadas
                        cv2.line(line_image,(x1,y1),(x2,y2), (0,0,255), thickness=10)
                    except:
                        print("Gabriel")
    return line_image

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

def makeCoordinates(image, lineParameters):
    slope, intercept = lineParameters
    #pegando a base da imagem
    y1 = image.shape[0]
    #pegando o "meio" da imagem
    y2 = int(y1*(4/5))
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

#------------------------------------Dashboard-----------------------------------#

def lineDashBoardColor(laneImage, infoLines):
    if infoLines == "left and right":
        cv2.line(laneImage, pt1=(100,80), pt2=(100,160), color=(0,255,0), thickness=10)
        cv2.line(laneImage, pt1=(120,80), pt2=(120,160), color=(0,255,0), thickness=10)
            
    elif infoLines == "left":
        #desenhar uma reta na imagem
        cv2.line(laneImage, pt1=(100,80), pt2=(100,160), color=(0,255,0), thickness=10)
        cv2.line(laneImage, pt1=(120,80), pt2=(120,160), color=(128,128,128), thickness=10)
    elif infoLines == "right":
        #desenhar uma reta na imagem
        cv2.line(laneImage, pt1=(100,80), pt2=(100,160), color=(128,128,128), thickness=10)
        cv2.line(laneImage, pt1=(120,80), pt2=(120,160), color=(0,255,0), thickness=10)
    else:
        cv2.line(laneImage, pt1=(100,80), pt2=(100,160), color=(128,128,128), thickness=10)
        cv2.line(laneImage, pt1=(120,80), pt2=(120,160), color=(128,128,128), thickness=10)

        
def main():
    videoPath = "./videos/acessoGrasel.mp4"
    capture = cv2.VideoCapture(videoPath)
    linhaIdentificada = 0
    linhaNaoIdentificada = 0

    while True:
        startTime = time.time()
        # lê um frame do video. Retorna True se a leitura foi bem sucedida e retorna também o frame
        ret, image = capture.read()
        if ret is False:
            break

        baseImage = np.copy(image)
        cannyImage = canny(baseImage)
        croppedImage = regionOfInterest(cannyImage)

        #detectando linhas
        lines = cv2.HoughLinesP(croppedImage, 2, np.pi/180, 100, np.array([]),minLineLength=40, 
        maxLineGap = 5) #maxLineGap representa o espaço entre linhas que posso considerar como se fosse linha.

        #se linhas foram identificadas
        if lines is not None:
            linhaIdentificada += 1

            infoLines, averagedLines = averageSlopeIntercept(baseImage, lines)
            if infoLines is not "nothing":
                if verificaMudancaDeFaixa(infoLines, averagedLines):
                    # escrevendo texto na imagem
                    cv2.putText(baseImage, "Mudanca de faixa", (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)    
                else:
                    cv2.putText(baseImage, "Dentro das faixas", (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
            else:
                cv2.putText(baseImage, "Indefinido", (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,165,255), 2)

            # pinta linhas no dashboard (canto superior esquerdo)
            lineDashBoardColor(baseImage, infoLines)

            if averagedLines is not None and len(averagedLines) > 0:
                #lineImage = displayLines(laneImage, averagedLines)
                lineImage = displayLines(baseImage, averagedLines)
                #Vamos combinar a imagem que mostra as linhas com a imagem real. Para isso, somamos a imagem real com a imagem preta que possui linhas azuis, deste modo os pixels pretos, que valem zero, não irão modificar a imagem, porém, os pixels azuis, que valem 255, irão modificar a imagem.
                comboImage = cv2.addWeighted(baseImage, 1, lineImage, 1, 1)       
            else:
                comboImage = baseImage

        #se linhas não foram identificadas
        else:
            cv2.putText(baseImage, "Indefinido", (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,165,255), 2)
            #pinta linhas no dashboard
            lineDashBoardColor(baseImage, "")
            comboImage = baseImage
            linhaNaoIdentificada += 1
            
        # Definir a largura desejada para a exibição
        largura_janela = 1400
       
        #prints das diferentes imagens
        #cv2.imshow("Normal", baseImage)
        cv2.imshow("Cropped RGB", redimensionarImagem(regionOfInterest(baseImage), 1200))
        cv2.imshow("comboImage", redimensionarImagem(comboImage, largura_janela))
        #cv2.imshow("croppedImage", redimensionar_imagem(croppedImage, largura_janela))
        #cv2.imshow("grayImage", redimensionar_imagem(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY), largura_janela))

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