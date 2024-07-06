import os

class MenuParent:

    DIRETORIO_VIDEOS = "videos"

    def __init__(self):
        self.plataform = os.name

    def apagar_terminal(self):
        if (self.plataform == "posix"):
            os.system("clear") # Linux
        else:
            os.system("cls")   # Windows

    def pressione_enter_para_continuar(self):
        input("Precione ENTER para continuar...")

    def opcao_invalida(self):
        print("Opção inválida!")
        self.pressione_enter_para_continuar()