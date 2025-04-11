from configuracoes import *
import time

class Horario:
    def __init__(self):
        self.tempo_inicial = time.time()
        self.hora = 0
        self.minuto = 0

    def atualizar(self):
        tempo_passado = time.time() - self.tempo_inicial
        minutos_totais = int(tempo_passado) % (8 * 60)  
        self.hora = (minutos_totais // 60) % 8
        self.minuto = minutos_totais % 60

    def aplicar_filtro(self, tela):
        alpha = max(0, 180 - int((self.hora / 7) * 180))
        filtro = pygame.Surface(tela.get_size())
        filtro.fill((0, 0, 0))
        filtro.set_alpha(alpha)
        tela.blit(filtro, (0, 0))

    def desenhar_hora(self, tela):
        fonte = pygame.font.SysFont(None, 36)
        texto = fonte.render(f"{self.hora:02d}:{self.minuto:02d}", True, (255, 255, 255))
        tela.blit(texto, (10, 10))

    def avancar_hora(self, horas):
        segundos = horas * 60 
        self.tempo_inicial -= segundos
