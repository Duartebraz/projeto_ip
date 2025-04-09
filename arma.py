import pygame
from pygame.math import Vector2
from os.path import join
from time import time
import math

class Projetil(pygame.sprite.Sprite):
    def __init__(self, pos, direcao, grupos, grupo_inimigos):
        super().__init__(grupos)
        self.original_image = pygame.image.load(join('images', 'player', 'projetil.png')).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (30, 10))
        
        angulo = math.degrees(math.atan2(-direcao.y, direcao.x))
        self.image = pygame.transform.rotate(self.original_image, angulo)
        self.rect = self.image.get_rect(center=pos)

        self.velocidade = 8
        self.direcao = direcao.normalize()

    def update(self):
        self.rect.center += self.direcao * self.velocidade
        self.colidiu()
        if self.rect.x > 1280 or self.rect.x < -32 or self.rect.y > 720 or self.rect.y < -32:
            self.kill()

    def colidiu(self):
        for inimigo in self.monstros:
            if inimigo.rect.colliderect(self.rect):
                inimigo.kill()
                self.kill()
                break

class Arma:
    def __init__(self, jogador, grupo_sprites, monstros):
        self.jogador = jogador
        self.grupo_sprites = grupo_sprites
        self.monstros = monstros
        self.cooldown = 1
        self.ultimo_ataque = time()
        self.municao = 10

    def update(self, offset):
        agora = time()
        if self.municao > 0 and agora - self.ultimo_ataque >= self.cooldown:
            if pygame.mouse.get_pressed()[0]:  # botão esquerdo
                self.atacar(offset)
                self.ultimo_ataque = agora

    def atacar(self, offset):
        mouse_pos = Vector2(pygame.mouse.get_pos()) + offset
        player_pos = Vector2(self.jogador.rect.center)
    
        direcao = mouse_pos - player_pos

        if direcao.length() == 0:
            return

        Projetil(player_pos, direcao, self.grupo_sprites, self.monstros)
        self.municao -= 1


