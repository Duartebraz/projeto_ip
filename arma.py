import pygame
from pygame.math import Vector2
from time import time


class Projetil(pygame.sprite.Sprite):
    def __init__(self, pos, direcao, grupos):
        super().__init__(grupos)
        self.image = pygame.Surface((10, 10))
        self.image.fill('red')
        self.rect = self.image.get_rect(center=pos)
        self.velocidade = 8
        self.direcao = direcao.normalize()

    def update(self, dt):
        self.rect.center += self.direcao * self.velocidade

class Arma:
    def __init__(self, jogador, grupo_sprites):
        self.jogador = jogador
        self.grupo_sprites = grupo_sprites
        self.cooldown = 1
        #esse é o cooldown entre os tiros
        self.ultimo_ataque = time()
        self.municao = 10

    def update(self):
        agora = time()
        if self.municao > 0 and agora - self.ultimo_ataque >= self.cooldown:
            self.atacar()
            self.ultimo_ataque = agora

    def atacar(self):
        #calcula o angulo do jogador com o mouse pra mirar
        mouse_pos = pygame.mouse.get_pos()
        player_pos = self.jogador.rect.center

        direcao = Vector2(mouse_pos) - Vector2(player_pos)
        
        if direcao.length() == 0:
            return
            
        Projetil(player_pos, direcao, self.grupo_sprites)
        self.municao -= 1


