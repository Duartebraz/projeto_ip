from configuracoes import *
import time

class Horario:
    def __init__(self):
        self.tempo_inicial = time.time()
        self.hora = 0  

    def atualizar(self):
        tempo_passado = time.time() - self.tempo_inicial
        self.hora = int(tempo_passado // 10) % 8 
    def aplicar_filtro(self, tela):
        alpha = max(0, 180 - int((self.hora / 7) * 180))

        filtro = pygame.Surface(tela.get_size())
        filtro.fill((0, 0, 0))
        filtro.set_alpha(alpha)
        tela.blit(filtro, (0, 0))

    def desenhar_hora(self, tela):
        fonte = pygame.font.SysFont(None, 36)
        texto = fonte.render(f"{self.hora:02d}:00", True, (255, 255, 255))
        tela.blit(texto, (10, 10))