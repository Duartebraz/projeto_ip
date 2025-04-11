from random import randint, choice
from monstros import Galega, Perna, Lobisomem, Zepilantra

class SpawnerMonstros:
    def __init__(self, player, horario, todos_sprites, monstros, coletaveis, colisao_sprites, limites_mapa):
        self.player = player
        self.horario = horario
        self.todos_sprites = todos_sprites
        self.monstros = monstros
        self.coletaveis = coletaveis
        self.colisao_sprites = colisao_sprites
        self.limites_mapa = limites_mapa

        self.ultima_hora = -1
        self.horas_spawnadas = set()

    def atualizar(self):
        hora_atual = self.horario.hora

        if hora_atual != self.ultima_hora:
            self.ultima_hora = hora_atual

            if hora_atual not in self.horas_spawnadas:
                self.spawnar_monstros(hora_atual)
                self.horas_spawnadas.add(hora_atual)

    def spawnar_monstros(self, hora):
        quantidade = min(5 + hora * 3, 20)  

        tipos = [Galega, Perna, Lobisomem, Zepilantra]
        mapa_largura, mapa_altura = self.limites_mapa

        for _ in range(quantidade):
            classe = choice(tipos)
            x, y = randint(100, mapa_largura - 100), randint(100, mapa_altura - 100)

            while self.player.rect.collidepoint(x, y):
                x, y = randint(100, mapa_largura - 100), randint(100, mapa_altura - 100)

            classe(
                (x, y),
                self.todos_sprites,
                self.monstros,
                alvo=self.player,
                horario=self.horario,
                colisao_sprites=self.colisao_sprites,
                limites_mapa=self.limites_mapa,
                groups_dict={
                    'todos_sprites': self.todos_sprites,
                    'coletaveis': self.coletaveis
                }
            )
