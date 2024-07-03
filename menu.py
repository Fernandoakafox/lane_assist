from enum import Enum ,auto

class MenuPrincipal(Enum):
    ESCOLHER_VIDEO = auto()
    UTILIZAR_CAMERA_EXTERNA = auto()
    INICIAR_CASOS_DE_TESTE = auto()
    SAIR = auto()

class FormatoExibicao(Enum):
    VER_COMBOIMAGE = auto()
    VER_MULTIPLAS_IMAGENS = auto()
    SOMENTE_ALERTAS = auto()

def escolher_video():
    print("Você escolheu a opção de escolher vídeo.")
    mostrar_menu_formato_exibicao()

def utilizar_camera_externa():
    print("Você escolheu utilizar a câmera externa.")

def iniciar_casos_de_teste():
    print("Você escolheu iniciar casos de teste.")

def sair():
    print("Saindo...")

def ver_comboimage():
    print("Visualizando comboImage.")

def ver_multiplas_imagens():
    print("Visualizando comboImage, croppedImage, cannyImage e allLines.")

def somente_alertas():
    print("Exibindo apenas alertas, sem imagens.")

def mostrar_menu_principal():
    print("\nMenu principal:")
    for opcao in MenuPrincipal:
        print(f"({opcao.value}) {opcao.name.replace('_', ' ').capitalize()}")
    escolha = input("Escolha uma opção: ")
    return escolha

def mostrar_menu_formato_exibicao():
    print("\nEscolher formato de Exibição")
    for opcao in FormatoExibicao:
        print(f"({opcao.value}) {opcao.name.replace('_', ' ').capitalize()}")
    escolha = input("Escolha uma opção: ")
    
    try:
        opcao_formato = FormatoExibicao(int(escolha))
        if opcao_formato == FormatoExibicao.VER_COMBOIMAGE:
            ver_comboimage()
        elif opcao_formato == FormatoExibicao.VER_MULTIPLAS_IMAGENS:
            ver_multiplas_imagens()
        elif opcao_formato == FormatoExibicao.SOMENTE_ALERTAS:
            somente_alertas()
    except (ValueError, KeyError):
        print("Opção inválida. Retornando ao menu principal.")

def main():
    while True:
        escolha = mostrar_menu_principal()
        try:
            opcao_menu = MenuPrincipal(int(escolha))
            if opcao_menu == MenuPrincipal.ESCOLHER_VIDEO:
                escolher_video()
            elif opcao_menu == MenuPrincipal.UTILIZAR_CAMERA_EXTERNA:
                utilizar_camera_externa()
            elif opcao_menu == MenuPrincipal.INICIAR_CASOS_DE_TESTE:
                iniciar_casos_de_teste()
            elif opcao_menu == MenuPrincipal.SAIR:
                sair()
                break
        except (ValueError, KeyError):
            print("Opção inválida. Por favor, escolha uma opção válida.")