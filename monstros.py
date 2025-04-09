import pygame
from configuracoes import *
from os.path import join

class Monstros(pygame.sprite.Sprite): 
    def __init__(self, pos, *groups, alvo, velocidade, vida, nome, colisao_sprites):
        super().__init__(*groups)
        self.image = pygame.image.load(join('images', 'monstros', nome, '0.png')).convert_alpha()
        self.rect =  self.image.get_rect(center = pos)
        self.hitbox_rect = self.rect.inflate(0,0)
        self.direcao = pygame.Vector2()
        self.velocidade = velocidade
        self.vida = vida
        self.alvo = alvo
        self.colisao_sprites = colisao_sprites

    def seguir_alvo(self):
        h

    def movimentar(self):
        self.hitbox_rect.x += self.direcao.x * self.velocidade
        self.colisao('horizontal')
        self.hitbox_rect.y += self.direcao.y * self.velocidade
        self.colisao('vertical')
        self.rect.center = self.hitbox_rect.center

    def colisao (self, direcao):
        for sprite in self.colisao_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direcao == 'horizontal':
                    if self.direcao.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direcao.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direcao.y <0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direcao.y >0: self.hitbox_rect.bottom = sprite.rect.top

    def levar_dano(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.kill()

    def update(self, dt):
        self.seguir_alvo()
        self.movimentar(dt)

class Galega(Monstros):
    def __init__(self, pos, *groups, alvo, colisao_sprites):
        super().__init__(pos, *groups, alvo = alvo, velocidade = 16, vida = vida, nome = 'galega', colisao_sprites=colisao_sprites)

class Perna(Monstros):
    def __init__(self, pos, *groups, alvo, colisao_sprites):
        super().__init__(pos, *groups, alvo = alvo, velocidade = 18, vida = vida, nome = 'perna', colisao_sprites=colisao_sprites)

class Monstro3(Monstros):
    def __init__(self, pos, *groups, alvo, colisao_sprites):
        super().__init__(pos, *groups, alvo = alvo, velocidade = 14, vida = vida, nome = 'monstro3', colisao_sprites=colisao_sprites)
