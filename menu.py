from enum import Enum ,auto
from lane_assist import LaneAssist
from menu_parent import MenuParent
import os
from pathlib import Path
from enums.car_atributes import CarAtributes
from enums.car_atributes import Presets

class OpcoesMenu(Enum):
    ESCOLHER_VIDEO = auto()
    INICIAR_COM_VIDEO = auto()
    ESCOLHER_AJUSTES_DE_CAMERA = auto()
    SAIR = 0

class FormatoExibicao(Enum):
    VER_COMBOIMAGE = auto()
    VER_MULTIPLAS_IMAGENS = auto()
    SOMENTE_ALERTAS = auto()
    VOLTAR = 0


# Classe responsável por manipular e mostrar os Menus de exibição.
# Menus de exibição são os que apenas informam as opções
# para o usuário para auxliar na sua escolha
class Menu(MenuParent):

    def __init__(self):
        super().__init__()
        self.video_path = "videos/ultrapassagens.mp4"
        self.car_atributes = CarAtributes(Presets.VW_SANTANA)

    # ============================== .:| Opções de menu para rodar |:. ==============================
    def iniciar_com_video(self):
        self.apagar_terminal()
        print("Escolher Vídeo:")
        self.mostrar_menu_formato_exibicao()

    def escolher_ajustes_camera(self):
        self.apagar_terminal()
        print("Escolha o ajuste de câmera:")
        self.ajustar_camera()

    def sair(self):
        self.apagar_terminal()
        print("Saindo...")


    # ============================ .:| Opções de formato de exibição |:. ============================
    def ver_comboimage(self):
        self.apagar_terminal()
        print("Visualizando comboImage.")
        LaneAssist(self.video_path, self.car_atributes).debug_mode(combo_image_output = True)

    def ver_multiplas_imagens(self):
        self.apagar_terminal()
        print("Visualizando multiplas imagens.")
        LaneAssist(self.video_path, self.car_atributes).debug_mode(False, True, True, True, True)

    def somente_alertas(self):
        self.apagar_terminal()
        print("Exibindo apenas alertas, sem imagens.")
        LaneAssist(self.video_path, self.car_atributes).sentinel_mode()


    # =================================== .:| Opções auxliares de escolha |:. ======================================

    # Função resposnsável por printar os vídeo disponíveis na pasta [videos]
    def mostrar_opcoes_video(self):
        # guardando os vídeos disponíveis
        lista_videos = os.listdir(self.DIRETORIO_VIDEOS)

        # essa lista será responsável por armazenar os vídeos
        videos = []

        # iterrando por cada arquivo presente na pasta de vídeos do projeto
        for arquivo in lista_videos:
            # iremos adicionar a lista de vídeos somente os arquivo com as extenções de arquivo
            # ( .mp4 ), ( .avi ) e ( .mov ) 
            # ou seja, arquivos de vídeo
            if Path(arquivo).suffix.lower() in [".mp4", ".avi", ".mov"]:
                videos.append(arquivo)

        while (True):
            self.apagar_terminal()
            print("Opções de vídeo:")

            # iterrando pela lista de vídeos para exibir as opções no terminal
            for i, video in enumerate(videos):
                print(f"[{i+1}] {video}")

            print("[0] voltar")

            # Lendo a entrada do usuário em int para servir de index
            escolha_usuario = int(input("\nDigite o index do vídeo que deseja exibir: "))

            # validando a entrada do usuário
            if escolha_usuario == 0:
                break
            
            if 1 <= escolha_usuario <= len(videos):
                video_selecionado = videos[escolha_usuario - 1]

                # estamos atualizando path do vídeo para o que o usuário escolheu
                self.video_path = str(Path(self.DIRETORIO_VIDEOS) / video_selecionado)

                # FeedBack da escolha do usuário
                self.apagar_terminal()
                print(f"Você escolheu o vídeo: {video_selecionado}")
                self.pressione_enter_para_continuar()

                break

            else:
                self.opcao_invalida()
    

    # === Menu Formato de Exibição ==
    # Essa função é responsável por manter o usuário interagindo (escolhendo as opções)
    # até este degitar uma entrada válida
    def mostrar_menu_formato_exibicao(self):
        
        while (True):
            self.apagar_terminal()
            print("\nEscolha o formato de exibição:")

            # vamos iterar por cada opção presente no Nosso Enum FormatoExibicao
            # e exibir seu respectivo nome e index
            for opcao in FormatoExibicao:
                print(f"[{opcao.value}] {opcao.name.replace('_', ' ').capitalize()}")
            escolha = input("\nEscolha uma opção: ")

            # conforme a escolha do usuário iremos seguir um fluxo diferente
            # esse fluxo é referente ao formato de imagem que será exibido
            # do Lane Assist
            try:
                match (FormatoExibicao(int(escolha))):
                    
                    case FormatoExibicao.VER_COMBOIMAGE:
                        self.ver_comboimage()
                        break

                    case FormatoExibicao.VER_MULTIPLAS_IMAGENS:
                        self.ver_multiplas_imagens()
                        break

                    case FormatoExibicao.SOMENTE_ALERTAS:
                        self.somente_alertas()
                        break

                    case FormatoExibicao.VOLTAR:
                        break

            except ValueError:
                self.opcao_invalida()


    # Essa função é responsável por interagir com o usuário para que ele escolha
    # a configuração de câmre mais adequada para o cenário desejado
    def ajustar_camera(self):
        
        while (True):
            self.apagar_terminal()
            print("\nEscolha o ajuste de câmera:")

            # Presets é um Enum presente em car_atributes
            # ele representa os ajustes pre-configurados já existentes
            for opcao in Presets:
                print(f"[{opcao.value}] {opcao.name.replace('_', ' ').capitalize()}")
            
            # Dessa vez, vamos adicionar uma opção de voltar diretamente no código
            # ser estar presente no Enum diretamente, pois o Enum serve para outras finalidades
            print("[0] Voltar")
            escolha = input("\nEscolha uma opção: ")

            # validar se o usuário não está tentando voltar
            if (escolha == 0):
                break

            try:
                # Fazendo essa convesão, conseguimos validar se a escolha do usuário
                # está dentro das opçãos disponíveis
                preset = Presets(int(escolha))

                # Atribuímos a escolha do usuário ao atributo da classe
                self.car_atributes = CarAtributes(preset)
                break
                    
            except ValueError:
                self.opcao_invalida()


    # === Menu principal ===
    # Essa função é responsável por listar o menu principal
    def mostrar_menu_principal(self):
        self.apagar_terminal()
        print(f"Vídeo atual: [ {self.video_path} ]")
        print(f"A camera está ajustada para: [ {self.car_atributes.name} ]")
        print("\n=== .:| Menu Principal |:. ===")

        # vamos iterar por cada opção presente no Nosso Enum OpcoesMenu
        # e exibir seu respectivo nome e index
        for opcao in OpcoesMenu:
            print(f"[{opcao.value}] {opcao.name.replace('_', ' ').capitalize()}")
        escolha = input("\nEscolha uma opção: ")
        return escolha
    

    # Função inicial, ela é resposável por iniciar o loop de interação com o usuário
    def start(self):
        while True:
            opcao = self.mostrar_menu_principal()

            try:
                match OpcoesMenu(int(opcao)):

                    case OpcoesMenu.ESCOLHER_VIDEO:
                        self.mostrar_opcoes_video()
                        continue

                    case OpcoesMenu.INICIAR_COM_VIDEO:
                        self.mostrar_menu_formato_exibicao()
                        continue

                    case OpcoesMenu.ESCOLHER_AJUSTES_DE_CAMERA:
                        self.escolher_ajustes_camera()
                        continue

                    case OpcoesMenu.SAIR:
                        break

            except ValueError:
                self.opcao_invalida()

        print("Programa encerrado!")

                