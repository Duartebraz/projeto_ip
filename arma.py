import pygame
from pygame.math import Vector2
from time import time
import math

class Projetil(pygame.sprite.Sprite):
    def __init__(self, pos, direcao, grupos):
        super().__init__(grupos)
        self.original_image = pygame.Surface((10, 4))  # mais retangular para mostrar rotação
        self.original_image.fill('red')

        # calcula ângulo
        angulo = math.degrees(math.atan2(-direcao.y, direcao.x))
        self.image = pygame.transform.rotate(self.original_image, angulo)
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


    def update(self, offset):
        agora = time()
        if self.municao > 0 and agora - self.ultimo_ataque >= self.cooldown:
            if pygame.mouse.get_pressed()[0]:  # botão esquerdo
                self.atacar(offset)
                self.ultimo_ataque = agora


    def atacar(self, offset):
        # converte a posição do mouse para coordenadas do mundo
        mouse_pos = Vector2(pygame.mouse.get_pos()) + offset
        player_pos = Vector2(self.jogador.rect.center)
    
        direcao = mouse_pos - player_pos

        if direcao.length() == 0:
            return

        Projetil(player_pos, direcao, self.grupo_sprites)
        self.municao -= 1

