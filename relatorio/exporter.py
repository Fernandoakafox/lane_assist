
class CSVExporter:
    def __init__(self, relatorio):
        self.relatorio = relatorio

    def export(self):
        with open("output.csv", "w") as file:
            file.write(f"Tempo total,Tempo na faixa,Tempo fora,Tempo desconhecido\n")
            file.write(f"{self.relatorio.tempo_total},{self.relatorio.tempo_na_faixa},{self.relatorio.tempo_fora},{self.relatorio.tempo_desconhecido}")