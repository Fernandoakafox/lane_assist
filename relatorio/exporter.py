
class CSVExporter:
    def __init__(self, relatorio):
        self.relatorio = relatorio

    def export(self):
        with open("output.csv", "w") as file:
            file.write(str(self.relatorio))

