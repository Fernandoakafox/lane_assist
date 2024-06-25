from estado import Estado

class Relatorio:
    def __init__(self, time_line, fps):
        self.time_line = time_line
        self.fps = fps
        self.tempo_total = self.calcular_tempo_total()
        self.tempo_na_faixa = self.calcular_tempo_na_faixa()
        self.tempo_fora = self.calcular_tempo_fora
        self.tempo_desconhecido = self.calcular_tempo_desconhecido()

    def calcular_tempo_total(self):
        return len(self.time_line)

    def calcular_tempo_na_faixa(self):
        time = 0
        for i in self.time_line:
            if i == Estado.NA_FAIXA:
                time += 1
        return time

    def calcular_tempo_fora(self):
        time = 0
        for i in self.time_line:
            if i == Estado.FORA:
                time += 1
        return time

    def calcular_tempo_desconhecido(self):
        time = 0
        for i in self.time_line:
            if i == Estado.DESCONHECIDO:
                time += 1
        return time


class RelatorioMinutos(Relatorio):
    def __init__(self, time_line, fps):
        super().__init__(time_line, fps)
        self.tempo_total = self.tempo_total / self.fps / 60
        self.tempo_na_faixa = self.tempo_na_faixa / self.fps / 60
        self.tempo_fora = self.tempo_fora / self.fps / 60
        self.tempo_desconhecido = self.tempo_desconhecido / self.fps / 60

    def __str__(self):
        return f"Tempo total: {self.tempo_total} minutos\nTempo na faixa: {self.tempo_na_faixa} minutos\nTempo fora: {self.tempo_fora} minutos\nTempo desconhecido: {self.tempo_desconhecido} minutos"
