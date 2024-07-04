from estado import Estado

class Relatorio:
    def __init__(self, time_line, fps, time_divisor=1, unidade="segundos"):
        self.time_line = time_line
        self.fps = fps
        self.time_divisor = time_divisor
        self.unidade = unidade
        self.tempo_total = self.calcular_tempo_total()
        self.tempo_na_faixa = self.calcular_tempo_na_faixa()
        self.tempo_fora = self.calcular_tempo_fora()
        self.tempo_desconhecido = self.calcular_tempo_desconhecido()

    def calcular_tempo_total(self):
        # Total time in frames divided by the fps and then by the time divisor
        return len(self.time_line) / self.fps / self.time_divisor

    def calcular_tempo_na_faixa(self):
        time = 0
        for i in self.time_line:
            if i == Estado.NA_FAIXA:
                time += 1
        return time / self.fps / self.time_divisor

    def calcular_tempo_fora(self):
        time = 0
        for i in self.time_line:
            if i == Estado.FORA:
                time += 1
        return time / self.fps / self.time_divisor

    def calcular_tempo_desconhecido(self):
        time = 0
        for i in self.time_line:
            if i == Estado.DESCONHECIDO:
                time += 1
        return time / self.fps / self.time_divisor

    def __str__(self):
        return (
            f"tempo_total: {round(self.tempo_total, 2)} {self.unidade}\n"
            f"tempo_na_faixa: {round(self.tempo_na_faixa, 2)} {self.unidade}\n"
            f"tempo_fora: {round(self.tempo_fora, 2)} {self.unidade}\n"
            f"tempo_desconhecido: {round(self.tempo_desconhecido, 2)} {self.unidade}"
        )
